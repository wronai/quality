#!/bin/bash
# SPYQ - Shell Python Quality Checker
# A comprehensive code quality checking script for Python projects

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PYTHON_FILES=$(find . -type f -name "*.py" | grep -v "venv/" | grep -v "migrations/")
MAX_LINE_LENGTH=88
MAX_COMPLEXITY=10
MIN_TEST_COVERAGE=80

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Print section header
print_section() {
    echo -e "\n${YELLOW}=== $1 ===${NC}"
}

# Run black formatter
run_black() {
    if ! command_exists black; then
        echo -e "${RED}black not found. Install with 'pip install black'${NC}"
        return 1
    fi
    
    print_section "Running Black (code formatter)"
    black --check --diff --line-length $MAX_LINE_LENGTH .
}

# Run isort
run_isort() {
    if ! command_exists isort; then
        echo -e "${RED}isort not found. Install with 'pip install isort'${NC}"
        return 1
    fi
    
    print_section "Running isort (import sorter)"
    isort --check-only --profile black .
}

# Run flake8
run_flake8() {
    if ! command_exists flake8; then
        echo -e "${RED}flake8 not found. Install with 'pip install flake8'${NC}"
        return 1
    fi
    
    print_section "Running flake8 (linter)"
    flake8 --max-line-length=$MAX_LINE_LENGTH --max-complexity=$MAX_COMPLEXITY .
}

# Run mypy
run_mypy() {
    if ! command_exists mypy; then
        echo -e "${RED}mypy not found. Install with 'pip install mypy'${NC}"
        return 1
    fi
    
    print_section "Running mypy (static type checker)"
    mypy .
}

# Run pytest with coverage
run_tests() {
    if ! command_exists pytest; then
        echo -e "${RED}pytest not found. Install with 'pip install pytest pytest-cov'${NC}"
        return 1
    fi
    
    print_section "Running tests with coverage"
    pytest --cov=. --cov-report=term-missing --cov-fail-under=$MIN_TEST_COVERAGE tests/
}

# Run bandit for security checks
run_bandit() {
    if ! command_exists bandit; then
        echo -e "${YELLOW}bandit not found. Install with 'pip install bandit'${NC}"
        return 1
    fi
    
    print_section "Running bandit (security linter)"
    bandit -r .
}

# Run all checks
run_all_checks() {
    local exit_code=0
    
    echo -e "${GREEN}🚀 Starting SPYQ Quality Checks...${NC}"
    
    # Run each check and track the exit code
    for check in run_black run_isort run_flake8 run_mypy run_tests run_bandit; do
        if ! $check; then
            exit_code=1
        fi
    done
    
    if [ $exit_code -eq 0 ]; then
        echo -e "\n${GREEN}✅ All quality checks passed!${NC}"
    else
        echo -e "\n${RED}❌ Some quality checks failed. Please fix the issues above.${NC}"
    fi
    
    return $exit_code
}

# Main execution
main() {
    # If arguments are provided, run specific checks
    if [ $# -gt 0 ]; then
        for arg in "$@"; do
            case $arg in
                black) run_black ;;
                isort) run_isort ;;
                flake8) run_flake8 ;;
                mypy) run_mypy ;;
                test) run_tests ;;
                bandit) run_bandit ;;
                *) echo "Unknown check: $arg" ;;
            esac
        done
    else
        # Run all checks by default
        run_all_checks
    fi
}

# Execute main function with all arguments
main "$@"
