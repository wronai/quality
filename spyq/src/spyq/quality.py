"""
SPYQ - Quality Declaration Module

This module provides decorators and utilities for declaring and enforcing
code quality expectations in Python code.
"""
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union
import ast
import inspect
import logging
import re

# Type variable for generic function typing
F = TypeVar('F', bound=Callable[..., Any])

@dataclass
class QualityCheckResult:
    """Result of a quality check."""
    passed: bool
    message: str
    severity: str = "error"  # 'error' or 'warning'
    line: Optional[int] = None
    col: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'passed': self.passed,
            'message': self.message,
            'severity': self.severity,
            'line': self.line,
            'col': self.col
        }

class QualityError(Exception):
    """Raised when a quality check fails."""
    pass

def enforce_quality(func: F) -> F:
    """
    Decorator to enforce quality checks on a function.
    
    Example:
        @enforce_quality
        def example():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Run quality checks before function execution
        source = inspect.getsource(func)
        checks = [
            check_function_length,
            check_docstring,
            check_arg_naming,
            check_variable_naming,
        ]
        
        issues = []
        for check in checks:
            result = check(func, source)
            if not result.passed:
                issues.append(result)
        
        if issues:
            for issue in issues:
                logging.warning(f"Quality issue in {func.__name__}: {issue.message}")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper  # type: ignore

def check_function_length(func: Callable, source: str) -> QualityCheckResult:
    """Check if function is too long."""
    max_lines = 50
    line_count = len(inspect.getsourcelines(func)[0])
    
    if line_count > max_lines:
        return QualityCheckResult(
            passed=False,
            message=f"Function '{func.__name__}' is too long ({line_count} > {max_lines} lines)",
            severity="warning",
            line=inspect.getsourcelines(func)[1]
        )
    return QualityCheckResult(passed=True, message="Function length OK")

def check_docstring(func: Callable, source: str) -> QualityCheckResult:
    """Check if function has a docstring."""
    if not func.__doc__:
        return QualityCheckResult(
            passed=False,
            message=f"Function '{func.__name__}' is missing a docstring",
            severity="warning",
            line=inspect.getsourcelines(func)[1]
        )
    return QualityCheckResult(passed=True, message="Docstring present")

def check_arg_naming(func: Callable, source: str) -> QualityCheckResult:
    """Check argument naming follows snake_case."""
    args = inspect.signature(func).parameters
    for arg_name in args:
        if not re.match(r'^[a-z][a-z0-9_]*$', arg_name):
            return QualityCheckResult(
                passed=False,
                message=f"Argument '{arg_name}' should be in snake_case",
                severity="error",
                line=inspect.getsourcelines(func)[1]
            )
    return QualityCheckResult(passed=True, message="Argument naming OK")

def check_variable_naming(func: Callable, source: str) -> QualityCheckResult:
    """Check variable naming follows snake_case."""
    # This is a simplified version - in practice, you'd want to use AST
    # to properly parse and check all variable assignments
    lines = source.split('\n')
    for i, line in enumerate(lines, 1):
        # Simple check for variable assignments (not foolproof)
        if '=' in line and not line.strip().startswith('def'):
            var_name = line.split('=')[0].strip()
            if var_name and not re.match(r'^[a-z][a-z0-9_]*$', var_name):
                return QualityCheckResult(
                    passed=False,
                    message=f"Variable '{var_name}' should be in snake_case",
                    severity="error",
                    line=i
                )
    return QualityCheckResult(passed=True, message="Variable naming OK")

# Example usage
if __name__ == "__main__":
    @enforce_quality
    def example_function(arg_one, argTwo):  # Will trigger arg naming check
        """Example function with quality checks."""
        BadVar = 42  # Will trigger variable naming check
        return BadVar + arg_one
    
    try:
        example_function(1, 2)
    except QualityError as e:
        print(f"Quality check failed: {e}")
