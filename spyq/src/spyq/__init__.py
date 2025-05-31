# In spyq/__init__.py
import sys
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import importlib.util
import importlib.machinery
import ast
import json

__version__ = "0.1.10"

class SPYQImportHook:
    def __init__(self):
        self.original_import = None
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        # Try to load config from ~/.config/spyq/config.json
        config_path = Path.home() / ".config" / "spyq" / "config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default config
        return {
            "max_file_lines": 300,
            "max_function_lines": 50,
            "max_function_params": 4,
            "max_nesting_depth": 4,
            "require_docstrings": True,
            "require_type_hints": True,
            "forbid_global_vars": True,
            "forbid_bare_except": True,
            "forbid_print_statements": True
        }
    
    def validate_source(self, source: str, filename: str) -> List[Dict[str, Any]]:
        """Validate Python source code against configured rules."""
        issues = []
        
        try:
            tree = ast.parse(source, filename=filename)
            
            # Check file length
            if 'max_file_lines' in self.config:
                line_count = len(source.splitlines())
                if line_count > self.config['max_file_lines']:
                    issues.append({
                        'line': 1,
                        'col': 0,
                        'message': f'File too long ({line_count} > {self.config["max_file_lines"]} lines)',
                        'type': 'error'
                    })
            
            # Add more validations here...
            
        except SyntaxError as e:
            issues.append({
                'line': e.lineno or 1,
                'col': e.offset or 0,
                'message': f'Syntax error: {e.msg}',
                'type': 'error'
            })
        
        return issues
    
    def find_spec(self, fullname, path=None, target=None):
        """Find the module spec and install our loader if it's a Python file."""
        if self.original_import is None:
            return None
            
        spec = self.original_import(fullname, path, target)
        if spec is not None and spec.origin is not None and spec.origin.endswith('.py'):
            spec.loader = SPYQLoader(spec.loader, self)
        return spec

class SPYQLoader:
    def __init__(self, original_loader, hook):
        self.original_loader = original_loader
        self.hook = hook
    
    def create_module(self, spec):
        return self.original_loader.create_module(spec)
    
    def exec_module(self, module):
        # Get the source code
        source = self.original_loader.get_source(module.__name__)
        if source is not None:
            # Validate the source
            issues = self.hook.validate_source(source, getattr(module, '__file__', '<string>'))
            if issues:
                for issue in issues:
                    print(f"{module.__file__}:{issue['line']}:{issue['col']}: {issue['type'].upper()}: {issue['message']}")
                if any(issue['type'] == 'error' for issue in issues):
                    print("Validation failed - aborting execution")
                    sys.exit(1)
        
        # Execute the module
        return self.original_loader.exec_module(module)
    
    # Forward all other attributes to the original loader
    def __getattr__(self, name):
        return getattr(self.original_loader, name)

def install_import_hook():
    """Install the SPYQ import hook."""
    if not hasattr(sys, 'frozen'):
        hook = SPYQImportHook()
        # Save the original import function
        if not hasattr(sys, '_spyq_original_import'):
            import builtins
            sys._spyq_original_import = builtins.__import__
            hook.original_import = builtins.__import__
            builtins.__import__ = hook.find_spec
        return hook

# Install the hook automatically when the module is imported
if 'SPYQ_DISABLE' not in os.environ:
    install_import_hook()