"""
SPYQ - Quality Guard Setup

This module provides functionality to set up Quality Guard in a Python project.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import shutil
from typing import Optional, Union, Dict, Any


class QualityGuardInstaller:
    """Instalator Quality Guard z naprawionymi ścieżkami"""

    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "quality-guard.json"

        # Sprawdź czy jesteśmy już w katalogu Quality Guard
        self.is_source_dir = self._is_quality_guard_source_directory()

    def _is_quality_guard_source_directory(self):
        """Sprawdza czy aktualny katalog to źródła Quality Guard"""
        indicators = [
            "quality_guard_exceptions.py",
            "setup_quality_guard.py",
            "core/",
            "wrappers/",
            "config/"
        ]

        return any((self.project_root / indicator).exists() for indicator in indicators)

    def install_option_1_pip_package(self):
        """OPCJA 1: Instalacja jako pakiet pip (naprawiona)"""
        print("📦 OPCJA 1: Instalacja jako pakiet pip")
        print("=" * 50)

        if not self.is_source_dir:
            print("❌ Błąd: Nie znaleziono plików źródłowych Quality Guard")
            print("💡 Uruchom ten skrypt w katalogu z plikami Quality Guard")
            return False

        # Sprawdź czy setup.py istnieje
        setup_py = self.project_root / "setup.py"
        if not setup_py.exists():
            print("📝 Tworzenie setup.py...")
            self._create_setup_py()

        # Sprawdź czy pyproject.toml istnieje
        pyproject = self.project_root / "pyproject.toml"
        if not pyproject.exists():
            print("📝 Tworzenie pyproject.toml...")
            self._create_pyproject_toml()

        print("🚀 Instalacja pakietu...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-e", "."
            ], check=True, capture_output=True, text=True)

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
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Błąd instalacji: {e}")
            print(f"Output: {e.stdout}")
            print(f"Error: {e.stderr}")
            return False

    def install_option_3_project_local(self):
        """OPCJA 3: Instalacja lokalna w projekcie (naprawiona)"""
        print("📁 OPCJA 3: Instalacja lokalna w projekcie")
        print("=" * 50)

        if self.is_source_dir:
            print("ℹ️  Jesteś już w katalogu źródłowym Quality Guard")
            print("🔄 Tworzenie kopii dla demonstracji...")

            # Utwórz katalog demo
            demo_dir = self.project_root / "demo_project"
            demo_dir.mkdir(exist_ok=True)

            # Przejdź do katalogu demo
            original_cwd = os.getcwd()
            os.chdir(demo_dir)
            self.project_root = demo_dir

            print(f"📁 Praca w katalogu demo: {demo_dir}")

        # Lista plików do skopiowania
        quality_files = [
            ("quality_guard_exceptions.py", "core/quality_guard_exceptions.py"),
            ("quality-config.json", "config/quality-config.json"),
            ("python-quality-wrapper.py", "wrappers/python-quality-wrapper.py"),
            ("nodejs-quality-wrapper.js", "wrappers/nodejs-quality-wrapper.js")
        ]

        print("📂 Kopiowanie plików Quality Guard...")

        source_root = Path(original_cwd) if self.is_source_dir else self.project_root

        for local_name, source_path in quality_files:
            source_file = source_root / source_path
            target_file = self.project_root / local_name

            if source_file.exists() and source_file != target_file:
                try:
                    shutil.copy2(source_file, target_file)
                    print(f"  ✅ {local_name}")
                except Exception as e:
                    print(f"  ⚠️ Nie można skopiować {local_name}: {e}")
            elif source_file == target_file:
                print(f"  ✅ {local_name} (już istnieje)")
            else:
                print(f"  ❌ Brak pliku źródłowego: {source_path}")

        # Stwórz aktywator
        self._create_project_activator()

        # Stwórz startup script
        self._create_startup_script()

        print("✅ Instalacja zakończona!")
        print("\n📋 Użycie:")
        print("python run_with_quality.py main.py")
        print("# lub po ustawieniu aliasu:")
        print("python main.py  # automatycznie z Quality Guard")

        return True

    def _create_setup_py(self):
        """Tworzy setup.py"""
        setup_content = '''#!/usr/bin/env python3
"""Setup script for Quality Guard"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Quality Guard - Automatic Code Quality Enforcement"

