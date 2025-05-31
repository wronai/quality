#!/usr/bin/env python3
"""Simple test file to verify Quality Guard functionality."""

# This will activate Quality Guard for all subsequent imports
import quality_guard_activator

# Now let's test if Quality Guard is working
def test_function():
    """A simple test function that should be wrapped by Quality Guard."""
    return "This function is now protected by Quality Guard"

# Let's verify if our function is wrapped
if __name__ == "__main__":
    print("🛡️ Quality Guard Simple Test")
    print("=" * 30)
    
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
