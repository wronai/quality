# SPYQ API Reference

## CLI Commands

### `spyq init [--force]`

Initialize SPYQ configuration in the current directory.

```bash
# Initialize with default configuration
spyq init

# Force overwrite existing configuration
spyq init --force
```

**Files Created:**
- `.spyq/config.json` - Main configuration
- `.spyq/.eslintrc.advanced.js` - ESLint rules
- `.spyq/.prettierrc` - Prettier config
- `.spyq/sonar-project.properties` - SonarQube config

### `spyq setup [path] [--force]`

Set up quality guard in a project.

```bash
# Setup in current directory
spyq setup

# Setup in specific directory
spyq setup /path/to/project

# Force overwrite existing setup
spyq setup --force
```

### `spyq version`

Show version information.

```bash
spyq version
# or
spyq --version
```

## Configuration Reference

### `config.json`

```json
{
  "version": "1.0.0",
  "description": "SPYQ Quality Guard Configuration",
  "rules": {
    "require_tests": true,
    "require_docstrings": true,
    "require_architecture_docs": false,
    "max_file_lines": 300,
    "max_function_lines": 50,
    "max_function_params": 4,
    "max_nesting_depth": 4,
    "max_complexity": 10,
    "max_class_methods": 15
  },
  "enforcement": {
    "level": "error",
    "strict_mode": true,
    "block_execution": true
  },
  "patterns": {
    "test_patterns": [
      "tests/test_*.py",
      "test_*.py",
      "*_test.py"
    ],
    "doc_files": [
      "README.md",
      "docs/README.md",
      "docs/API.md"
    ],
    "forbidden_patterns": [
      "eval(",
      "exec(",
      "globals()"
    ]
  },
  "auto_generation": {
    "enabled": true,
    "tests": true,
    "docs": true,
    "templates_dir": "templates/"
  },
  "exceptions": {
    "missing_test": "MissingTestException",
    "missing_docs": "MissingDocumentationException",
    "invalid_structure": "InvalidStructureException"
  }
}
```

## Python API

### `spyq.setup_quality_guard(project_path: Path, force: bool = False) -> None`

Set up quality guard in the specified project directory.

**Parameters:**
- `project_path`: Path to the project directory
- `force`: If True, overwrite existing files

### `spyq.quality_guard.run_checks() -> Dict[str, Any]`

Run all quality checks and return results.

**Returns:**
```python
{
    "passed": bool,
    "checks": List[Dict[str, Any]],
    "score": float,
    "timestamp": str
}
```

## Exit Codes

| Code | Description                     |
|------|---------------------------------|
| 0    | Success                         |
| 1    | General error                   |
| 2    | Configuration error             |
| 3    | Quality check failed            |
| 4    | Invalid arguments               |
| 5    | Unsupported Python version      |

## Error Handling

All errors follow this format:

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable message",
        "details": {}
    }
}
```

Common error codes:
- `config_missing`: Configuration file not found
- `invalid_config`: Invalid configuration
- `quality_check_failed`: Quality check failed
- `unsupported_feature`: Feature not supported
- `permission_denied`: Insufficient permissions