setup(
    name="quality-guard",
    version="1.0.0",
    author="Quality Guard Team",
    description="Automatic code quality enforcement at interpreter level",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "quality-guard=quality_guard_exceptions:main",
        ],
    },
    py_modules=["quality_guard_exceptions"],
)
'''

        with open("setup.py", "w") as f:
            f.write(setup_content)

    def _create_pyproject_toml(self):
        """Tworzy pyproject.toml"""
        pyproject_content = '''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "quality-guard"
version = "1.0.0"
description = "Automatic code quality enforcement at interpreter level"
authors = [{name = "Quality Guard Team"}]
license = {text = "MIT"}
requires-python = ">=3.7"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]

[project.scripts]
quality-guard = "quality_guard_exceptions:main"

[tool.setuptools]
py-modules = ["quality_guard_exceptions"]
'''

        with open("pyproject.toml", "w") as f:
            f.write(pyproject_content)

    def _create_project_activator(self):
        """Tworzy aktywator projektu"""
        activator_content = '''# quality_guard_activator.py
# Aktywuj Quality Guard lokalnie w projekcie

import sys
import os
from pathlib import Path

# Dodaj ścieżkę projektu
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🛡️ Quality Guard Activator")

try:
    import quality_guard_exceptions
    quality_guard_exceptions.QualityGuardInstaller.install_globally()
    print("✅ Quality Guard aktywny dla tego projektu")
except ImportError as e:
    print(f"⚠️ Nie można załadować Quality Guard: {e}")
    print("💡 Sprawdź czy quality_guard_exceptions.py istnieje")
except Exception as e:
    print(f"⚠️ Błąd aktywacji Quality Guard: {e}")

