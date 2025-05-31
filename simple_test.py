#!/usr/bin/env python3
"""Simple test file to verify Quality Guard functionality."""

import sys
import inspect
from quality_guard_activator import wrap_function, wrap_module_functions

# This will activate Quality Guard for all subsequent imports
import quality_guard_activator

# Now let's test if Quality Guard is working
def test_function():
    """A simple test function that should be wrapped by Quality Guard."""
    return "This function is now protected by Quality Guard"

# Explicitly wrap the test function
test_function = wrap_function(test_function)

# Let's verify if our function is wrapped
if __name__ == "__main__":
    print("🛡️ Quality Guard Simple Test")
    print("=" * 30)
    
    # Check if Quality Guard is active
    if hasattr(sys, '_quality_guard_installed') and sys._quality_guard_installed:
        print(f"✅ Quality Guard is active (v{sys._quality_guard_version})")
    else:
        print("❌ Quality Guard is NOT active")
    
    # Check if the function is wrapped
    if hasattr(test_function, '_quality_guard_wrapped'):
        print("✅ test_function is wrapped by Quality Guard")
    else:
        print("❌ test_function is NOT wrapped by Quality Guard")
    
    # Call the function to see if it works
    try:
        result = test_function()
        print(f"\nFunction result: {result}")
    except Exception as e:
        print(f"\n❌ Error calling test_function: {e}")
    
    # Additional debug info
    print("\nDebug Info:")
    print(f"- Python version: {sys.version.split()[0]}")
    print(f"- Module: {__name__}")
    print(f"- Current directory: {os.getcwd()}")
    print(f"- Quality Guard module: {quality_guard_activator.__file__}")
