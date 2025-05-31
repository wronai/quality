"""
SPYQ Quality Check Example

This module demonstrates how to use the SPYQ quality checking system.
It includes examples of both good and bad code patterns that will be caught
by the quality checks.
"""

from typing import List, Dict, Optional
import os
import sys

# Import the quality module
from spyq.quality import enforce_quality, QualityCheckResult

# ===== GOOD EXAMPLES =====

@enforce_quality
def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers to calculate average for
        
    Returns:
        float: The average of the input numbers
        
    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
        
    total = sum(numbers)
    return total / len(numbers)

# ===== BAD EXAMPLES =====

# This function will trigger multiple quality issues
@enforce_quality
def BadlyFormattedFunction(param1, param_two: int, ParamThree: str) -> None:  # noqa: N802
    """Poorly documented function with style issues."""
    # Bad variable naming
    BadVar = 42
    another_bad_var=13  # No spaces around operator
    
    # Overly complex expression
    result = (BadVar * another_bad_var + len(ParamThree) - param1) / param_two if param_two != 0 else 0
    
    # Unused variable
    unused = "This variable is never used"
    
    # Print statement in production code
    print(f"Result: {result}")
    
    # Too many blank lines


    return result

# This class will trigger quality issues
class BadClassExample:
    """Class with quality issues."""
    
    def __init__(self, name: str):
        self.name = name
    
    def BadMethodNaming(self):  # noqa: N802
        """Method with bad naming convention."""
        return f"Hello, {self.name}"

def main():
    """Run the example."""
    # Good example usage
    try:
        avg = calculate_average([1, 2, 3, 4, 5])
        print(f"Average: {avg:.2f}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Bad example usage
    BadlyFormattedFunction(1, 2, "test")
    
    # Another bad example
    bad_instance = BadClassExample("Test")
    print(bad_instance.BadMethodNaming())

if __name__ == "__main__":
    main()
