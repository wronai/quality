"""
Command-line interface for SPYQ - Shell Python Quality Guard.

SPYQ ensures code quality by enforcing best practices and running static analysis
before code execution. It integrates with popular tools like ESLint, Prettier, and SonarQube.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from .config import ConfigManager, DEFAULT_CONFIG
from .validator import validate_file, ValidationError
from .importhook import install_import_hook, uninstall_import_hook

# Legacy imports for backward compatibility
from .setup_quality_guard import setup_quality_guard
from .commands.init import init_command

__version__ = "0.2.0"

def create_init_parser(subparsers: argparse._SubParsersAction) -> None:
    """Create the init command parser."""
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new SPYQ configuration",
        description="Create a new SPYQ configuration file with default settings.",
    )
    init_parser.add_argument(
        "--project",
        action="store_true",
        help="Create a project-level configuration file (spyq.json in current directory)",
    )
    init_parser.add_argument(
        "--user",
        action="store_true",
        help="Create a user-level configuration file (~/.config/spyq/config.json)",
    )
    init_parser.add_argument(
        "--path",
        type=str,
        help="Path where to create the configuration file",
    )
    init_parser.set_defaults(func=handle_init)


def create_validate_parser(subparsers: argparse._SubParsersAction) -> None:
    """Create the validate command parser."""
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate Python files",
        description="Validate Python files against SPYQ rules.",
    )
    validate_parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to validate (default: current directory)",
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )
    validate_parser.set_defaults(func=handle_validate)


def create_run_parser(subparsers: argparse._SubParsersAction) -> None:
    """Create the run command parser."""
    run_parser = subparsers.add_parser(
        "run",
        help="Run a Python script with validation",
        description="Run a Python script with SPYQ validation.",
    )
    run_parser.add_argument(
        "script",
        help="Python script to run",
    )
    run_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to the script",
    )
    run_parser.set_defaults(func=handle_run)


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    # First check for version flag
    if "--version" in args or "-v" in args:
        return argparse.Namespace(version=True)
        
    parser = argparse.ArgumentParser(
        description="SPYQ - Shell Python Quality Guard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    # Add version flag
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version information and exit"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add subcommands
    create_init_parser(subparsers)
    create_validate_parser(subparsers)
    create_run_parser(subparsers)
    
    # Add legacy setup command for backward compatibility
    setup_parser = subparsers.add_parser(
        "setup", 
        help="(Legacy) Setup quality guard in a project",
        description="Legacy command. Use 'init' instead."
    )
    setup_parser.add_argument(
        "path",
        nargs="?",
        type=str,
        default=".",
        help="Path to the project directory (default: current directory)"
    )
    setup_parser.set_defaults(func=handle_legacy_setup)
    
    # If no arguments provided, show help
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    
    return parser.parse_args(args)

def handle_init(args: argparse.Namespace) -> int:
    """Handle the init command."""
    config_manager = ConfigManager()
    
    if args.path:
        path = Path(args.path).resolve()
    elif args.project:
        path = Path.cwd() / "spyq.json"
    elif args.user:
        path = Path.home() / ".config" / "spyq" / "config.json"
    else:
        # Default to project config if in a project, otherwise user config
        if (Path.cwd() / "pyproject.toml").exists() or (Path.cwd() / "setup.py").exists():
            path = Path.cwd() / "spyq.json"
        else:
            path = Path.home() / ".config" / "spyq" / "config.json"
    
    try:
        saved_path = config_manager.init_config(path)
        print(f"✅ Created SPYQ configuration at: {saved_path}")
        print("\nDefault configuration:")
        print(json.dumps(DEFAULT_CONFIG, indent=2))
        return 0
    except Exception as e:
        print(f"❌ Error creating configuration: {e}", file=sys.stderr)
        return 1


def handle_validate(args: argparse.Namespace) -> int:
    """Handle the validate command."""
    from .validator import validate_file
    
    paths = [Path(p) for p in args.paths]
    all_issues = []
    
    for path in paths:
        if path.is_dir():
            # Recursively find all Python files in directory
            py_files = list(path.rglob("*.py"))
            for py_file in py_files:
                try:
                    issues = validate_file(py_file)
                    if issues:
                        all_issues.extend([{"file": str(py_file), **i} for i in issues])
                except Exception as e:
                    print(f"❌ Error validating {py_file}: {e}", file=sys.stderr)
        elif path.is_file() and path.suffix == ".py":
            try:
                issues = validate_file(path)
                if issues:
                    all_issues.extend([{"file": str(path), **i} for i in issues])
            except Exception as e:
                print(f"❌ Error validating {path}: {e}", file=sys.stderr)
    
    # Print issues
    for issue in all_issues:
        file_path = issue.get('file', 'unknown')
        line = issue.get('line', 0)
        col = issue.get('col', 0)
        message = issue.get('message', 'Unknown issue')
        severity = issue.get('severity', 'error')
        
        if args.strict and severity == 'warning':
            severity = 'error'
            
        print(f"{file_path}:{line}:{col}: {severity.upper()}: {message}")
    
    # Count issues by severity
    error_count = sum(1 for i in all_issues if i.get('severity') == 'error' or args.strict)
    warning_count = sum(1 for i in all_issues if i.get('severity') == 'warning' and not args.strict)
    
    print(f"\nFound {error_count} errors and {warning_count} warnings")
    
    return 1 if error_count > 0 else 0


def handle_run(args: argparse.Namespace) -> int:
    """Handle the run command."""
    script_path = Path(args.script).resolve()
    
    if not script_path.exists():
        print(f"❌ Error: Script not found: {script_path}", file=sys.stderr)
        return 1
    
    # Validate the script first
    try:
        issues = validate_file(script_path)
    except Exception as e:
        print(f"❌ Error validating {script_path}: {e}", file=sys.stderr)
        return 1
    
    if issues:
        error_count = sum(1 for i in issues if i.get('severity') == 'error')
        warning_count = sum(1 for i in issues if i.get('severity') == 'warning')
        
        print(f"\n🔍 Validation issues in {script_path}:")
        for issue in issues:
            line = issue.get('line', 0)
            col = issue.get('col', 0)
            message = issue.get('message', 'Unknown issue')
            severity = issue.get('severity', 'error')
            print(f"  Line {line}, Column {col}: {severity.upper()}: {message}")
        
        print(f"\nFound {error_count} errors and {warning_count} warnings")
        
        if error_count > 0:
            print("\n❌ Aborting execution due to validation errors.")
            return 1
    
    # Run the script
    import runpy
    
    sys.argv = [script_path.name] + args.args
    
    print(f"\n🚀 Running {script_path}...\n")
    try:
        runpy.run_path(str(script_path), run_name="__main__")
        return 0
    except Exception as e:
        print(f"\n❌ Error running script: {e}", file=sys.stderr)
        return 1


def handle_legacy_setup(args: argparse.Namespace) -> int:
    """Handle the legacy setup command."""
    print("⚠️  The 'setup' command is deprecated. Using 'init' instead.", file=sys.stderr)
    return handle_init(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the SPYQ CLI."""
    if args is None:
        args = sys.argv[1:]
    
    try:
        parsed_args = parse_args(args)
        
        # Handle version flag
        if getattr(parsed_args, 'version', False):
            print(f"SPYQ version {__version__}")
            return 0
            
        # Call the appropriate handler function
        if hasattr(parsed_args, 'func'):
            return parsed_args.func(parsed_args)
            
        # No command provided, show help
        if not args:  # No arguments at all
            print("No command provided. Use 'spyq --help' for usage information.")
        else:
            # There were arguments but no valid command
            print(f"Unknown command: {args[0]}. Use 'spyq --help' for usage information.")
        return 1
            
    except Exception as e:
        print(f"❌ An error occurred: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
