""
SPYQ - Shell Python Quality Guard

A command-line tool for managing and enforcing code quality in Python projects.
"""

__version__ = "0.1.0"

from .cli import main
from .setup_quality_guard import setup_quality_guard

__all__ = ['main', 'setup_quality_guard']
