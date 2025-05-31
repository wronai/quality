# 🛠️ Quality Guard Troubleshooting Guide

## Common Issues and Solutions

### 🚨 Installation Issues

#### Problem: `ImportError: No module named 'quality_guard_exceptions'`

**Symptoms:**
```bash
$ python main.py
ImportError: No module named 'quality_guard_exceptions'
```

**Solutions:**

1. **Check Python Path:**
```bash
export PYTHONPATH="$PYTHONPATH:$(pwd)"
python main.py
```

2. **Install as Package:**
```bash
pip install -e /path/to/quality-guard/
```

3. **Copy Files Locally:**
```bash
cp /path/to/quality-guard/core/quality_guard_exceptions.py .
cp /path/to/quality-guard/config/quality-config.json .
```

4. **Verify Installation:**
```bash
python -c "import quality_guard_exceptions; print('✅ Import successful')"
```

---

#### Problem: `FileNotFoundError: quality-config.json`

**Symptoms:**
```bash
⚠️ Nie można załadować quality-config.json, używam domyślnej konfiguracji
```

**Solutions:**

1. **Create Default Config:**
```bash
cat > quality-config.json << 'EOF'
{
  "rules": {
    "require_tests": true,
    "require_docstrings": true,
    "max_function_lines": 50,
    "max_complexity": 10
  }
}
EOF
```

2. **Use Template:**
```bash
cp templates/quality-guard-template.json quality-config.json
```

3. **Generate Config:**
```bash
python setup_quality_guard.py --create-config
```

---

### 🔒 Permission Issues

#### Problem: `Permission denied` when running wrappers

**Symptoms:**
```bash
$ ./python-quality-wrapper.py main.py
bash: ./python-quality-wrapper.py: Permission denied
```

**Solutions:**

1. **Make Executable:**
```bash
chmod +x python-quality-wrapper.py
chmod +x nodejs-quality-wrapper.js
chmod +x npm-quality-wrapper.sh
```

2. **Run with Interpreter:**
```bash
python python-quality-wrapper.py main.py
node nodejs-quality-wrapper.js server.js
bash npm-quality-wrapper.sh start
```

---

### ⚡ Performance Issues

#### Problem: Quality Guard is too slow

**Symptoms:**
- Long delays before code execution
- High CPU usage during validation
- Timeouts in CI/CD

**Solutions:**

1. **Enable Caching:**
```json
{
  "performance": {
    "cache_results": true,
    "cache_duration": 3600
  }
}
```

2. **Reduce Scope:**
```json
{
  "patterns": {
    "include_only": [
      "src/**/*.py",
      "app/**/*.py"
    ],
    "exclude": [
      "tests/**/*",
      "migrations/**/*",
      "venv/**/*"
    ]
  }
}
```

3. **Parallel Processing:**
```json
{
  "performance": {
    "parallel_validation": true,
    "max_workers": 4
  }
}
```

4. **Skip Large Files:**
```json
{
  "rules": {
    "skip_files_larger_than": 1000
  }
}
```

---

### 🎯 Rule Configuration Issues

#### Problem: Rules are too strict/lenient

**Symptoms:**
```bash
❌ Funkcja ma 52 linii (maksimum: 50)
# OR
✅ Code passes but quality seems low
```

**Solutions:**

1. **Adjust Thresholds:**
```json
{
  "rules": {
    "max_function_lines": 75,
    "max_complexity": 15,
    "enforcement_level": "warning"
  }
}
```

2. **Use Presets:**
```bash
# For startups/prototypes
cp templates/presets/startup.json quality-config.json

# For production
cp templates/presets/production.json quality-config.json
```

3. **Gradual Tightening:**
```json
{
  "migration": {
    "current_phase": 1,
    "phases": {
      "1": {"max_function_lines": 100, "require_tests": false},
      "2": {"max_function_lines": 75, "require_tests": false},
      "3": {"max_function_lines": 50, "require_tests": true}
    }
  }
}
```

---

#### Problem: False positives in complexity detection

**Symptoms:**
```bash
❌ Funkcja ma kompleksność 12 (maksimum: 10)
# But function seems simple
```

**Solutions:**

1. **Review Complexity Calculation:**
```python
# Each of these adds +1 to complexity:
if condition:        # +1
    for item in list:    # +1
        if item.valid:   # +1
            while processing:  # +1
                if error and retry:  # +2 (and + or)
```

2. **Adjust Complexity Rules:**
```json
{
  "rules": {
    "max_complexity": 15,
    "complexity_calculation": {
      "count_logical_operators": false,
      "ignore_simple_conditions": true
    }
  }
}
```

