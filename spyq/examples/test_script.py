"""
Example script for SPYQ validation testing.

This script contains intentional style issues to demonstrate SPYQ validation.
"""

def calculate_sum(a, b):
    # Inconsistent indentation
  return a + b  # Bad indentation

def print_greeting(name):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    # Missing space after comma
    result = calculate_sum(1,2)
    print_greeting("World")
    print(f"1 + 2 = {result}")
