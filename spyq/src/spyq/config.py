"""
SPYQ Configuration Manager

Handles loading and validating configuration from config files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration
DEFAULT_CONFIG = {
    "max_file_lines": 300,
    "max_function_lines": 50,
    "max_function_params": 4,
    "max_nesting_depth": 4,
    "enable_import_hook": True,
    "validate_on_import": True,
}

class ConfigError(Exception):
    """Raised when there's an error with the configuration."""
    pass

class ConfigManager:
    """Manages SPYQ configuration."""
    
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.config_paths = [
            Path.cwd() / "spyq.json",  # Project config
            Path.home() / ".config" / "spyq" / "config.json",  # User config
            Path.home() / ".spyq" / "config.json",  # Legacy user config
        ]
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from the first available config file."""
        for config_path in self.config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        user_config = json.load(f)
                        self.config.update(user_config)
                        break
                except (json.JSONDecodeError, IOError) as e:
                    raise ConfigError(f"Error loading config from {config_path}: {e}")
        
        return self.config
    
    def save(self, config: Dict[str, Any], path: Optional[Path] = None) -> Path:
        """Save configuration to a file."""
        if path is None:
            # Default to project config if in a project, otherwise user config
            if (Path.cwd() / "pyproject.toml").exists() or (Path.cwd() / "setup.py").exists():
                path = Path.cwd() / "spyq.json"
            else:
                path = Path.home() / ".config" / "spyq" / "config.json"
        
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, 'w') as f:
                json.dump(config, f, indent=2)
            return path
        except IOError as e:
            raise ConfigError(f"Error saving config to {path}: {e}")
    
    def init_config(self, path: Optional[Path] = None) -> Path:
        """Initialize a new configuration file."""
        return self.save(DEFAULT_CONFIG, path)

def get_config() -> Dict[str, Any]:
    """Get the current configuration."""
    return ConfigManager().load()