3. **Whitelist Specific Functions:**
```json
{
  "exceptions": {
    "complexity": {
      "whitelist_functions": [
        "main",
        "setup_arguments",
        "complex_calculation"
      ]
    }
  }
}
```

---

### 📝 Documentation Issues

#### Problem: Documentation requirements too strict

**Symptoms:**
```bash
❌ Funkcja 'helper' nie ma dokumentacji
# For simple private functions
```

**Solutions:**

1. **Adjust Documentation Rules:**
```json
{
  "rules": {
    "require_docstrings": true,
    "docstring_rules": {
      "require_for_private": false,
      "require_for_short": false,
      "min_function_lines_for_docs": 10
    }
  }
}
```

2. **Use Patterns:**
```json
{
  "patterns": {
    "skip_docstring_for": [
      "_*",
      "test_*",
      "setUp",
      "tearDown"
    ]
  }
}
```

3. **Auto-Generate Docs:**
```json
{
  "auto_generation": {
    "docs": true,
    "doc_template": "minimal"
  }
}
```

---

### 🧪 Testing Issues

#### Problem: Test requirements too strict

**Symptoms:**
```bash
❌ Funkcja 'process_data' nie ma testów jednostkowych
# For every small function
```

**Solutions:**

1. **Adjust Test Requirements:**
```json
{
  "rules": {
    "require_tests": true,
    "test_rules": {
      "require_for_private": false,
      "require_for_simple": false,
      "min_function_lines_for_tests": 20
    }
  }
}
```

2. **Auto-Generate Tests:**
```json
{
  "auto_generation": {
    "tests": true,
    "test_template": "basic",
    "auto_create_missing": true
  }
}
```

3. **Pattern-Based Exclusions:**
```json
{
  "patterns": {
    "skip_tests_for": [
      "test_*",
      "_*",
      "main",
      "setup_*"
    ]
  }
}
```

---

### 🔧 Integration Issues

#### Problem: VS Code integration not working

**Symptoms:**
- No real-time quality feedback
- Settings not applying
- Extensions not loading

**Solutions:**

1. **Install Required Extensions:**
```bash
code --install-extension ms-python.python
code --install-extension esbenp.prettier-vscode
code --install-extension ms-vscode.vscode-eslint
```

2. **Check Workspace Settings:**
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "editor.formatOnSave": true,
  "files.autoSave": "onFocusChange"
}
```

3. **Reload Window:**
```
Ctrl+Shift+P → Developer: Reload Window
```

---

#### Problem: Git hooks not triggering

**Symptoms:**
- Commits go through without quality checks
- Pre-commit hooks not running

**Solutions:**

1. **Verify Husky Installation:**
```bash
npx husky install
npx husky add .husky/pre-commit "python quality_guard_exceptions.py"
```

2. **Check Hook Permissions:**
```bash
chmod +x .husky/pre-commit
chmod +x .husky/pre-push
```

3. **Test Hook Manually:**
```bash
.husky/pre-commit
```

4. **Verify Git Hooks Directory:**
```bash
git config core.hooksPath
# Should show .husky
```

---

### 🐳 Docker Issues

#### Problem: Quality Guard not working in containers

**Symptoms:**
```bash
docker run my-app
⚠️ Quality Guard not found
```

**Solutions:**

1. **Install in Dockerfile:**
```dockerfile
# Add to Dockerfile
COPY quality-guard/ /opt/quality-guard/
RUN pip install -e /opt/quality-guard/
ENV PYTHONPATH="${PYTHONPATH}:/opt/quality-guard/core"
```

2. **Volume Mount for Development:**
```bash
docker run -v $(pwd):/app -v ~/.quality_guard:/root/.quality_guard my-app
```

3. **Environment Variables:**
```dockerfile
ENV QUALITY_GUARD_ENABLE=1
ENV QUALITY_GUARD_CONFIG=/app/quality-config.json
```

---

### 🚀 CI/CD Issues

#### Problem: CI pipeline failing due to Quality Guard

**Symptoms:**
```bash
# GitHub Actions
❌ quality-check failed
Exit code: 1
```

**Solutions:**

1. **Adjust CI Configuration:**
```yaml
# .github/workflows/quality.yml
- name: Quality Check
  run: python quality_guard_exceptions.py --ci-mode
  continue-on-error: true  # Don't fail build on warnings
```

2. **Separate Quality from Build:**
```yaml
jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - name: Quality Check
        run: python quality_guard_exceptions.py
        # Don't block deployment
  
  deploy:
    needs: [quality-check]
    if: always()  # Deploy even if quality check has warnings
