"""
SPYQ Validator

Validates Python code against configured quality rules.
"""

import ast
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable, TypeVar

from .config import get_config

class ValidationError(Exception):
    """Raised when validation fails."""
    def __init__(self, message: str, line: int = 0, col: int = 0):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(self.message)

class CodeValidator(ast.NodeVisitor):
    """Validates Python code against configured rules."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or get_config()
        self.issues: List[Dict[str, Any]] = []
    
    def validate_file(self, filepath: Path) -> List[Dict[str, Any]]:
        """Validate a Python file."""
        self.issues = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
                
            # Check file length
            self._check_file_length(source, filepath)
            
            # Parse and check AST
            try:
                tree = ast.parse(source, filename=str(filepath))
                self.visit(tree)
            except SyntaxError as e:
                self._add_issue(f"Syntax error: {e.msg}", e.lineno, e.offset or 0)
                
        except IOError as e:
            self._add_issue(f"Could not read file: {e}")
            
        return self.issues
    
    def _check_file_length(self, source: str, filepath: Path) -> None:
        """Check if the file exceeds the maximum allowed lines."""
        max_lines = self.config.get('max_file_lines', 300)
        line_count = len(source.splitlines())
        
        if line_count > max_lines:
            self._add_issue(
                f"File too long ({line_count} > {max_lines} lines)",
                line=line_count
            )
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions and validate them."""
        # Check function length
        self._check_function_length(node)
        
        # Check number of parameters
        self._check_param_count(node)
        
        # Check nesting depth
        self._check_nesting_depth(node)
        
        # Continue visiting child nodes
        self.generic_visit(node)
    
    def _check_function_length(self, node: ast.FunctionDef) -> None:
        """Check if function exceeds maximum allowed lines."""
        max_lines = self.config.get('max_function_lines', 50)
        line_count = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 1
        
        if line_count > max_lines:
            self._add_issue(
                f"Function '{node.name}' is too long ({line_count} > {max_lines} lines)",
                node.lineno
            )
    
    def _check_param_count(self, node: ast.FunctionDef) -> None:
        """Check if function has too many parameters."""
        max_params = self.config.get('max_function_params', 4)
        param_count = len(node.args.args) + len(node.args.kwonlyargs)
        
        if param_count > max_params:
            self._add_issue(
                f"Function '{node.name}' has too many parameters ({param_count} > {max_params})",
                node.lineno
            )
    
    def _check_nesting_depth(self, node: ast.AST) -> None:
        """Check maximum nesting depth in a function."""
        max_depth = self.config.get('max_nesting_depth', 4)
        
        class DepthVisitor(ast.NodeVisitor):
            def __init__(self):
                self.max_depth = 0
                self.current_depth = 0
                
            def visit_If(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
                
            def visit_For(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
                
            def visit_While(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
                
            def visit_Try(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
        
        visitor = DepthVisitor()
        visitor.visit(node)
        
        if visitor.max_depth > max_depth:
            self._add_issue(
                f"Code nesting too deep (max {max_depth} levels, found {visitor.max_depth})",
                node.lineno
            )
    
    def _add_issue(self, message: str, line: int = 0, col: int = 0) -> None:
        """Add a validation issue."""
        self.issues.append({
            'message': message,
            'line': line,
            'col': col,
            'severity': 'error'
        })

def validate_file(filepath: Path) -> List[Dict[str, Any]]:
    """Validate a Python file against configured rules."""
    validator = CodeValidator()
    return validator.validate_file(filepath)

def validate_source(source: str, filename: str = "<string>") -> List[Dict[str, Any]]:
    """Validate Python source code against configured rules."""
    validator = CodeValidator()
    
    # Write source to a temporary file and validate
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(source)
        temp_path = Path(f.name)
    
    try:
        return validator.validate_file(temp_path)
    finally:
        temp_path.unlink()  # Clean up the temporary file
