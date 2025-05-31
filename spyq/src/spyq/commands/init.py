"""
Initialize a new SPYQ configuration in the current directory.
"""
import json
from pathlib import Path
from typing import Tuple, List, Union

def create_default_config() -> dict:
    """Create a default configuration dictionary."""
    return {
        "version": "1.0.0",
        "description": "SPYQ Quality Guard Configuration",
        "rules": {
            "require_tests": True,
            "require_docstrings": True,
            "require_architecture_docs": False,
            "max_file_lines": 300,
            "max_function_lines": 50,
            "max_function_params": 4,
            "max_nesting_depth": 4,
            "max_complexity": 10,
            "max_class_methods": 15
        },
        "enforcement": {
            "level": "error",
            "strict_mode": True,
            "block_execution": True
        },
        "patterns": {
            "test_patterns": [
                "tests/test_*.py",
                "test_*.py",
                "*_test.py",
                "tests/**/test_*.py"
            ],
            "doc_files": [
                "README.md",
                "docs/README.md",
                "docs/API.md",
                "docs/architecture.md"
            ],
            "forbidden_patterns": [
                "eval(",
                "exec(",
                "globals()",
                "__import__",
                "input("
            ]
        },
        "auto_generation": {
            "enabled": True,
            "tests": True,
            "docs": True,
            "templates_dir": "templates/"
        },
        "exceptions": {
            "missing_test": "MissingTestException",
            "missing_docs": "MissingDocumentationException",
            "invalid_structure": "InvalidStructureException"
        }
    }

def create_eslint_config() -> str:
    """Create default ESLint configuration."""
    return """module.exports = {
  root: true,
  env: {
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['@typescript-eslint', 'prettier'],
  rules: {
    'prettier/prettier': 'error',
    'no-console': 'warn',
    'no-debugger': 'warn',
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': ['error'],
    'no-var': 'error',
    'prefer-const': 'error',
    'no-extra-semi': 'error',
    'semi': ['error', 'always'],
  },
};
"""

def create_prettier_config() -> dict:
    """Create default Prettier configuration."""
    return {
        "semi": True,
        "singleQuote": True,
        "tabWidth": 2,
        "printWidth": 100,
        "trailingComma": "all",
        "bracketSpacing": True,
        "arrowParens": "always"
    }

def create_sonar_properties() -> str:
    """Create default SonarQube properties."""
    return """# Required metadata
sonar.projectKey=my_project
sonar.projectName=My Project
sonar.projectVersion=1.0

# Comma-separated paths to directories with sources (required)
sonar.sources=.

# Language
sonar.language=py

# Encoding of the source files
sonar.sourceEncoding=UTF-8

# Exclusions
sonar.exclusions=**/node_modules/**,**/*.min.js,**/bower_components/**,**/jspm_packages/**,**/htmlcov/**,**/tests/**,**/test_*.py

# Python specific
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.xunit.reportPath=nosetests.xml
"""

def init_config(force: bool = False) -> Tuple[bool, Union[List[str], str]]:
    """
    Initialize SPYQ configuration in the current directory.
    
    Args:
        force: If True, overwrite existing files
        
    Returns:
        Tuple[bool, Union[List[str], str]]: (success, result) where result is either a list of created files or an error message
    """
    config_dir = Path(".spyq")
    config_file = config_dir / "config.json"
    eslint_file = config_dir / ".eslintrc.advanced.js"
    prettier_file = config_dir / ".prettierrc"
    sonar_file = config_dir / "sonar-project.properties"
    
    # Create .spyq directory if it doesn't exist
    config_dir.mkdir(exist_ok=True)
    
    # Create config files if they don't exist or if force is True
    files_created = []
    
    try:
        # config.json
        if force or not config_file.exists():
            with open(config_file, 'w') as f:
                json.dump(create_default_config(), f, indent=2)
            files_created.append(str(config_file))
            
        # .eslintrc.advanced.js
        if force or not eslint_file.exists():
            with open(eslint_file, 'w') as f:
                f.write(create_eslint_config())
            files_created.append(str(eslint_file))
            
        # .prettierrc
        if force or not prettier_file.exists():
            with open(prettier_file, 'w') as f:
                json.dump(create_prettier_config(), f, indent=2)
            files_created.append(str(prettier_file))
            
        # sonar-project.properties
        if force or not sonar_file.exists():
            with open(sonar_file, 'w') as f:
                f.write(create_sonar_properties())
            files_created.append(str(sonar_file))
            
        return True, files_created
        
    except Exception as e:
        return False, str(e)

def init_command(force: bool = False) -> None:
    """
    Initialize SPYQ configuration in the current directory.
    
    Args:
        force: If True, overwrite existing files
    """
    success, result = init_config(force=force)
    
    if success:
        if result:  # Files were created
            print("✅ SPYQ configuration initialized successfully!")
            print("\nCreated files:")
            for file in result:
                print(f"  - {file}")
            print("\nNext steps:")
            print("  1. Review the configuration in .spyq/config.json")
            print("  2. Run 'spyq setup' to set up the quality guard")
        else:
            print("✅ SPYQ configuration already exists. Use --force to overwrite.")
    else:
        print(f"❌ Error initializing SPYQ: {result}")
        exit(1)
