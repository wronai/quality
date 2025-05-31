# File: spyq/__main__.py
import os
import sys
import runpy
from pathlib import Path
from spyq.validator import validate_file


def validate_script(script_path):
    """Validate a Python script using SPYQ."""
    try:
        issues = validate_file(script_path)
        if not issues:
            return True, []

        errors = [i for i in issues if i.get('severity') == 'error']
        warnings = [i for i in issues if i.get('severity') == 'warning']

        return len(errors) == 0, (errors, warnings)
    except Exception as e:
        return False, [{'message': f"Validation error: {str(e)}", 'severity': 'error', 'line': 0}]


def run_script(script_path, args):
    """Run the specified Python script with arguments."""
    sys.path.insert(0, str(script_path.parent))
    sys.argv = [str(script_path)] + args
    runpy.run_path(str(script_path), run_name="__main__")


def main():
    if len(sys.argv) < 2:
        print("Python", sys.version)
        print("Usage: python -m spyq <script.py> [args...]")
        return

    script_path = Path(sys.argv[1]).resolve()

    if not script_path.exists():
        print(f"Error: Script not found: {script_path}", file=sys.stderr)
        sys.exit(1)

    # Skip validation for internal Python files
    if str(script_path).startswith(sys.prefix):
        run_script(script_path, sys.argv[2:])
        return

    # Validate the script
    is_valid, result = validate_script(script_path)
    errors, warnings = ([], []) if is_valid else result

    # Show warnings
    for warning in warnings:
        print(f"Line {warning.get('line', 0)}: WARNING: {warning.get('message')}")

    # Show errors and abort if any
    if not is_valid:
        print("\n❌ SPYQ Validation Errors:", file=sys.stderr)
        for error in errors:
            print(f"Line {error.get('line', 0)}: ERROR: {error.get('message')}", file=sys.stderr)
        print("\n❌ Execution aborted due to validation errors", file=sys.stderr)
        sys.exit(1)

    # If we got here, run the script
    run_script(script_path, sys.argv[2:])


if __name__ == "__main__":
    main()