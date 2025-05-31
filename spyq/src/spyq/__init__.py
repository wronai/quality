"""
SPYQ - Shell Python Quality Guard

A command-line tool for managing and enforcing code quality in Python projects.

This package provides tools to set up and manage code quality checks,
including automatic test and documentation requirements for Python functions.
"""

__version__ = "0.1.0"

from pathlib import Path
from typing import Optional

from .cli import main
from .setup_quality_guard import setup_quality_guard, QualityGuardInstaller

__all__ = [
    'main',
    'setup_quality_guard',
    'QualityGuardInstaller',
]
