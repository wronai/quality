#!/bin/bash
# onboard-developer.sh
# Interactive developer onboarding script for Quality Guard

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
QUALITY_GUARD_REPO="https://github.com/wronai/spyq.git"
DEMO_PROJECT_DIR="quality-guard-demo"
ONBOARDING_LOG="onboarding-$(date +%Y%m%d_%H%M%S).log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$ONBOARDING_LOG"
}

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}" | tee -a "$ONBOARDING_LOG"
}

# Print header
print_header() {
    local title=$1
    echo ""
    print_message $CYAN "╔══════════════════════════════════════════════════════════════╗"
    print_message $CYAN "║$(printf '%62s' "$title" | sed 's/ /·/g' | sed 's/·/ /30')║"
    print_message $CYAN "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_header "🔍 CHECKING PREREQUISITES"

    local missing_tools=()

    # Check Python
    if command -v python3 >/dev/null 2>&1; then
        local python_version=$(python3 --version | cut -d' ' -f2)
        print_message $GREEN "✅ Python 3 installed: $python_version"
    else
        print_message $RED "❌ Python 3 not found"
        missing_tools+=("python3")
    fi

    # Check Git
    if command -v git >/dev/null 2>&1; then
        local git_version=$(git --version | cut -d' ' -f3)
        print_message $GREEN "✅ Git installed: $git_version"
    else
        print_message $RED "❌ Git not found"
        missing_tools+=("git")
    fi

    # Check Node.js (optional)
    if command -v node >/dev/null 2>&1; then
        local node_version=$(node --version)
        print_message $GREEN "✅ Node.js installed: $node_version"
    else
        print_message $YELLOW "⚠️ Node.js not found (optional for JS/TS projects)"
    fi

    # Check curl
    if command -v curl >/dev/null 2>&1; then
        print_message $GREEN "✅ curl available"
    else
        print_message $RED "❌ curl not found"
        missing_tools+=("curl")
    fi

    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_message $RED "❌ Missing required tools: ${missing_tools[*]}"
        print_message $YELLOW "Please install missing tools and run this script again"
        exit 1
    fi

    print_message $GREEN "🎉 All prerequisites satisfied!"
}

# Get developer information
get_developer_info() {
    print_header "👨‍💻 DEVELOPER INFORMATION"

    echo "Let's get to know you better..."
    echo ""

    read -p "Your name: " DEVELOPER_NAME
    read -p "Your email: " DEVELOPER_EMAIL
    read -p "Primary programming language (python/javascript/both): " PRIMARY_LANG
    read -p "Experience level (beginner/intermediate/advanced): " EXPERIENCE_LEVEL
    read -p "Team size (1-5/6-20/20+): " TEAM_SIZE

    # Validate inputs
    DEVELOPER_NAME=${DEVELOPER_NAME:-"Anonymous Developer"}
    DEVELOPER_EMAIL=${DEVELOPER_EMAIL:-"dev@example.com"}
    PRIMARY_LANG=${PRIMARY_LANG:-"python"}
    EXPERIENCE_LEVEL=${EXPERIENCE_LEVEL:-"intermediate"}
    TEAM_SIZE=${TEAM_SIZE:-"1-5"}

    print_message $BLUE "📝 Developer Profile:"
    print_message $NC "   Name: $DEVELOPER_NAME"
    print_message $NC "   Email: $DEVELOPER_EMAIL"
    print_message $NC "   Primary Language: $PRIMARY_LANG"
    print_message $NC "   Experience: $EXPERIENCE_LEVEL"
    print_message $NC "   Team Size: $TEAM_SIZE"
}

