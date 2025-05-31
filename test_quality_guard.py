#!/usr/bin/env python3
"""Test script to verify Quality Guard installation."""

import sys

# This import should activate Quality Guard for all subsequent imports
import quality_guard_hook

# Now import something that should be guarded
import math

def test_function():
    """A test function that should be guarded by Quality Guard."""
    return "This function is now protected by Quality Guard"

if __name__ == "__main__":
    print("🛡️ Quality Guard Test Script")
    print("=" * 30)
    
    # Check if Quality Guard is active
    if hasattr(sys, '_quality_guard_installed'):
        print("✅ Quality Guard is active!")
        print(f"Version: {getattr(sys, '_quality_guard_version', 'unknown')}")
    else:
        print("❌ Quality Guard is NOT active")
    
    # Test if our function is guarded
    print("\nTesting function decoration:")
    print(f"test_function is guarded: {hasattr(test_function, '_quality_guard_wrapped')}")
