"""
Run validation examples for SPYQ.

This script demonstrates how to use SPYQ to validate Python code quality.
It includes examples of both passing and failing validations.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple, List, Dict, Any

# Add the parent directory to the path so we can import from examples
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_validation(script_path: str) -> Tuple[bool, str]:
    """
    Run validation on a Python script using SPYQ.
    
    Args:
        script_path: Path to the Python script to validate
        
    Returns:
        Tuple of (success, output) where success is a boolean indicating
        if validation passed, and output is the command output.
    """
    try:
        result = subprocess.run(
            ["python", "-m", "flake8", script_path],
            capture_output=True,
            text=True,
            check=False
        )
        return (result.returncode == 0, result.stdout + result.stderr)
    except Exception as e:
        return (False, str(e))

def print_validation_result(script_name: str, success: bool, output: str):
    """Print the validation result in a user-friendly way."""
    print("\n" + "=" * 80)
    print(f"Validating: {script_name}")
    print("=" * 80)
    
    if success:
        print("✅ Validation passed!")
    else:
        print("❌ Validation failed with the following issues:")
        print("-" * 40)
        print(output.strip())
    
    print("\n" + "=" * 80 + "\n")

def create_test_script(filename: str, content: str, temp_dir: Path) -> str:
    """
    Create a test script with the given content in the specified temp directory.
    
    Args:
        filename: Name of the file to create
        content: Content to write to the file
        temp_dir: Temporary directory to create the file in
        
    Returns:
        Path to the created file
        
    Raises:
        OSError: If there's an error creating the file
    """
    try:
        # Ensure the temp directory exists and is writable
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Create the full path for the test script
        path = temp_dir / filename
        
        # Write the file with proper line endings
        with open(path, "w", encoding='utf-8') as f:
            f.write(content.strip() + "\n")
        
        # Set appropriate permissions
        path.chmod(0o644)
        
        return str(path)
        
    except Exception as e:
        print(f"Error creating test script {filename}: {e}", file=sys.stderr)
        raise

def get_test_scripts() -> List[Dict[str, str]]:
    """Return a list of test scripts to validate.
    
    Returns:
        List of dictionaries containing script names and content
    """
    return [
        {
            "name": "valid_script.py",
            "content": """
# This is a valid Python script
def hello():
    print("Hello, World!")


if __name__ == "__main__":
    hello()
"""
        },
        {
            "name": "invalid_indentation.py",
            "content": """
# This script has indentation issues
def hello():
  print("Hello, World!")  # Inconsistent indentation


if __name__ == "__main__":
    hello()
"""
        },
        {
            "name": "missing_whitespace.py",
            "content": """
# This script has whitespace issues
def hello():
    result=1+2  # Missing spaces around operators
    print(f"1+2={result}")


if __name__=="__main__":  # Missing spaces around ==
    hello()
"""
        }
    ]
    
def main():
    """Run the validation examples."""
    # Create a temporary directory for test files
    with tempfile.TemporaryDirectory(prefix="spyq_test_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        
        # Get test scripts and validate each one
        test_scripts = get_test_scripts()
        
        for script in test_scripts:
            script_path = create_test_script(
                script["name"], 
                script["content"],
                temp_dir
            )
            success, output = run_validation(script_path)
            print_validation_result(script_path, success, output)
        
        print("\n🎉 All validation examples completed!")

if __name__ == "__main__":
    main()
