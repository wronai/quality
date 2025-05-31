#!/usr/bin/env node
/**
 * Quality Watcher - Real-time code quality monitoring
 *
 * Monitors file changes and provides immediate feedback on code quality violations.
 * Integrates with Quality Guard to provide continuous quality enforcement.
 */

const fs = require('fs');
const path = require('path');
const chokidar = require('chokidar');
const { spawn, exec } = require('child_process');
const notifier = require('node-notifier');

class QualityWatcher {
    constructor(config = {}) {
        this.config = {
            watchPaths: config.watchPaths || ['src/**/*.{js,ts,py}', 'core/**/*.py'],
            ignored: config.ignored || [
                '**/node_modules/**',
                '**/.git/**',
                '**/dist/**',
                '**/__pycache__/**',
                '**/venv/**'
            ],
            debounceMs: config.debounceMs || 500,
            enableNotifications: config.enableNotifications !== false,
            qualityConfigPath: config.qualityConfigPath || 'quality-config.json',
            logLevel: config.logLevel || 'info',
            ...config
        };

        this.qualityConfig = this.loadQualityConfig();
        this.debounceTimers = new Map();
        this.violationCounts = new Map();
        this.lastViolations = new Map();

        this.setupWatcher();
        this.setupSignalHandlers();

        console.log('🔍 Quality Watcher started');
        console.log(`👀 Watching: ${this.config.watchPaths.join(', ')}`);
    }

    loadQualityConfig() {
        try {
            const configPath = path.resolve(this.config.qualityConfigPath);
            if (fs.existsSync(configPath)) {
                const content = fs.readFileSync(configPath, 'utf8');
                return JSON.parse(content);
            }
        } catch (error) {
            this.log('warn', `Failed to load quality config: ${error.message}`);
        }

        // Default configuration
        return {
            rules: {
                max_file_lines: 200,
                max_function_lines: 50,
                max_complexity: 10,
                require_tests: true,
                require_docstrings: true
            },
            enforcement: {
                level: 'error',
                real_time_feedback: true
            }
        };
    }

    setupWatcher() {
        this.watcher = chokidar.watch(this.config.watchPaths, {
            ignored: this.config.ignored,
            persistent: true,
            ignoreInitial: true
        });

        this.watcher
            .on('change', (filePath) => this.handleFileChange(filePath, 'changed'))
            .on('add', (filePath) => this.handleFileChange(filePath, 'added'))
            .on('unlink', (filePath) => this.handleFileChange(filePath, 'removed'))
            .on('error', (error) => this.log('error', `Watcher error: ${error}`));
    }

    setupSignalHandlers() {
        process.on('SIGINT', () => {
            console.log('\n🛑 Quality Watcher stopping...');
            this.cleanup();
            process.exit(0);
        });

        process.on('SIGTERM', () => {
            this.cleanup();
            process.exit(0);
        });
    }

    handleFileChange(filePath, changeType) {
        const fileKey = path.resolve(filePath);

        // Clear existing debounce timer
        if (this.debounceTimers.has(fileKey)) {
            clearTimeout(this.debounceTimers.get(fileKey));
        }

        // Set new debounce timer
        const timer = setTimeout(() => {
            this.processFileChange(filePath, changeType);
            this.debounceTimers.delete(fileKey);
        }, this.config.debounceMs);

        this.debounceTimers.set(fileKey, timer);
    }

    async processFileChange(filePath, changeType) {
        const timestamp = new Date().toISOString();
        this.log('info', `📝 ${changeType}: ${filePath}`);

        if (changeType === 'removed') {
            this.violationCounts.delete(filePath);
            this.lastViolations.delete(filePath);
            return;
        }

        try {
            const violations = await this.analyzeFile(filePath);
            this.handleViolations(filePath, violations, changeType);
        } catch (error) {
            this.log('error', `Analysis failed for ${filePath}: ${error.message}`);
        }
    }