def activate_for_file(file_path):
    """Aktywuje Quality Guard dla konkretnego pliku"""
    if not os.path.exists(file_path):
        print(f"❌ Plik {file_path} nie istnieje")
        return False

    print(f"🔍 Sprawdzanie jakości: {file_path}")

    try:
        import quality_guard_exceptions
        validator = quality_guard_exceptions.QualityGuardValidator()
        violations = validator.analyze_file(file_path)

        if violations:
            print(f"❌ Znaleziono {len(violations)} naruszeń:")
            for violation in violations[:5]:  # Pokaż pierwsze 5
                print(f"  • {violation.message}")
            if len(violations) > 5:
                print(f"  ... i {len(violations) - 5} więcej")
            return False
        else:
            print("✅ Kod spełnia standardy jakości!")
            return True

    except Exception as e:
        print(f"❌ Błąd walidacji: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_to_check = sys.argv[1]
        activate_for_file(file_to_check)
'''

        with open("quality_guard_activator.py", "w") as f:
            f.write(activator_content)

    def _create_startup_script(self):
        """Tworzy skrypt startowy"""
        startup_content = '''#!/usr/bin/env python3
# run_with_quality.py
# Uruchom swój kod z Quality Guard

import sys
import os
from pathlib import Path

def main():
    print("🛡️ Quality Guard Runner")

    if len(sys.argv) < 2:
        print("❌ Użycie: python run_with_quality.py <your_script.py> [args...]")
        print("   Przykład: python run_with_quality.py main.py")
        sys.exit(1)

    script_to_run = sys.argv[1]
    script_args = sys.argv[2:]

    if not os.path.exists(script_to_run):
        print(f"❌ Plik {script_to_run} nie istnieje")
        sys.exit(1)

    # Aktywuj Quality Guard
    try:
        import quality_guard_activator
        if quality_guard_activator.activate_for_file(script_to_run):
            print("🚀 Uruchamianie kodu...")

            # Uruchom skrypt
            script_globals = {
                '__name__': '__main__',
                '__file__': os.path.abspath(script_to_run)
            }

            with open(script_to_run) as f:
                code = f.read()
                exec(code, script_globals)
        else:
            print("🚫 Kod nie spełnia standardów jakości - wykonanie przerwane")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Błąd: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

        with open("run_with_quality.py", "w") as f:
            f.write(startup_content)

        # Ustaw uprawnienia wykonywania
        os.chmod("run_with_quality.py", 0o755)

    def install_option_2_sitecustomize(self):
        """OPCJA 2: sitecustomize.py (bez zmian)"""
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
        # Sprawdź czy Quality Guard jest zainstalowany jako pakiet
        import quality_guard_exceptions
        quality_guard_exceptions.QualityGuardInstaller.install_globally()
        print("🛡️ Quality Guard aktywny (pakiet)")
    except ImportError:
        # Sprawdź czy Quality Guard jest w lokalnym projekcie
        if os.path.exists("quality_guard_exceptions.py"):
            sys.path.insert(0, os.getcwd())
            try:
                import quality_guard_exceptions
                quality_guard_exceptions.QualityGuardInstaller.install_globally()
                print("🛡️ Quality Guard aktywny (lokalny)")
            except Exception:
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
        return True

    def create_demo_files(self):
        """Tworzy pliki demonstracyjne"""
        print("🎨 Tworzenie plików demonstracyjnych...")

        # Utwórz katalogi
        os.makedirs("src", exist_ok=True)
        os.makedirs("tests", exist_ok=True)

        # Plik z problemami jakości
        bad_code = '''# main.py - Kod z problemami jakości (celowo)

def process_user_data_with_many_parameters_and_complex_logic(user_id, first_name, last_name, email_address, phone_number, street_address, city_name, postal_code, country_code, date_of_birth, preferences, settings, metadata):
    if user_id:
        if first_name:
            if last_name:
                if email_address:
                    if phone_number:
                        if street_address:
                            if city_name:
                                if postal_code:
                                    result = {}
                                    result['id'] = user_id
                                    result['first'] = first_name.strip().title()
                                    result['last'] = last_name.strip().title()
                                    result['email'] = email_address.lower().strip()
                                    result['phone'] = phone_number.strip()
                                    result['address'] = street_address.strip()
                                    result['city'] = city_name.strip()
                                    result['postal'] = postal_code.strip()
                                    result['country'] = country_code
                                    result['birth'] = date_of_birth
                                    result['prefs'] = preferences
                                    result['settings'] = settings
                                    result['meta'] = metadata
                                    result['status'] = 'active'
                                    result['created'] = 'now'
                                    result['updated'] = 'now'
                                    return result
    return None

def another_function_without_documentation():
    data = [1, 2, 3, 4, 5]
    return sum(data)

if __name__ == "__main__":
    result = process_user_data_with_many_parameters_and_complex_logic(
        "123", "John", "Doe", "john@example.com", "+1234567890",
        "123 Main St", "Anytown", "12345", "US", "1990-01-01",
        {"theme": "dark"}, {"notifications": True}, {"source": "web"}
    )
    print(f"Result: {result}")

    result2 = another_function_without_documentation()
    print(f"Sum: {result2}")
'''

        with open("main.py", "w") as f:
            f.write(bad_code)

        # Dobry przykład kodu
        good_code = '''"""
Good example module demonstrating Quality Guard compliance.
"""

from typing import Dict, Any, Optional


def process_user_data(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process and validate user data input.

    Args:
        user_data: Dictionary containing user information

    Returns:
        Processed user data or None if invalid

    Example:
        >>> data = {"user_id": "123", "name": "John", "email": "john@example.com"}
        >>> result = process_user_data(data)
        >>> result["status"]
        'active'
    """
    if not user_data or not isinstance(user_data, dict):
        return None

    required_fields = ["user_id", "name", "email"]
    if not all(field in user_data for field in required_fields):
        return None

    return _build_user_record(user_data)


def _build_user_record(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build formatted user record from validated data.

    Args:
        user_data: Validated user data dictionary

    Returns:
        Formatted user record
    """
    return {
        "user_id": user_data["user_id"],
        "name": user_data["name"].strip().title(),
        "email": user_data["email"].lower().strip(),
        "status": "active",
        "created_at": "now"
    }


def calculate_sum(numbers: list) -> int:
    """
    Calculate sum of a list of numbers.

    Args:
        numbers: List of numbers to sum

    Returns:
        Sum of all numbers

    Example:
        >>> calculate_sum([1, 2, 3, 4, 5])
        15
    """
    return sum(numbers)
'''

        with open("src/good_example.py", "w") as f:
            f.write(good_code)

        # Testy dla dobrego przykładu
        test_code = '''"""
Tests for good_example module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from good_example import process_user_data, calculate_sum


def test_process_user_data_valid():
    """Test processing valid user data."""
    user_data = {
        "user_id": "123",
        "name": "  john doe  ",
        "email": "  JOHN@EXAMPLE.COM  "
    }

    result = process_user_data(user_data)

    assert result is not None
    assert result["user_id"] == "123"
    assert result["name"] == "John Doe"
    assert result["email"] == "john@example.com"
    assert result["status"] == "active"


def test_process_user_data_invalid():
    """Test processing invalid user data."""
    assert process_user_data(None) is None
    assert process_user_data({}) is None
    assert process_user_data({"user_id": "123"}) is None  # Missing required fields


def test_calculate_sum():
    """Test calculate_sum function."""
    assert calculate_sum([1, 2, 3, 4, 5]) == 15
    assert calculate_sum([]) == 0
    assert calculate_sum([-1, 1]) == 0
'''

        with open("tests/test_good_example.py", "w") as f:
            f.write(test_code)

        print("  ✅ main.py (z problemami jakości)")
        print("  ✅ src/good_example.py (dobry przykład)")
        print("  ✅ tests/test_good_example.py (testy)")

    def interactive_install(self):
        """Interaktywna instalacja (naprawiona)"""
        print("🛡️ QUALITY GUARD - INTERAKTYWNA INSTALACJA")
        print("=" * 60)
        print()

        if self.is_source_dir:
            print("ℹ️  Wykryto katalog źródłowy Quality Guard")
            print()

        print("Wybierz opcję instalacji:")
        print()
        print("1. 📦 Pakiet pip (zalecane) - zainstaluj jako pakiet Python")
        print("2. 🌍 sitecustomize.py - automatyczne dla środowiska")
        print("3. 📁 Lokalna w projekcie - tylko dla tego projektu")
        print("4. 🎨 Demo + lokalna instalacja - pokaż przykłady")
        print("5. 🚀 Wszystkie opcje (mega instalacja)")
        print()

        while True:
            try:
                choice = input("Wybierz opcję (1-5): ").strip()

                if choice == "1":
                    success = self.install_option_1_pip_package()
                    break
                elif choice == "2":
                    success = self.install_option_2_sitecustomize()
                    break
                elif choice == "3":
                    success = self.install_option_3_project_local()
                    break
                elif choice == "4":
                    print("🎨 DEMO + INSTALACJA LOKALNA")
                    print("=" * 40)
                    self.create_demo_files()
                    success = self.install_option_3_project_local()
                    if success:
                        self._show_demo_instructions()
                    break
                elif choice == "5":
                    print("🚀 MEGA INSTALACJA - wszystkie opcje!")
                    success1 = self.install_option_1_pip_package()
                    success2 = self.install_option_2_sitecustomize()
                    success3 = self.install_option_3_project_local()
                    self.create_demo_files()
                    print("🎉 Wszystkie opcje zainstalowane!")
                    success = success1 or success2 or success3
                    break
                else:
                    print("❌ Nieprawidłowy wybór, spróbuj ponownie")
            except KeyboardInterrupt:
                print("\n\n👋 Instalacja przerwana")
                sys.exit(1)

        if success:
            self._show_final_instructions()
        else:
            self._show_troubleshooting()

    def _show_demo_instructions(self):
        """Pokazuje instrukcje demo"""
        print("\n🎮 INSTRUKCJE DEMO:")
        print("=" * 30)
        print("1. Przetestuj zły kod:")
        print("   python run_with_quality.py main.py")
        print("   (powinien pokazać naruszenia jakości)")
        print()
        print("2. Przetestuj dobry kod:")
        print("   python run_with_quality.py src/good_example.py")
        print("   (powinien przejść pomyślnie)")
        print()
        print("3. Uruchom testy:")
        print("   python -m pytest tests/ -v")
        print()
        print("4. Sprawdź konkretny plik:")
        print("   python quality_guard_activator.py main.py")

    def _show_final_instructions(self):
        """Pokazuje finalne instrukcje"""
        print("\n🎉 INSTALACJA ZAKOŃCZONA!")
        print("=" * 60)
        print("📋 Następne kroki:")
        print("1. Restart terminala (jeśli użyto opcji 2)")
        print("2. Przetestuj instalację:")
        print("   python -c \"print('🛡️ Quality Guard test')\"")
        print("3. Uruchom swój kod - Quality Guard będzie aktywny!")

    def _show_troubleshooting(self):
        """Pokazuje informacje o rozwiązywaniu problemów"""
        print("\n🔧 ROZWIĄZYWANIE PROBLEMÓW:")
        print("=" * 40)
        print("Jeśli instalacja nie powiodła się:")
        print("1. Sprawdź uprawnienia do zapisu")
        print("2. Uruchom z sudo (dla opcji sitecustomize)")
        print("3. Sprawdź czy Python >= 3.7")
        print("4. Sprawdź czy pip jest zainstalowany")


def setup_quality_guard(project_path: Union[str, Path], force: bool = False) -> bool:
    """
    Set up Quality Guard in the specified project directory.

    Args:
        project_path: Path to the project directory where Quality Guard should be set up
        force: If True, overwrite existing files

    Returns:
        bool: True if setup was successful, False otherwise
    """
    try:
        installer = QualityGuardInstaller()
        # Change to the project directory
        original_dir = os.getcwd()
        os.chdir(str(project_path))
        
        # Run the local installation
        result = installer.install_option_3_project_local()
        
        # Change back to the original directory
        os.chdir(original_dir)
        return result
    except Exception as e:
        print(f"Error setting up Quality Guard: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for the setup script."""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Usage: spyq setup [path] [--force]")
        print("\nOptions:")
        print("  path     Path to the project directory (default: current directory)")
        print("  --force  Overwrite existing files")
        return

    # For backward compatibility with the original script
    if len(sys.argv) > 1 and any(arg.startswith('--') for arg in sys.argv[1:]):
        installer = QualityGuardInstaller()
        option = sys.argv[1]
        if option == "--pip":
            installer.install_option_1_pip_package()
        elif option == "--site":
            installer.install_option_2_sitecustomize()
        elif option == "--local":
            installer.install_option_3_project_local()
        elif option == "--demo":
            installer.create_demo_files()
            installer.install_option_3_project_local()
        elif option == "--all":
            installer.install_option_1_pip_package()
            installer.install_option_2_sitecustomize()
            installer.install_option_3_project_local()
            installer.create_demo_files()
        else:
            print("Options: --pip, --site, --local, --demo, --all")
    else:
        installer = QualityGuardInstaller()
        installer.interactive_install()


if __name__ == "__main__":
    main()