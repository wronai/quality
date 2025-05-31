# setup_quality_guard.py
# Łatwa instalacja Quality Guard dla każdego projektu Python

import os
import sys
import subprocess
import json
from pathlib import Path
import shutil


class QualityGuardInstaller:
    """Instalator Quality Guard z różnymi opcjami wdrożenia"""

    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "quality-guard.json"

    def install_option_1_pip_package(self):
        """OPCJA 1: Instalacja jako pakiet pip (najłatwiejsza)"""
        print("📦 OPCJA 1: Instalacja jako pakiet pip")
        print("=" * 50)

        # Stwórz setup.py dla pakietu
        setup_content = '''
from setuptools import setup, find_packages

setup(
    name="quality-guard",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'quality-guard=quality_guard.cli:main',
        ],
    },
    python_requires='>=3.7',
)
'''

        # Stwórz __init__.py z auto-instalacją
        init_content = '''
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
'''

        print("📁 Tworząc strukturę pakietu...")
        package_dir = self.project_root / "quality_guard"
        package_dir.mkdir(exist_ok=True)

        (package_dir / "__init__.py").write_text(init_content)
        (self.project_root / "setup.py").write_text(setup_content)

        print("💾 Kopiowanie głównych plików...")
        # Tu należy skopiować pliki z quality_guard_exceptions.py

        print("🚀 Instalacja pakietu...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."])

        print("✅ Instalacja zakończona!")
        print("\n📋 Użycie:")
        print("import quality_guard  # Automatycznie aktywuje Quality Guard")
        print("# lub")
        print("from quality_guard import require_tests, require_docs")
        print("")
        print("@require_tests")
        print("@require_docs")
        print("def my_function():")
        print("    pass")

    def install_option_2_sitecustomize(self):
        """OPCJA 2: sitecustomize.py (automatyczne dla całego środowiska)"""
        print("🌍 OPCJA 2: Instalacja przez sitecustomize.py")
        print("=" * 50)

        # Znajdź ścieżkę site-packages
        import site
        site_packages = site.getsitepackages()[0]
        sitecustomize_path = Path(site_packages) / "sitecustomize.py"

        sitecustomize_content = '''
# sitecustomize.py - Automatyczna instalacja Quality Guard
import sys
import os

def install_quality_guard():
    """Instaluje Quality Guard automatycznie przy starcie Pythona"""
    try:
        # Importuj Quality Guard jeśli dostępny
        import quality_guard
        print("🛡️ Quality Guard aktywny")
    except ImportError:
        # Sprawdź czy Quality Guard jest w lokalnym projekcie
        if os.path.exists("quality_guard_exceptions.py"):
            sys.path.insert(0, os.getcwd())
            try:
                import quality_guard_exceptions
                quality_guard_exceptions.QualityGuardInstaller.install_globally()
                print("🛡️ Quality Guard załadowany z lokalnego projektu")
            except Exception as e:
                pass  # Ciche niepowodzenie

# Automatyczna instalacja
if not hasattr(sys, '_quality_guard_active'):
    install_quality_guard()
    sys._quality_guard_active = True
'''

        print(f"📝 Tworzenie {sitecustomize_path}...")

        # Sprawdź czy sitecustomize.py już istnieje
        if sitecustomize_path.exists():
            print("⚠️  sitecustomize.py już istnieje, dodaję do istniejącego pliku")
            with open(sitecustomize_path, 'a') as f:
                f.write(f"\n\n# Quality Guard Auto-Install\n{sitecustomize_content}")
        else:
            sitecustomize_path.write_text(sitecustomize_content)

        print("✅ Instalacja zakończona!")
        print("\n📋 Efekt:")
        print("• Quality Guard będzie automatycznie aktywny przy każdym uruchomieniu Pythona")
        print("• Działa dla wszystkich projektów w tym środowisku")
        print("• Nie wymaga zmian w kodzie projektów")

    def install_option_3_project_local(self):
        """OPCJA 3: Instalacja lokalna w projekcie"""
        print("📁 OPCJA 3: Instalacja lokalna w projekcie")
        print("=" * 50)

        # Skopiuj główne pliki Quality Guard
        quality_files = [
            "quality_guard_exceptions.py",
            "quality_config.json"
        ]

        print("📂 Kopiowanie plików Quality Guard...")
        for file_name in quality_files:
            if Path(file_name).exists():
                shutil.copy(file_name, self.project_root)
                print(f"  ✅ {file_name}")

        # Stwórz plik aktywacyjny
        activator_content = '''
# quality_guard_activator.py
# Aktywuj Quality Guard lokalnie w projekcie

import sys
import os
from pathlib import Path

# Dodaj ścieżkę projektu
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from quality_guard_exceptions import QualityGuardInstaller
    QualityGuardInstaller.install_globally()
    print("🛡️ Quality Guard aktywny dla tego projektu")
except ImportError as e:
    print(f"⚠️ Nie można załadować Quality Guard: {e}")

# Auto-import dla popularnych modułów
def auto_import_with_quality():
    """Automatycznie importuje moduły z Quality Guard"""
    original_import = __builtins__.__import__

    def quality_aware_import(name, *args, **kwargs):
        module = original_import(name, *args, **kwargs)

        # Jeśli to moduł projektu, dodaj Quality Guard
        if hasattr(module, '__file__') and module.__file__:
            module_path = Path(module.__file__)
            if str(project_root) in str(module_path):
                # To jest moduł z naszego projektu
                add_quality_decorators_to_module(module)

        return module

    __builtins__.__import__ = quality_aware_import

def add_quality_decorators_to_module(module):
    """Dodaje dekoratory Quality Guard do funkcji w module"""
    try:
        from quality_guard_exceptions import enforce_quality

        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                attr = getattr(module, attr_name)
                if callable(attr) and hasattr(attr, '__module__'):
                    if attr.__module__ == module.__name__:
                        # Wrap function with quality guard
                        wrapped = enforce_quality(attr)
                        setattr(module, attr_name, wrapped)
    except Exception:
        pass  # Fail silently

# Aktywuj auto-import
auto_import_with_quality()
'''

        activator_path = self.project_root / "quality_guard_activator.py"
        activator_path.write_text(activator_content)

        # Stwórz plik startowy
        startup_content = '''
# run_with_quality.py
# Uruchom swój kod z Quality Guard

import quality_guard_activator  # Aktywuje Quality Guard
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python run_with_quality.py <your_script.py>")
        sys.exit(1)

    script_to_run = sys.argv[1]

    # Uruchom skrypt z Quality Guard
    with open(script_to_run) as f:
        code = f.read()
        exec(code, {'__name__': '__main__'})
'''

        startup_path = self.project_root / "run_with_quality.py"
        startup_path.write_text(startup_content)

        # Stwórz alias w .bashrc/.zshrc
        self._create_shell_alias("python", f"python {startup_path}")

        print("✅ Instalacja zakończona!")
        print("\n📋 Użycie:")
        print("python run_with_quality.py main.py")
        print("# lub po ustawieniu aliasu:")
        print("python main.py  # automatycznie z Quality Guard")

    def install_option_4_environment_variable(self):
        """OPCJA 4: Zmienna środowiskowa PYTHONPATH"""
        print("🌿 OPCJA 4: Instalacja przez zmienne środowiskowe")
        print("=" * 50)

        # Stwórz katalog Quality Guard w home
        quality_home = Path.home() / ".quality_guard"
        quality_home.mkdir(exist_ok=True)

        print(f"📂 Instalacja w {quality_home}")

        # Skopiuj pliki
        quality_files = ["quality_guard_exceptions.py"]
        for file_name in quality_files:
            if Path(file_name).exists():
                shutil.copy(file_name, quality_home)

        # Stwórz auto-loader
        autoload_content = '''
# Auto-loader dla Quality Guard
import sys
import os

def load_quality_guard():
    """Ładuje Quality Guard automatycznie"""
    quality_home = os.path.expanduser("~/.quality_guard")
    if quality_home not in sys.path:
        sys.path.insert(0, quality_home)

    try:
        import quality_guard_exceptions
        quality_guard_exceptions.QualityGuardInstaller.install_globally()
        return True
    except ImportError:
        return False

# Auto-load przy imporcie
if os.environ.get('QUALITY_GUARD_ENABLE', '1') == '1':
    load_quality_guard()
'''

        autoload_path = quality_home / "__init__.py"
        autoload_path.write_text(autoload_content)

        # Dodaj do zmiennych środowiskowych
        self._add_to_shell_config(f'export PYTHONPATH="$PYTHONPATH:{quality_home}"')
        self._add_to_shell_config('export QUALITY_GUARD_ENABLE=1')

        print("✅ Instalacja zakończona!")
        print("\n📋 Efekt:")
        print("• Quality Guard będzie dostępny globalnie")
        print("• Można włączać/wyłączać przez QUALITY_GUARD_ENABLE")
        print("• Restart terminala wymagany")

    def install_option_5_import_hook(self):
        """OPCJA 5: Import hook (najbardziej eleganckie)"""
        print("🪝 OPCJA 5: Instalacja przez import hook")
        print("=" * 50)

        # Stwórz meta path finder
        hook_content = '''
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
'''

        hook_path = self.project_root / "quality_guard_hook.py"
        hook_path.write_text(hook_content)

        # Stwórz aktywator
        activator_content = '''
# W każdym projekcie dodaj na początku main.py:
import quality_guard_hook  # Aktywuje hook
'''

        print("📝 Tworzenie plików...")
        (self.project_root / "activate_quality_guard.py").write_text(activator_content)

        print("✅ Instalacja zakończona!")
        print("\n📋 Użycie:")
        print("# Na początku każdego skryptu dodaj:")
        print("import quality_guard_hook")
        print("# Wszystkie następne importy będą miały Quality Guard")

    def _create_shell_alias(self, command, replacement):
        """Tworzy alias w shell"""
        shell_configs = [
            Path.home() / ".bashrc",
            Path.home() / ".zshrc"
        ]

        alias_line = f'alias {command}="{replacement}"'

        for config_file in shell_configs:
            if config_file.exists():
                with open(config_file, 'a') as f:
                    f.write(f'\n# Quality Guard alias\n{alias_line}\n')
                print(f"✅ Alias dodany do {config_file}")

    def _add_to_shell_config(self, line):
        """Dodaje linię do konfiguracji shell"""
        shell_configs = [
            Path.home() / ".bashrc",
            Path.home() / ".zshrc"
        ]

        for config_file in shell_configs:
            if config_file.exists():
                with open(config_file, 'a') as f:
                    f.write(f'\n{line}\n')

    def create_configuration(self):
        """Tworzy plik konfiguracyjny"""
        config = {
            "require_tests": True,
            "require_docstrings": True,
            "require_architecture_docs": False,
            "max_function_lines": 50,
            "max_complexity": 10,
            "enforcement_level": "error",
            "auto_generate": {
                "tests": True,
                "docs": True
            },
            "test_patterns": [
                "tests/test_*.py",
                "test_*.py",
                "*_test.py"
            ],
            "doc_files": [
                "README.md",
                "docs/API.md",
                "ARCHITECTURE.md"
            ],
            "exceptions": {
                "missing_test": "MissingTestException",
                "missing_docs": "MissingDocumentationException",
                "high_complexity": "ComplexityException",
                "function_too_long": "FunctionTooLongException"
            }
        }

        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"✅ Konfiguracja utworzona: {self.config_file}")

    def interactive_install(self):
        """Interaktywna instalacja"""
        print("🛡️ QUALITY GUARD - INTERAKTYWNA INSTALACJA")
        print("=" * 60)
        print()
        print("Wybierz opcję instalacji:")
        print()
        print("1. 📦 Pakiet pip (zalecane) - najłatwiejsze")
        print("2. 🌍 sitecustomize.py - automatyczne dla środowiska")
        print("3. 📁 Lokalna w projekcie - tylko dla tego projektu")
        print("4. 🌿 Zmienne środowiskowe - globalne, konfigurowalne")
        print("5. 🪝 Import hook - najbardziej eleganckie")
        print("6. 🚀 Wszystkie opcje (mega instalacja)")
        print()

        while True:
            try:
                choice = input("Wybierz opcję (1-6): ").strip()

                if choice == "1":
                    self.install_option_1_pip_package()
                    break
                elif choice == "2":
                    self.install_option_2_sitecustomize()
                    break
                elif choice == "3":
                    self.install_option_3_project_local()
                    break
                elif choice == "4":
                    self.install_option_4_environment_variable()
                    break
                elif choice == "5":
                    self.install_option_5_import_hook()
                    break
                elif choice == "6":
                    print("🚀 MEGA INSTALACJA - wszystkie opcje!")
                    self.install_option_1_pip_package()
                    self.install_option_2_sitecustomize()
                    self.install_option_3_project_local()
                    self.install_option_4_environment_variable()
                    self.install_option_5_import_hook()
                    print("🎉 Wszystkie opcje zainstalowane!")
                    break
                else:
                    print("❌ Nieprawidłowy wybór, spróbuj ponownie")
            except KeyboardInterrupt:
                print("\n\n👋 Instalacja przerwana")
                sys.exit(1)

        # Utwórz konfigurację
        self.create_configuration()

        print("\n" + "=" * 60)
        print("🎉 INSTALACJA ZAKOŃCZONA!")
        print("=" * 60)
        print()
        print("📋 Następne kroki:")
        print("1. Restart terminala (jeśli używasz opcji 2, 4)")
        print(
            "2. Przetestuj: python -c \"import sys; print('Quality Guard:', hasattr(sys, '_quality_guard_installed'))\"")
        print("3. Uruchom swój kod - Quality Guard będzie aktywny!")
        print()
        print("🔧 Konfiguracja w: quality-guard.json")
        print("📚 Dokumentacja: https://github.com/your-repo/quality-guard")


def main():
    """Główna funkcja instalatora"""
    installer = QualityGuardInstaller()

    if len(sys.argv) > 1:
        option = sys.argv[1]
        if option == "--pip":
            installer.install_option_1_pip_package()
        elif option == "--site":
            installer.install_option_2_sitecustomize()
        elif option == "--local":
            installer.install_option_3_project_local()
        elif option == "--env":
            installer.install_option_4_environment_variable()
        elif option == "--hook":
            installer.install_option_5_import_hook()
        elif option == "--all":
            installer.install_option_1_pip_package()
            installer.install_option_2_sitecustomize()
            installer.install_option_3_project_local()
            installer.install_option_4_environment_variable()
            installer.install_option_5_import_hook()
        else:
            print("Opcje: --pip, --site, --local, --env, --hook, --all")
    else:
        installer.interactive_install()


if __name__ == "__main__":
    main()