    async analyzeFile(filePath) {
        const extension = path.extname(filePath);
        const violations = [];

        // Basic file size check
        const stats = fs.statSync(filePath);
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n');
        const lineCount = lines.length;

        if (lineCount > this.qualityConfig.rules.max_file_lines) {
            violations.push({
                type: 'FILE_TOO_LARGE',
                line: 0,
                message: `File has ${lineCount} lines (max: ${this.qualityConfig.rules.max_file_lines})`,
                suggestion: 'Split file into smaller modules',
                severity: 'error'
            });
        }

        // Language-specific analysis
        if (extension === '.py') {
            const pythonViolations = await this.analyzePythonFile(filePath, content, lines);
            violations.push(...pythonViolations);
        } else if (['.js', '.ts'].includes(extension)) {
            const jsViolations = await this.analyzeJavaScriptFile(filePath, content, lines);
            violations.push(...jsViolations);
        }

        return violations;
    }

    async analyzePythonFile(filePath, content, lines) {
        const violations = [];

        // Function analysis
        const functionRegex = /^(\s*)def\s+(\w+)\s*\(/gm;
        let match;
        const functions = [];

        while ((match = functionRegex.exec(content)) !== null) {
            const functionName = match[2];
            const startLine = content.substring(0, match.index).split('\n').length;
            const indentation = match[1].length;

            functions.push({
                name: functionName,
                startLine,
                indentation,
                startIndex: match.index
            });
        }

        // Analyze each function
        for (let i = 0; i < functions.length; i++) {
            const func = functions[i];
            const nextFunc = functions[i + 1];

            const functionEnd = nextFunc ? nextFunc.startIndex : content.length;
            const functionContent = content.substring(func.startIndex, functionEnd);
            const functionLines = functionContent.split('\n');

            // Check function length
            const actualLines = functionLines.filter(line =>
                line.trim() && !line.trim().startsWith('#')
            ).length;

            if (actualLines > this.qualityConfig.rules.max_function_lines) {
                violations.push({
                    type: 'FUNCTION_TOO_LONG',
                    line: func.startLine,
                    message: `Function '${func.name}' has ${actualLines} lines (max: ${this.qualityConfig.rules.max_function_lines})`,
                    suggestion: 'Break function into smaller functions',
                    severity: 'error',
                    functionName: func.name
                });
            }

            // Check for documentation
            if (this.qualityConfig.rules.require_docstrings) {
                const hasDocstring = functionContent.includes('"""') || functionContent.includes("'''");
                if (!hasDocstring) {
                    violations.push({
                        type: 'MISSING_DOCUMENTATION',
                        line: func.startLine,
                        message: `Function '${func.name}' lacks documentation`,
                        suggestion: 'Add docstring with description, parameters, and return value',
                        severity: 'warning',
                        functionName: func.name
                    });
                }
            }

            // Simple complexity check (count control structures)
            const complexityIndicators = [
                /\bif\b/g, /\bwhile\b/g, /\bfor\b/g, /\btry\b/g, /\bexcept\b/g,
                /\band\b/g, /\bor\b/g
            ];

            let complexity = 1; // Base complexity
            complexityIndicators.forEach(regex => {
                const matches = functionContent.match(regex) || [];
                complexity += matches.length;
            });

            if (complexity > this.qualityConfig.rules.max_complexity) {
                violations.push({
                    type: 'HIGH_COMPLEXITY',
                    line: func.startLine,
                    message: `Function '${func.name}' has complexity ${complexity} (max: ${this.qualityConfig.rules.max_complexity})`,
                    suggestion: 'Simplify function logic or break into smaller functions',
                    severity: 'error',
                    functionName: func.name
                });
            }
        }

        // Check for tests if required
        if (this.qualityConfig.rules.require_tests) {
            const missingTests = await this.checkForTests(filePath, functions);
            violations.push(...missingTests);
        }

        return violations;
    }

    async analyzeJavaScriptFile(filePath, content, lines) {
        const violations = [];

        // Function analysis (simple regex-based)
        const functionRegex = /(function\s+\w+|const\s+\w+\s*=\s*(?:async\s+)?\([^)]*\)\s*=>|const\s+\w+\s*=\s*(?:async\s+)?function)/gm;
        let match;

        while ((match = functionRegex.exec(content)) !== null) {
            const startLine = content.substring(0, match.index).split('\n').length;
            const functionContent = this.extractJSFunctionContent(content, match.index);

            if (functionContent) {
                const functionLines = functionContent.split('\n').filter(line =>
                    line.trim() && !line.trim().startsWith('//')
                ).length;

                if (functionLines > this.qualityConfig.rules.max_function_lines) {
                    violations.push({
                        type: 'FUNCTION_TOO_LONG',
                        line: startLine,
                        message: `Function has ${functionLines} lines (max: ${this.qualityConfig.rules.max_function_lines})`,
                        suggestion: 'Break function into smaller functions',
                        severity: 'error'
                    });
                }
            }
        }

        return violations;
    }