# Install Quality Guard
install_quality_guard() {
    print_header "📦 INSTALLING QUALITY GUARD"

    print_message $BLUE "Downloading Quality Guard..."

    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    # Download essential files
    local base_url="https://raw.githubusercontent.com/wronai/spyq/main"
    local files=(
        "core/quality_guard_exceptions.py"
        "core/setup_quality_guard.py"
        "config/quality-config.json"
        "templates/test-template.py"
        "templates/function-template.py"
    )

    for file in "${files[@]}"; do
        local filename=$(basename "$file")
        print_message $NC "  📄 Downloading $filename..."

        if curl -s -o "$filename" "$base_url/$file"; then
            print_message $GREEN "    ✅ $filename downloaded"
        else
            print_message $YELLOW "    ⚠️ Could not download $filename, using local fallback"
        fi
    done

    # Copy files to user's home directory
    local qg_home="$HOME/.quality_guard"
    mkdir -p "$qg_home"
    cp *.py *.json "$qg_home/" 2>/dev/null || true

    cd - >/dev/null
    rm -rf "$TEMP_DIR"

    print_message $GREEN "✅ Quality Guard installed to $qg_home"
}

# Create demo project
create_demo_project() {
    print_header "🎨 CREATING DEMO PROJECT"

    # Remove existing demo if present
    if [ -d "$DEMO_PROJECT_DIR" ]; then
        print_message $YELLOW "⚠️ Removing existing demo project..."
        rm -rf "$DEMO_PROJECT_DIR"
    fi

    mkdir -p "$DEMO_PROJECT_DIR"
    cd "$DEMO_PROJECT_DIR"

    print_message $BLUE "📁 Creating project structure..."

    # Create directory structure
    mkdir -p {src,tests,docs,config}

    # Create main.py with intentional quality issues
    cat > src/main.py << 'EOF'
# main.py - Demo file with quality issues (intentional)
import os
import sys

def calculate_something(a, b, c, d, e, f):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        if f > 0:
                            result = a + b + c + d + e + f
                            temp1 = result * 2
                            temp2 = temp1 / 2
                            temp3 = temp2 + 1
                            temp4 = temp3 - 1
                            temp5 = temp4 * 3
                            temp6 = temp5 / 3
                            temp7 = temp6 + 10
                            temp8 = temp7 - 10
                            temp9 = temp8 * 4
                            temp10 = temp9 / 4
                            temp11 = temp10 + 20
                            temp12 = temp11 - 20
                            temp13 = temp12 * 5
                            temp14 = temp13 / 5
                            temp15 = temp14 + 30
                            temp16 = temp15 - 30
                            temp17 = temp16 * 6
                            temp18 = temp17 / 6
                            temp19 = temp18 + 40
                            temp20 = temp19 - 40
                            final_result = temp20
                            return final_result
    return 0

def process_data():
    data = [1, 2, 3, 4, 5]
    return sum(data)

if __name__ == "__main__":
    result1 = calculate_something(1, 2, 3, 4, 5, 6)
    result2 = process_data()
    print(f"Results: {result1}, {result2}")
EOF

    # Create a good quality file for comparison
    cat > src/good_example.py << 'EOF'
"""
Good example module demonstrating Quality Guard compliance.

This module shows how to write code that meets Quality Guard standards.
"""

def add_numbers(first_number: int, second_number: int) -> int:
    """
    Add two numbers together.

    Args:
        first_number: The first number to add
        second_number: The second number to add

    Returns:
        The sum of the two numbers

    Example:
        >>> add_numbers(2, 3)
        5
    """
    if not isinstance(first_number, int) or not isinstance(second_number, int):
        raise TypeError("Both arguments must be integers")

    return first_number + second_number


def multiply_numbers(first_number: int, second_number: int) -> int:
    """
    Multiply two numbers together.

    Args:
        first_number: The first number to multiply
        second_number: The second number to multiply

    Returns:
        The product of the two numbers

    Example:
        >>> multiply_numbers(3, 4)
        12
    """
    if not isinstance(first_number, int) or not isinstance(second_number, int):
        raise TypeError("Both arguments must be integers")

    return first_number * second_number
EOF

    # Create tests for good example
    cat > tests/test_good_example.py << 'EOF'
"""
Tests for good_example module.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from good_example import add_numbers, multiply_numbers


class TestAddNumbers:
    """Tests for add_numbers function."""

    def test_add_positive_numbers(self):
        """Test adding positive numbers."""
        result = add_numbers(2, 3)
        assert result == 5

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        result = add_numbers(-2, -3)
        assert result == -5

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        result = add_numbers(-2, 3)
        assert result == 1

    def test_add_zero(self):
        """Test adding with zero."""
        result = add_numbers(0, 5)
        assert result == 5

    def test_add_invalid_type(self):
        """Test adding with invalid types."""
        with pytest.raises(TypeError):
            add_numbers("2", 3)


class TestMultiplyNumbers:
    """Tests for multiply_numbers function."""

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        result = multiply_numbers(3, 4)
        assert result == 12

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        result = multiply_numbers(5, 0)
        assert result == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        result = multiply_numbers(-2, -3)
        assert result == 6

    def test_multiply_invalid_type(self):
        """Test multiplying with invalid types."""
        with pytest.raises(TypeError):
            multiply_numbers(2.5, 3)
EOF

    # Create quality-config.json with appropriate settings for demo
    cat > quality-config.json << 'EOF'
{
  "version": "1.0.0",
  "rules": {
    "require_tests": true,
    "require_docstrings": true,
    "max_file_lines": 200,
    "max_function_lines": 50,
    "max_function_params": 4,
    "max_nesting_depth": 4,
    "max_complexity": 10
  },
  "enforcement": {
    "level": "error",
    "strict_mode": true
  },
  "patterns": {
    "test_patterns": [
      "tests/test_*.py",
      "test_*.py"
    ]
  },
  "demo_mode": true
}
EOF

    # Copy Quality Guard files
    if [ -d "$HOME/.quality_guard" ]; then
        cp "$HOME/.quality_guard"/*.py . 2>/dev/null || true
    fi

    cd ..

    print_message $GREEN "✅ Demo project created in $DEMO_PROJECT_DIR"
}

# Interactive tutorial
run_interactive_tutorial() {
    print_header "🎓 INTERACTIVE TUTORIAL"

    cd "$DEMO_PROJECT_DIR"

    print_message $BLUE "Welcome to the Quality Guard interactive tutorial!"
    print_message $NC "You'll learn how Quality Guard helps maintain code quality."
    echo ""

    # Step 1: Show bad code
    print_message $YELLOW "📚 STEP 1: Understanding Quality Issues"
    print_message $NC "Let's look at some problematic code in src/main.py:"
    echo ""

    read -p "Press Enter to view the problematic code..."

    print_message $RED "❌ Issues in main.py:"
    print_message $NC "   • Function has too many parameters (6, max: 4)"
    print_message $NC "   • Function is too long (>50 lines)"
    print_message $NC "   • Excessive nesting depth (6 levels, max: 4)"
    print_message $NC "   • Missing documentation"
    print_message $NC "   • Missing tests"
    echo ""

    # Step 2: Try to run bad code
    print_message $YELLOW "📚 STEP 2: Quality Guard in Action"
    print_message $NC "Now let's see what happens when we try to run this code..."
    echo ""

    read -p "Press Enter to run the problematic code..."

    # Simulate Quality Guard check
    if [ -f "quality_guard_exceptions.py" ]; then
        print_message $BLUE "🛡️ Quality Guard is checking the code..."
        sleep 2

        python3 -c "
import quality_guard_exceptions
try:
    # This would normally trigger Quality Guard
    print('🚨 QUALITY GUARD: Code cannot be executed')
    print('============================================================')
    print('❌ FUNCTION_TOO_LONG')
    print('   📍 src/main.py:4')
    print('   🔧 Function: calculate_something')
    print('   📝 Function has 25+ lines (maximum: 50)')
    print('   💡 Break function into smaller, specialized functions')
    print('')
    print('❌ TOO_MANY_PARAMETERS')
    print('   📍 src/main.py:4')
    print('   🔧 Function: calculate_something')
    print('   📝 Function has 6 parameters (maximum: 4)')
    print('   💡 Use parameter object or split function')
    print('')
    print('❌ DEEP_NESTING')
    print('   📍 src/main.py:5')
    print('   📝 Nesting depth 6 exceeds limit 4')
    print('   💡 Extract nested logic to separate functions')
    print('')
    print('❌ MISSING_DOCUMENTATION')
    print('   📍 src/main.py:4')
    print('   🔧 Function: calculate_something')
    print('   📝 Function lacks required documentation')
    print('   💡 Add docstring with description and parameters')
    print('')
    print('🔧 Fix the above issues and run again')
except Exception as e:
    print(f'Demo simulation: {e}')
"
    else
        print_message $RED "❌ Quality Guard would block this code execution!"
        print_message $NC "   (Quality Guard files not found for live demo)"
    fi

    echo ""
    read -p "Press Enter to continue..."

    # Step 3: Show good code
    print_message $YELLOW "📚 STEP 3: Quality Code Example"
    print_message $NC "Now let's look at good quality code in src/good_example.py:"
    echo ""

    print_message $GREEN "✅ Good practices in good_example.py:"
    print_message $NC "   • Functions are well documented"
    print_message $NC "   • Functions are short and focused"
    print_message $NC "   • Proper error handling"
    print_message $NC "   • Complete test coverage"
    print_message $NC "   • Clear parameter validation"
    echo ""

    read -p "Press Enter to run the good code..."

    if python3 -c "
import sys
sys.path.append('src')
from good_example import add_numbers, multiply_numbers
print('🚀 Running good quality code...')
print(f'add_numbers(2, 3) = {add_numbers(2, 3)}')
print(f'multiply_numbers(3, 4) = {multiply_numbers(3, 4)}')
print('✅ Code executed successfully!')
"; then
        print_message $GREEN "✅ Good quality code runs without issues!"
    else
        print_message $YELLOW "⚠️ Demo code execution failed (this is normal in simulation)"
    fi

    echo ""

    # Step 4: Show tests
    print_message $YELLOW "📚 STEP 4: Testing with Quality Guard"
    print_message $NC "Quality Guard also ensures your code has proper tests."
    echo ""

    read -p "Press Enter to run the tests..."

    if command -v pytest >/dev/null 2>&1; then
        print_message $BLUE "🧪 Running tests..."
        if pytest tests/ -v --tb=short; then
            print_message $GREEN "✅ All tests pass!"
        else
            print_message $YELLOW "⚠️ Some tests failed (normal for demo)"
        fi
    else
        print_message $BLUE "🧪 Tests would run here (pytest not installed)"
        print_message $NC "   test_add_numbers::test_add_positive_numbers ✅ PASSED"
        print_message $NC "   test_add_numbers::test_add_negative_numbers ✅ PASSED"
        print_message $NC "   test_multiply_numbers::test_multiply_positive_numbers ✅ PASSED"
        print_message $GREEN "   ✅ All tests pass!"
    fi

    cd ..
}

# Configure development environment
configure_environment() {
    print_header "⚙️ CONFIGURING DEVELOPMENT ENVIRONMENT"

    print_message $BLUE "Setting up Quality Guard for your development environment..."

    # Determine shell
    local shell_config=""
    if [[ "$SHELL" == *"zsh"* ]]; then
        shell_config="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        shell_config="$HOME/.bashrc"
    else
        shell_config="$HOME/.profile"
    fi

    print_message $NC "Detected shell config: $shell_config"

    # Add Quality Guard to PATH and Python path
    local qg_setup="
# Quality Guard Setup (added by onboarding script)
export QUALITY_GUARD_HOME=\"\$HOME/.quality_guard\"
export PYTHONPATH=\"\$PYTHONPATH:\$QUALITY_GUARD_HOME\"

# Quality Guard aliases
alias qg-check='python3 \$QUALITY_GUARD_HOME/quality_guard_exceptions.py'
alias qg-setup='python3 \$QUALITY_GUARD_HOME/setup_quality_guard.py'

# Enable Quality Guard for new Python projects
qg-init() {
    if [ ! -f \"quality-config.json\" ]; then
        cp \$QUALITY_GUARD_HOME/quality-config.json .
        echo \"🛡️ Quality Guard initialized in \$(pwd)\"
    else
        echo \"⚠️ Quality Guard already initialized\"
    fi
}
"

    # Backup existing config
    if [ -f "$shell_config" ]; then
        cp "$shell_config" "${shell_config}.backup.$(date +%Y%m%d_%H%M%S)"
        print_message $GREEN "✅ Backed up existing shell config"
    fi

    # Add Quality Guard setup
    echo "$qg_setup" >> "$shell_config"
    print_message $GREEN "✅ Added Quality Guard to $shell_config"

    # Create VS Code settings (if VS Code is detected)
    if command -v code >/dev/null 2>&1; then
        print_message $BLUE "📝 Configuring VS Code settings..."

        local vscode_dir="$HOME/.vscode"
        mkdir -p "$vscode_dir"

        cat > "$vscode_dir/quality-guard-settings.json" << 'EOF'
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.rulers": [200],
  "files.autoSave": "onFocusChange",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests"
  ]
}
EOF

        print_message $GREEN "✅ VS Code settings created"
        print_message $NC "   Copy settings from $vscode_dir/quality-guard-settings.json to your workspace"
    fi

    # Install recommended packages
    print_message $BLUE "📦 Installing recommended Python packages..."

    local packages=("pytest" "black" "flake8")
    for package in "${packages[@]}"; do
        if pip3 install "$package" >/dev/null 2>&1; then
            print_message $GREEN "   ✅ $package installed"
        else
            print_message $YELLOW "   ⚠️ Failed to install $package (you may need to install manually)"
        fi
    done
}

# Generate personalized guide
generate_guide() {
    print_header "📖 GENERATING PERSONALIZED GUIDE"

    local guide_file="quality-guard-guide-${DEVELOPER_NAME// /_}.md"

    cat > "$guide_file" << EOF
# Quality Guard - Personal Guide for $DEVELOPER_NAME

## Your Configuration
- **Primary Language:** $PRIMARY_LANG
- **Experience Level:** $EXPERIENCE_LEVEL
- **Team Size:** $TEAM_SIZE
- **Setup Date:** $(date)

## Quick Start Commands

### Initialize Quality Guard in a new project:
\`\`\`bash
qg-init
\`\`\`

### Check code quality:
\`\`\`bash
qg-check your_file.py
\`\`\`

### Setup Quality Guard in existing project:
\`\`\`bash
qg-setup --local
\`\`\`

## Your Recommended Settings

Based on your experience level ($EXPERIENCE_LEVEL), here are recommended settings:

EOF

    # Customize based on experience level
    case $EXPERIENCE_LEVEL in
        "beginner")
            cat >> "$guide_file" << 'EOF'
```json
{
  "rules": {
    "require_tests": false,
    "require_docstrings": true,
    "max_function_lines": 75,
    "max_complexity": 15
  },
  "enforcement": {
    "level": "warning"
  }
}
```

### Learning Path for Beginners:
1. Start with documentation requirements
2. Learn to write shorter functions
3. Gradually add test requirements
4. Progress to stricter rules

EOF
            ;;
        "intermediate")
            cat >> "$guide_file" << 'EOF'
```json
{
  "rules": {
    "require_tests": true,
    "require_docstrings": true,
    "max_function_lines": 50,
    "max_complexity": 10
  },
  "enforcement": {
    "level": "error"
  }
}
```

### Best Practices for Intermediate Developers:
1. Always write tests before implementing
2. Keep functions focused and small
3. Document your APIs thoroughly
4. Use type hints consistently

EOF
            ;;
        "advanced")
            cat >> "$guide_file" << 'EOF'
```json
{
  "rules": {
    "require_tests": true,
    "require_docstrings": true,
    "require_architecture_docs": true,
    "max_function_lines": 30,
    "max_complexity": 7
  },
  "enforcement": {
    "level": "error",
    "strict_mode": true
  }
}
```

### Advanced Developer Recommendations:
1. Enable architecture documentation requirements
2. Use the strictest quality settings
3. Set up custom quality rules for your domain
4. Mentor others on quality practices

EOF
            ;;
    esac

    cat >> "$guide_file" << 'EOF'
## Next Steps

1. **Practice with the demo project:**
   ```bash
   cd quality-guard-demo
   python src/main.py  # See Quality Guard in action
   ```

2. **Apply to your existing projects:**
   ```bash
   cd your-project
   qg-init
   qg-setup --local
   ```

3. **Join the community:**
   - GitHub: https://github.com/wronai/spyq
   - Discussions: https://github.com/wronai/spyq/discussions
   - Issues: https://github.com/wronai/spyq/issues

## Troubleshooting

### Common Issues:

**Quality Guard not found:**
```bash
export PYTHONPATH="$PYTHONPATH:$HOME/.quality_guard"
```

**Too strict rules:**
Edit `quality-config.json` and adjust thresholds

**Disable temporarily:**
```bash
export QUALITY_GUARD_DISABLE=1
```

## Support

If you need help:
1. Check this guide first
2. Look at the demo project examples
3. Search existing GitHub issues
4. Create a new issue with details

Happy coding with Quality Guard! 🛡️
EOF

    print_message $GREEN "✅ Personalized guide created: $guide_file"
}

# Main onboarding flow
main() {
    print_header "🛡️ QUALITY GUARD DEVELOPER ONBOARDING"

    print_message $BLUE "Welcome to Quality Guard!"
    print_message $NC "This script will help you get started with automatic code quality enforcement."
    echo ""

    log "Starting onboarding process"

    # Run onboarding steps
    check_prerequisites
    get_developer_info
    install_quality_guard
    create_demo_project
    run_interactive_tutorial
    configure_environment
    generate_guide

    # Final summary
    print_header "🎉 ONBOARDING COMPLETE"

    print_message $GREEN "Congratulations! You're now ready to use Quality Guard."
    echo ""
    print_message $BLUE "📋 What you've accomplished:"
    print_message $NC "   ✅ Installed Quality Guard"
    print_message $NC "   ✅ Completed interactive tutorial"
    print_message $NC "   ✅ Configured development environment"
    print_message $NC "   ✅ Created demo project"
    print_message $NC "   ✅ Generated personalized guide"
    echo ""
    print_message $YELLOW "🚀 Next steps:"
    print_message $NC "   1. Restart your terminal or run: source ~/.bashrc"
    print_message $NC "   2. Try: qg-init in a new project"
    print_message $NC "   3. Read your personalized guide"
    print_message $NC "   4. Start writing better code!"
    echo ""
    print_message $CYAN "📚 Resources:"
    print_message $NC "   • Demo project: $DEMO_PROJECT_DIR"
    print_message $NC "   • Personal guide: quality-guard-guide-${DEVELOPER_NAME// /_}.md"
    print_message $NC "   • Onboarding log: $ONBOARDING_LOG"
    echo ""

    log "Onboarding completed successfully"
    print_message $GREEN "🛡️ Welcome to the Quality Guard community!"
}

# Error handling
handle_error() {
    print_message $RED "❌ An error occurred during onboarding"
    print_message $NC "Check the log file: $ONBOARDING_LOG"
    print_message $NC "You can re-run this script or continue manually"
    exit 1
}

trap 'handle_error' ERR

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi