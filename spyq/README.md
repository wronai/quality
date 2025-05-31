# 🛡️ SPYQ - Shell Python Quality Guard

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation](https://img.shields.io/badge/docs-📘-brightgreen)](https://github.com/wronai/spyq/tree/main/docs)

SPYQ is a powerful quality guard system that automatically validates Python code before execution. It ensures your code meets quality standards before it runs, preventing technical debt and maintaining high code quality across your projects.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Configuration](#️-configuration)
- [📦 Advanced Usage](#-advanced-usage)
- [🏗️ Project Structure](#️-project-structure)
- [🧪 Development Setup](#-development-setup)
- [🔍 Troubleshooting](#-troubleshooting)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

## ✨ Features

- 🚀 **Automatic Validation** - Validates Python scripts before execution
- 🛡️ **Zero Configuration** - Works out of the box with sensible defaults
- ⚡ **Seamless Integration** - No changes to your workflow needed
- 🔧 **Configurable** - Customize rules via `spyq.json`
- 📊 **Detailed Feedback** - Clear error messages with line numbers
- 🔄 **CI/CD Ready** - Perfect for automated pipelines
- 🐳 **Docker Compatible** - Works in containerized environments
- 🧪 **Tested** - Comprehensive test coverage
- 📝 **Documented** - Clear documentation and examples

## 🚀 Quick Start

### 1. Install SPYQ

```bash
# Install from PyPI
pip install spyq
```

### 2. Run Python Scripts with Validation

```bash
# Run any Python script with automatic validation
python your_script.py

# Or use the explicit command
python -m spyq your_script.py

# Disable validation if needed
SPYQ_DISABLE=1 python your_script.py
```

### 3. Initialize Configuration

```bash
# Create a project-level config
spyq init --project

# Create a user-level config
spyq init --user
```

## ⚙️ Configuration

SPYQ uses a `spyq.json` configuration file to define validation rules. You can create one in your project root or in your home directory (`~/.config/spyq/config.json`).

### Default Configuration

```json
{
    "version": "1.0.0",
    "rules": {
        "max_file_lines": 300,
        "max_function_lines": 50,
        "max_function_params": 4,
        "max_nesting_depth": 4,
        "require_docstrings": true,
        "require_type_hints": true,
        "forbid_global_vars": true,
        "forbid_bare_except": true,
        "forbid_print_statements": false
    }
}
```

### Available Rules

| Rule | Default | Description |
|------|---------|-------------|
| `max_file_lines` | 300 | Maximum lines per file |
| `max_function_lines` | 50 | Maximum lines per function |
| `max_function_params` | 4 | Maximum parameters per function |
| `max_nesting_depth` | 4 | Maximum nesting depth |
| `require_docstrings` | true | Require docstrings |
| `require_type_hints` | true | Require type hints |
| `forbid_global_vars` | true | Forbid global variables |
| `forbid_bare_except` | true | Forbid bare except clauses |
| `forbid_print_statements` | false | Forbid print statements |

## 📦 Advanced Usage

### Manual Validation

```bash
# Validate a single file
spyq validate path/to/script.py

# Validate a directory
spyq validate path/to/directory

# Validate with strict mode (warnings become errors)
spyq validate --strict script.py
```

### Integration with IDEs

Most IDEs allow you to configure the Python interpreter. You can set it to use SPYQ:

1. **VS Code**: Update `python.pythonPath` in settings
2. **PyCharm**: Set up a custom Python interpreter pointing to SPYQ
3. **Vim/Neovim**: Use `:set makeprg=python\ -m\ spyq\ %`

## 🏗️ Project Structure

```
spyq/
├── src/
│   └── spyq/
│       ├── __init__.py
│       ├── __main__.py        # Main entry point
│       ├── validator.py       # Core validation logic
│       ├── config.py          # Configuration management
│       ├── imphook.py         # Import hook for validation
│       └── scripts/
│           └── spyq-python   # Python wrapper script
├── tests/                    # Test files
├── examples/                 # Example scripts
│   ├── bad_script.py        # Example with issues
│   └── good_script.py       # Example following best practices
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## 🧪 Development Setup

### Install from Source

```bash
git clone https://github.com/wronai/quality.git
cd quality/spyq
pip install -e .[dev]  # Install with development dependencies
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=spyq --cov-report=term-missing

# Run specific test file
pytest tests/test_validator.py -v
```

### Code Quality Checks

```bash
# Run linter
flake8

# Format code with black
black .

# Sort imports
isort .

# Type checking
mypy .
```

## 🔍 Troubleshooting

### Common Issues

#### Import Errors
```bash
# If you get import errors, try reinstalling in development mode
pip install -e .
```

#### Permission Issues
```bash
# Make sure scripts are executable
chmod +x spyq/scripts/*
```

### Debugging

```bash
# Enable debug output
SPYQ_DEBUG=1 python -m spyq script.py

# Or set the log level
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve SPYQ
- Inspired by various Python quality tools and linters
- Built with ❤️ by the Wronai team
