"""
Quality Guard - Automatic Code Quality Enforcement System

Main components:
- quality_guard_exceptions: Exception-based quality control
- setup_quality_guard: Installation and setup utilities
- validators: Code validation logic
"""

from .quality_guard_exceptions import (
    QualityGuardException,
    MissingTestException,
    MissingDocumentationException,
    ComplexityException,
    FunctionTooLongException,
    require_tests,
    require_docs,
    enforce_quality,
    QualityGuardValidator,
    QualityConfig,
    AutoGenerator
)

__version__ = "1.0.0"
__author__ = "Quality Guard Team"

# Auto-activation when imported
import sys
if not hasattr(sys, '_quality_guard_active'):
    from .quality_guard_exceptions import QualityGuardInstaller
    QualityGuardInstaller.install_globally()
    sys._quality_guard_active = True
    print("🛡️ Quality Guard activated automatically")

__all__ = [
    'QualityGuardException',
    'MissingTestException', 
    'MissingDocumentationException',
    'ComplexityException',
    'FunctionTooLongException',
    'require_tests',
    'require_docs', 
    'enforce_quality',
    'QualityGuardValidator',
    'QualityConfig',
    'AutoGenerator'
]
