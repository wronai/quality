# quality_guard_activator.py
# Automatycznie aktywuje Quality Guard w projekcie

import sys
import os
from pathlib import Path

# Załaduj Quality Guard
try:
    from quality_guard_exceptions import QualityGuardInstaller
    QualityGuardInstaller.install_globally()
    print("🛡️ Quality Guard aktywny dla tego projektu")
except ImportError as e:
    print(f"⚠️ Nie można załadować Quality Guard: {e}")
    print("💡 Uruchom: python setup_quality_guard.py --local")

# Auto-import - wszystkie kolejne importy będą sprawdzane