    extractJSFunctionContent(content, startIndex) {
        let braceCount = 0;
        let inFunction = false;
        let result = '';

        for (let i = startIndex; i < content.length; i++) {
            const char = content[i];
            result += char;

            if (char === '{') {
                braceCount++;
                inFunction = true;
            } else if (char === '}') {
                braceCount--;
                if (inFunction && braceCount === 0) {
                    break;
                }
            }
        }

        return result;
    }

    async checkForTests(filePath, functions) {
        const violations = [];
        const fileName = path.basename(filePath, path.extname(filePath));

        // Common test file patterns
        const testPatterns = [
            `tests/test_${fileName}.py`,
            `test_${fileName}.py`,
            `${fileName}_test.py`,
            `tests/${fileName}_test.py`
        ];

        for (const func of functions) {
            let hasTest = false;

            for (const testPattern of testPatterns) {
                const testPath = path.resolve(path.dirname(filePath), testPattern);

                if (fs.existsSync(testPath)) {
                    const testContent = fs.readFileSync(testPath, 'utf8');
                    const testFunctionPattern = new RegExp(`def\\s+test_${func.name}`, 'g');

                    if (testFunctionPattern.test(testContent)) {
                        hasTest = true;
                        break;
                    }
                }
            }

            if (!hasTest) {
                violations.push({
                    type: 'MISSING_TEST',
                    line: func.startLine,
                    message: `Function '${func.name}' has no unit test`,
                    suggestion: `Create test_${func.name}() in tests/test_${fileName}.py`,
                    severity: 'warning',
                    functionName: func.name
                });
            }
        }

        return violations;
    }

    handleViolations(filePath, violations, changeType) {
        const previousCount = this.violationCounts.get(filePath) || 0;
        const currentCount = violations.length;

        this.violationCounts.set(filePath, currentCount);
        this.lastViolations.set(filePath, violations);

        // Determine change status
        let status = '✅';
        let statusMessage = 'No issues';

        if (currentCount > 0) {
            status = currentCount > previousCount ? '⬆️' :
                     currentCount < previousCount ? '⬇️' : '🔄';
            statusMessage = `${currentCount} violation${currentCount > 1 ? 's' : ''}`;
        }

        // Log summary
        this.log('info', `${status} ${path.relative(process.cwd(), filePath)}: ${statusMessage}`);

        // Detailed violations
        if (violations.length > 0 && this.config.logLevel === 'verbose') {
            violations.forEach(violation => {
                const icon = violation.severity === 'error' ? '❌' : '⚠️';
                this.log('info', `  ${icon} Line ${violation.line}: ${violation.message}`);
                this.log('info', `     💡 ${violation.suggestion}`);
            });
        }

        // Desktop notification for new violations
        if (this.config.enableNotifications && violations.length > 0) {
            this.sendNotification(filePath, violations);
        }

        // Generate real-time report
        this.generateRealTimeReport();
    }