```

3. **Use Different Rules for CI:**
```json
{
  "environments": {
    "ci": {
      "enforcement_level": "warning",
      "block_execution": false
    }
  }
}
```

---

### 🏗️ Legacy Code Issues

#### Problem: Too many violations in existing codebase

**Symptoms:**
```bash
❌ Found 1,247 quality violations across 156 files
```

**Solutions:**

1. **Enable Legacy Mode:**
```json
{
  "legacy_mode": {
    "enabled": true,
    "baseline_file": ".quality-baseline.json",
    "only_check_new_code": true
  }
}
```

2. **Gradual Migration:**
```json
{
  "migration": {
    "enabled": true,
    "target_violations_per_sprint": 50,
    "priority_rules": ["require_tests", "max_complexity"]
  }
}
```

3. **Whitelist Existing Files:**
```bash
# Generate baseline
python quality_guard_exceptions.py --generate-baseline

# Only new files will be checked
```

---

### 🔍 Debugging Issues

#### Problem: Need to debug Quality Guard behavior

**Symptoms:**
- Unexpected rule violations
- Rules not triggering as expected
- Need to understand rule logic

**Solutions:**

1. **Enable Debug Mode:**
```json
{
  "debug": {
    "enabled": true,
    "log_level": "verbose",
    "save_ast": true,
    "explain_violations": true
  }
}
```

2. **Use Dry Run Mode:**
```bash
python quality_guard_exceptions.py --dry-run --verbose main.py
```

3. **Generate Debug Report:**
```bash
python quality_guard_exceptions.py --debug-report main.py
# Creates debug-report.html with detailed analysis
```

4. **Check Individual Rules:**
```bash
python quality_guard_exceptions.py --rule=complexity main.py
python quality_guard_exceptions.py --rule=function_length main.py
```

---

## 🚨 Emergency Procedures

### Temporary Disable Quality Guard

```bash
# Environment variable (session-only)
export QUALITY_GUARD_DISABLE=1
python main.py

# Config file (persistent)
echo '{"enforcement": {"level": "disabled"}}' > quality-config.json

# For specific files
echo 'main.py' >> .quality-ignore
```

### Reset Configuration

```bash
# Remove all Quality Guard files
rm quality-config.json
rm quality_guard_exceptions.py
rm -rf .quality_guard/

# Reinstall with defaults
python setup_quality_guard.py --reset --local
```

### Bypass for Critical Hotfix

```bash
# Use original interpreter directly
/usr/bin/python main.py  # Bypasses wrapper

# Or temporarily rename wrapper
mv python-quality-wrapper.py python-quality-wrapper.py.disabled
```

---

## 📞 Getting Help

### Self-Diagnosis

1. **Run Health Check:**
```bash
python quality_guard_exceptions.py --health-check
```

2. **Validate Configuration:**
```bash
python quality_guard_exceptions.py --validate-config quality-config.json
```

3. **Test Installation:**
```bash
python -c "
import quality_guard_exceptions
config = quality_guard_exceptions.QualityConfig()
print('✅ Quality Guard working correctly')
print(f'📊 Config loaded: {len(config.config)} settings')
"
```

### Community Support

1. **Search Issues:** https://github.com/quality-guard/quality-guard/issues
2. **Discussions:** https://github.com/quality-guard/quality-guard/discussions
3. **Documentation:** https://quality-guard.readthedocs.io
4. **Discord:** https://discord.gg/quality-guard

### Reporting Bugs

When reporting issues, include:

```bash
# System information
python --version
pip show quality-guard

# Configuration
cat quality-config.json

# Error output
python quality_guard_exceptions.py main.py 2>&1

# Debug information
python quality_guard_exceptions.py --debug-info
```

---

## 📈 Performance Optimization

### For Large Projects

```json
{
  "performance": {
    "parallel_validation": true,
    "max_workers": 8,
    "cache_results": true,
    "cache_duration": 86400,
    "skip_unchanged_files": true,
    "incremental_analysis": true
  }
}
```

### For CI/CD Optimization

```json
{
  "ci_optimization": {
    "only_changed_files": true,
    "parallel_jobs": true,
    "cache_dependencies": true,
    "fail_fast": true
  }
}
```

### Memory Usage Optimization

```json
{
  "memory": {
    "max_file_size_mb": 10,
    "stream_large_files": true,
    "garbage_collect_frequency": 100
  }
}
```

---

**Remember:** Quality Guard is designed to help, not hinder. If you're fighting the tool, the configuration likely needs adjustment rather than disabling the entire system. 🛡️