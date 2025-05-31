"""
SPYQ Import Hook

Provides an import hook that validates Python modules when they're imported.
"""

import importlib.abc
import importlib.machinery
import sys
import warnings
from pathlib import Path
from typing import Any, Optional, Sequence

from .config import get_config
from .validator import validate_file, ValidationError

class SPYQLoader(importlib.machinery.SourceFileLoader):
    """A loader that validates source code before importing it."""
    
    def __init__(self, fullname: str, path: str) -> None:
        super().__init__(fullname, path)
        self.config = get_config()
    
    def source_to_code(self, data: bytes, path: str, *, _optimize: int = -1) -> Any:
        """Convert source code to a code object, validating it first."""
        if self.config.get('validate_on_import', True):
            self._validate_source(path)
        return super().source_to_code(data, path, _optimize=_optimize)
    
    def _validate_source(self, path: str) -> None:
        """Validate the source file."""
        try:
            issues = validate_file(Path(path))
            if issues:
                self._report_issues(issues, path)
        except Exception as e:
            warnings.warn(f"Failed to validate {path}: {e}", RuntimeWarning)
    
    def _report_issues(self, issues: list, path: str) -> None:
        """Report validation issues."""
        print(f"\nSPYQ Validation issues in {path}:", file=sys.stderr)
        for issue in issues:
            line = issue.get('line', 0)
            col = issue.get('col', 0)
            msg = issue['message']
            print(f"  Line {line}, Column {col}: {msg}", file=sys.stderr)
        print(file=sys.stderr)
        
        if self.config.get('strict', False):
            raise ValidationError(f"Validation failed for {path}")

class SPYQFinder(importlib.abc.MetaPathFinder):
    """A finder that uses SPYQLoader to load Python modules."""
    
    def __init__(self) -> None:
        self.config = get_config()
        self.original_path_hooks = None
        self.original_path_importer_cache = None
    
    def find_spec(self, fullname: str, path: Optional[Sequence[str]] = None, target=None):
        """Find the spec for the given module."""
        if not self.config.get('enable_import_hook', True):
            return None
            
        # Let the standard finder find the module first
        for finder in sys.meta_path:
            if finder is not self and hasattr(finder, 'find_spec'):
                spec = finder.find_spec(fullname, path, target)
                if spec is not None and spec.origin and spec.origin.endswith('.py'):
                    # Replace the loader with our own
                    spec.loader = SPYQLoader(fullname, spec.origin)
                    return spec
        return None

def install_import_hook() -> None:
    """Install the SPYQ import hook."""
    config = get_config()
    if not config.get('enable_import_hook', True):
        return
    
    # Check if already installed
    for finder in sys.meta_path:
        if isinstance(finder, SPYQFinder):
            return
    
    # Install our finder
    finder = SPYQFinder()
    sys.meta_path.insert(0, finder)

def uninstall_import_hook() -> None:
    """Uninstall the SPYQ import hook."""
    for i, finder in enumerate(sys.meta_path):
        if isinstance(finder, SPYQFinder):
            sys.meta_path.pop(i)
            break

# Install the hook when this module is imported
install_import_hook()
