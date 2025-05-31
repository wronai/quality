# File: spyq/examples/python_with_spyq.py
import sys
import runpy
from pathlib import Path
from spyq.validator import validate_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python_with_spyq.py <script.py> [args...]")
        sys.exit(1)

    script_path = Path(sys.argv[1]).resolve()

    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)

    # Validate the script
    print(f"🔍 Validating {script_path} with SPYQ...")
    issues = validate_file(script_path)

    if issues:
        error_count = sum(1 for i in issues if i.get('severity') == 'error')
        warning_count = sum(1 for i in issues if i.get('severity') == 'warning')

        print("\n⚠️  SPYQ Validation Issues:")
        for issue in issues:
            line = issue.get('line', 0)
            message = issue.get('message', 'Unknown issue')
            severity = issue.get('severity', 'error').upper()
            print(f"  Line {line}: {severity}: {message}")

        print(f"\nFound {error_count} errors and {warning_count} warnings")

        if error_count > 0:
            print("\n❌ Execution aborted due to validation errors")
            sys.exit(1)
        else:
            print("\n⚠️  Warnings found but continuing execution...\n")

    # Run the original script
    sys.argv = sys.argv[1:]  # Remove our script name from args
    runpy.run_path(str(script_path), run_name="__main__")


if __name__ == "__main__":
    main()