    sendNotification(filePath, violations) {
        const fileName = path.basename(filePath);
        const errorCount = violations.filter(v => v.severity === 'error').length;
        const warningCount = violations.filter(v => v.severity === 'warning').length;

        let title = '🛡️ Quality Guard';
        let message = `${fileName}: `;

        if (errorCount > 0) {
            message += `${errorCount} error${errorCount > 1 ? 's' : ''}`;
        }
        if (warningCount > 0) {
            if (errorCount > 0) message += ', ';
            message += `${warningCount} warning${warningCount > 1 ? 's' : ''}`;
        }

        notifier.notify({
            title,
            message,
            icon: path.join(__dirname, 'assets', 'quality-guard-icon.png'),
            sound: false,
            timeout: 5
        });
    }

    generateRealTimeReport() {
        const totalFiles = this.violationCounts.size;
        const filesWithViolations = Array.from(this.violationCounts.values()).filter(count => count > 0).length;
        const totalViolations = Array.from(this.violationCounts.values()).reduce((sum, count) => sum + count, 0);

        // Update status file for other tools
        const statusReport = {
            timestamp: new Date().toISOString(),
            summary: {
                totalFiles,
                filesWithViolations,
                totalViolations,
                qualityScore: Math.max(0, 100 - (totalViolations * 2))
            },
            files: Array.from(this.lastViolations.entries()).map(([file, violations]) => ({
                path: path.relative(process.cwd(), file),
                violationCount: violations.length,
                violations: violations.map(v => ({
                    type: v.type,
                    line: v.line,
                    severity: v.severity,
                    message: v.message
                }))
            }))
        };

        fs.writeFileSync('.quality-status.json', JSON.stringify(statusReport, null, 2));
    }

    getQualityStatus() {
        const totalViolations = Array.from(this.violationCounts.values()).reduce((sum, count) => sum + count, 0);
        const filesWithIssues = Array.from(this.violationCounts.values()).filter(count => count > 0).length;

        return {
            totalViolations,
            filesWithIssues,
            qualityScore: Math.max(0, 100 - (totalViolations * 2))
        };
    }

    log(level, message) {
        const timestamp = new Date().toISOString().substring(11, 19);
        const levels = { error: '❌', warn: '⚠️', info: 'ℹ️', verbose: '🔍' };
        const icon = levels[level] || 'ℹ️';

        if (level === 'verbose' && this.config.logLevel !== 'verbose') {
            return;
        }

        console.log(`${timestamp} ${icon} ${message}`);
    }

    cleanup() {
        if (this.watcher) {
            this.watcher.close();
        }

        // Clear all debounce timers
        this.debounceTimers.forEach(timer => clearTimeout(timer));
        this.debounceTimers.clear();
    }
}

// Command line interface
if (require.main === module) {
    const args = process.argv.slice(2);
    const config = {};

    // Parse command line arguments
    for (let i = 0; i < args.length; i += 2) {
        const key = args[i].replace(/^--/, '');
        const value = args[i + 1];

        switch (key) {
            case 'watch':
                config.watchPaths = value.split(',');
                break;
            case 'config':
                config.qualityConfigPath = value;
                break;
            case 'notifications':
                config.enableNotifications = value === 'true';
                break;
            case 'verbose':
                config.logLevel = 'verbose';
                i--; // No value for this flag
                break;
            case 'debounce':
                config.debounceMs = parseInt(value, 10);
                break;
        }
    }

    const watcher = new QualityWatcher(config);

    // Graceful shutdown
    process.on('uncaughtException', (error) => {
        console.error('❌ Uncaught exception:', error);
        watcher.cleanup();
        process.exit(1);
    });
}

module.exports = QualityWatcher;