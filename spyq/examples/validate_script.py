"""
Example script demonstrating SPYQ validation.

This script shows how to use SPYQ to validate Python code quality.
"""

import subprocess
import sys
from pathlib import Path

def validate_script(script_path: str) -> bool:
    """
    Validate a Python script using SPYQ.
    
    Args:
        script_path: Path to the Python script to validate
        
    Returns:
        bool: True if validation passed, False otherwise
    """
    try:
        result = subprocess.run(
            ["spyq", "validate", script_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Validation passed for {script_path}")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Validation failed for {script_path}")
        print("Error:", e.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'spyq' command not found. Make sure SPYQ is installed.")
        return False

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <script_to_validate.py>")
        sys.exit(1)
    
    script_path = Path(sys.argv[1])
    if not script_path.exists():
        print(f"Error: File '{script_path}' not found")
        sys.exit(1)
    
    if not script_path.suffix == '.py':
        print("Error: Only Python (.py) files can be validated")
        sys.exit(1)
    
    success = validate_script(str(script_path))
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
