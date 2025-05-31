# quality_guard_activator.py
# Automatycznie aktywuje Quality Guard w projekcie

import sys
import os
import inspect
from pathlib import Path
from typing import Any, Callable, Dict, Optional

# Globalna flaga wskazująca, czy Quality Guard jest aktywny
_quality_guard_active = False

def wrap_function(func: Callable) -> Callable:
    """Opakowuje funkcję w Quality Guard."""
    if hasattr(func, '_quality_guard_wrapped'):
        return func  # Już opakowana

    from quality_guard_exceptions import enforce_quality
    
    wrapped = enforce_quality(func)
    wrapped._quality_guard_wrapped = True
    return wrapped

def wrap_module_functions(module_name: str) -> None:
    """Opakowuje wszystkie funkcje w module."""
    import importlib
    try:
        module = sys.modules[module_name]
        for name, obj in list(module.__dict__.items()):
            if (inspect.isfunction(obj) and 
                obj.__module__ == module_name and 
                not name.startswith('_')):
                setattr(module, name, wrap_function(obj))
    except Exception as e:
        print(f"⚠️ Błąd podczas opakowywania modułu {module_name}: {e}")

# Główna inicjalizacja
try:
    from quality_guard_exceptions import QualityGuardInstaller, enforce_quality
    
    # Zainstaluj globalnie
    QualityGuardInstaller.install_globally()
    
    # Oznacz jako aktywny
    _quality_guard_active = True
    sys._quality_guard_installed = True
    sys._quality_guard_version = "1.0.0"
    
    print("🛡️ Quality Guard aktywny dla tego projektu")
    
    # Opakuj funkcje w bieżącym module głównym
    if __name__ != "__main__":
        wrap_module_functions(__name__)
        
except ImportError as e:
    print(f"⚠️ Nie można załadować Quality Guard: {e}")
    print("💡 Upewnij się, że wszystkie zależności są zainstalowane")

# Eksportuj funkcje do użytku zewnętrznego
__all__ = ['wrap_function', 'wrap_module_functions']
