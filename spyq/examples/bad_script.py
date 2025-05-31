# File: spyq/examples/bad_script.py
"""
Example script with intentional quality issues.
"""

def very_long_function_with_too_many_parameters(one, two, three, four, five):
    # This function is too long and has too many parameters
    result = 0
    for i in range(100):
        result += i
        if result > 50:
            if i % 2 == 0:
                print("Even")
            else:
                print("Odd")
    return result

def missing_whitespace():
    x=5  # Missing spaces around operator
    y=10
    return x+y

if __name__ == "__main__":
    print("This script has quality issues!")
    missing_whitespace()
    very_long_function_with_too_many_parameters(1, 2, 3, 4, 5)