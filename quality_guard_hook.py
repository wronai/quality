
# quality_guard_hook.py
# Import hook dla automatycznego Quality Guard

import sys
import importlib.util
from importlib.abc import MetaPathFinder, Loader
from pathlib import Path

class QualityGuardLoader(Loader):
    """Loader który dodaje Quality Guard do modułów"""

    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path

    def create_module(self, spec):
        """Tworzy moduł z Quality Guard"""
        return None  # Use default module creation

    def exec_module(self, module):
        """Wykonuje moduł i dodaje Quality Guard"""
        # Załaduj normalnie
        with open(self.path, 'rb') as f:
            source = f.read()

        code = compile(source, self.path, 'exec')
        exec(code, module.__dict__)

        # Dodaj Quality Guard do funkcji
        self._add_quality_guard_to_module(module)

    def _add_quality_guard_to_module(self, module):
        """Dodaje Quality Guard do wszystkich funkcji w module"""
        try:
            from quality_guard_exceptions import enforce_quality

            for attr_name in dir(module):
                if not attr_name.startswith('_'):
                    attr = getattr(module, attr_name)
                    if callable(attr) and hasattr(attr, '__module__'):
                        if attr.__module__ == module.__name__:
                            wrapped = enforce_quality(attr)
                            setattr(module, attr_name, wrapped)
        except ImportError:
            pass

class QualityGuardFinder(MetaPathFinder):
    """Meta path finder dla Quality Guard"""

    def find_spec(self, fullname, path, target=None):
        """Znajduje specyfikację modułu i dodaje Quality Guard"""

        # Tylko dla modułów użytkownika (nie systemowych)
        if self._is_user_module(fullname):
            # Znajdź normalną specyfikację
            for finder in sys.meta_path:
                if isinstance(finder, QualityGuardFinder):
                    continue

                spec = finder.find_spec(fullname, path, target)
                if spec and spec.origin:
                    # Podmień loader na nasz
                    spec.loader = QualityGuardLoader(fullname, spec.origin)
                    return spec

        return None

    def _is_user_module(self, fullname):
        """Sprawdza czy to moduł użytkownika"""
        # Pomiń moduły systemowe
        system_modules = ['os', 'sys', 'json', 'ast', 'inspect', 'functools']
        if any(fullname.startswith(mod) for mod in system_modules):
            return False

        # Pomiń site-packages
        try:
            import importlib.util
            spec = importlib.util.find_spec(fullname)
            if spec and spec.origin:
                if 'site-packages' in spec.origin:
                    return False
        except:
            pass

        return True

def install_import_hook():
    """Instaluje import hook"""
    finder = QualityGuardFinder()
    if finder not in sys.meta_path:
        sys.meta_path.insert(0, finder)
        print("🪝 Quality Guard import hook zainstalowany")

# Auto-instalacja
install_import_hook()
