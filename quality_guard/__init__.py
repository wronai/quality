
"""Quality Guard - Automatic code quality enforcement"""

import sys
import importlib.util
from .exceptions import *
from .validator import QualityGuardValidator
from .decorators import require_tests, require_docs, enforce_quality

# AUTO-INSTALACJA przy imporcie
def auto_install():
    """Automatycznie instaluje Quality Guard w interpreterze"""
    if not hasattr(sys, '_quality_guard_installed'):
        from .installer import QualityGuardInstaller
        QualityGuardInstaller.install_globally()
        sys._quality_guard_installed = True

# Automatyczna instalacja gdy pakiet jest importowany
auto_install()

__version__ = "1.0.0"
__all__ = [
    'require_tests', 'require_docs', 'enforce_quality',
    'QualityGuardException', 'MissingTestException', 
    'MissingDocumentationException'
]
