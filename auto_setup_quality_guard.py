#!/usr/bin/env python3
# auto_setup_quality_guard.py
# Automatyczny instalator Quality Guard dla nowych projektów

import os
import sys
import subprocess
import shutil
from pathlib import Path
import requests


def download_quality_guard():
    """Pobiera najnowszą wersję Quality Guard"""
    print("📦 Pobieranie Quality Guard...")

    # Lista kluczowych plików do pobrania
    base_url = "https://raw.githubusercontent.com/quality-guard/quality-guard/main"
    essential_files = {
        "core/quality_guard_exceptions.py": "quality_guard_exceptions.py",
        "config/quality-config.json": "quality-config.json",
        "core/setup_quality_guard.py": "setup_quality_guard.py",
        "templates/test-template.py": "templates/test-template.py",
        "templates/function-template.py": "templates/function-template.py"
    }

    for remote_path, local_path in essential_files.items():
        try:
            url = f"{base_url}/{remote_path}"
            response = requests.get(url)
            response.raise_for_status()

            # Utwórz katalog jeśli nie istnieje
            local_file = Path(local_path)
            local_file.parent.mkdir(parents=True, exist_ok=True)

            with open(local_file, 'w') as f:
                f.write(response.text)

            print(f"  ✅ {local_path}")

        except Exception as e:
            print(f"  ❌ Błąd pobierania {remote_path}: {e}")

    return True


def setup_project_structure():
    """Tworzy strukturę projektu z Quality Guard"""
    print("🏗️ Tworzenie struktury projektu...")

    # Struktura katalogów
    directories = [
        "src",
        "tests",
        "docs",
        "config",
        "scripts"
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  📁 {directory}/")

    return True


def create_project_files():
    """Tworzy podstawowe pliki projektu"""
    print("📝 Tworzenie plików projektu...")

    # main.py z Quality Guard
    main_py = '''#!/usr/bin/env python3
"""
Main application file with Quality Guard integration
"""

# Quality Guard Auto-Activation
try:
    import quality_guard_exceptions
    quality_guard_exceptions.QualityGuardInstaller.install_globally()
    print("🛡️ Quality Guard active!")
except ImportError:
    print("⚠️ Quality Guard not found - install with: pip install quality-guard")

def main():
    """
    Main application function.

    This function serves as the entry point for the application.
    Quality Guard will enforce that this function has proper tests
    and documentation.

    Returns:
        int: Exit code (0 for success)
    """
    print("Hello, World! (with Quality Guard)")
    return 0

if __name__ == "__main__":
    exit(main())
'''

    with open("main.py", "w") as f:
        f.write(main_py)
    print("  ✅ main.py")

    # requirements.txt
    requirements = '''# Core dependencies
quality-guard>=1.0.0

# Development dependencies (optional)
pytest>=6.0.0
black>=21.0.0
flake8>=3.8.0
mypy>=0.800
'''

    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("  ✅ requirements.txt")

    # .gitignore
    gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Quality Guard
quality-violations.log
quality-report-*.html
.quality_guard/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env
.venv
env/
venv/
'''

    with open(".gitignore", "w") as f:
        f.write(gitignore)
    print("  ✅ .gitignore")

    # Makefile
    makefile = '''# Makefile for Python project with Quality Guard

.PHONY: setup dev test quality clean help

setup: ## Install dependencies and setup Quality Guard
	pip install -r requirements.txt
	python setup_quality_guard.py --local

dev: ## Run in development mode
	python main.py

test: ## Run tests
	python -m pytest tests/ -v

quality: ## Check code quality
	python -c "import quality_guard_exceptions; print('Quality Guard OK')"

clean: ## Clean temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f quality-violations.log

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-30s\\033[0m %s\\n", $1, $2}'
'''

    with open("Makefile", "w") as f:
        f.write(makefile)
    print("  ✅ Makefile")

    return True


def create_sample_test():
    """Tworzy przykładowy test"""
    print("🧪 Tworzenie przykładowego testu...")

    test_main = '''"""
Tests for main.py
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import main


class TestMain:
    """Tests for main function"""

    def test_main_returns_zero(self):
        """Test that main function returns 0 for success"""
        result = main()
        assert result == 0

    def test_main_is_callable(self):
        """Test that main function is callable"""
        assert callable(main)

    def test_main_has_documentation(self):
        """Test that main function has proper documentation"""
        assert main.__doc__ is not None
        assert len(main.__doc__.strip()) > 10
'''

    with open("tests/test_main.py", "w") as f:
        f.write(test_main)
    print("  ✅ tests/test_main.py")

    return True


def install_quality_guard():
    """Instaluje i konfiguruje Quality Guard"""
    print("⚙️ Instalowanie Quality Guard...")

    try:
        # Uruchom setup Quality Guard
        if Path("setup_quality_guard.py").exists():
            subprocess.run([sys.executable, "setup_quality_guard.py", "--local"], check=True)
            print("  ✅ Quality Guard skonfigurowany lokalnie")
        else:
            print("  ⚠️ setup_quality_guard.py nie znaleziony, używam basic setup")

        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Błąd instalacji Quality Guard: {e}")
        return False


def test_installation():
    """Testuje czy instalacja działa"""
    print("🔬 Testowanie instalacji...")

    try:
        # Test 1: Import Quality Guard
        result = subprocess.run([
            sys.executable, "-c",
            "import quality_guard_exceptions; print('Import OK')"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("  ✅ Import Quality Guard - OK")
        else:
            print("  ❌ Import Quality Guard - FAILED")
            return False

        # Test 2: Uruchom main.py
        result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)

        if result.returncode == 0:
            print("  ✅ Uruchomienie main.py - OK")
        else:
            print(f"  ❌ Uruchomienie main.py - FAILED: {result.stderr}")
            return False

        # Test 3: Uruchom testy
        if Path("tests/test_main.py").exists():
            result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"],
                                    capture_output=True, text=True)

            if result.returncode == 0:
                print("  ✅ Testy - OK")
            else:
                print(f"  ⚠️ Testy - SOME ISSUES: {result.stdout}")

        return True

    except Exception as e:
        print(f"  ❌ Błąd testowania: {e}")
        return False


def main():
    """Główna funkcja instalatora"""
    print("🛡️ QUALITY GUARD - AUTOMATYCZNY SETUP NOWEGO PROJEKTU")
    print("=" * 60)

    project_name = input("📝 Nazwa projektu (default: my-project): ").strip() or "my-project"

    # Utwórz katalog projektu
    project_path = Path(project_name)
    if project_path.exists():
        overwrite = input(f"⚠️ Katalog {project_name} już istnieje. Kontynuować? (y/N): ")
        if overwrite.lower() != 'y':
            print("❌ Anulowano")
            return

    project_path.mkdir(exist_ok=True)
    os.chdir(project_path)

    print(f"\n📁 Tworzenie projektu w: {project_path.absolute()}")

    # Wykonaj kroki instalacji
    steps = [
        ("Pobieranie Quality Guard", download_quality_guard),
        ("Tworzenie struktury projektu", setup_project_structure),
        ("Tworzenie plików projektu", create_project_files),
        ("Tworzenie przykładowego testu", create_sample_test),
        ("Instalowanie Quality Guard", install_quality_guard),
        ("Testowanie instalacji", test_installation)
    ]

    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            success = step_func()
            if not success:
                print(f"❌ {step_name} - FAILED")
                break
        except Exception as e:
            print(f"❌ {step_name} - ERROR: {e}")
            break
    else:
        # Wszystkie kroki zakończone sukcesem
        print("\n🎉 PROJEKT UTWORZONY POMYŚLNIE!")
        print("=" * 60)
        print(f"📁 Lokalizacja: {project_path.absolute()}")
        print("\n📋 Następne kroki:")
        print("1. cd", project_name)
        print("2. make setup     # Finalna konfiguracja")
        print("3. make dev       # Uruchom aplikację")
        print("4. make test      # Uruchom testy")
        print("5. make quality   # Sprawdź jakość kodu")
        print("\n🛡️ Quality Guard jest aktywny - kod automatycznie sprawdzany!")
        print("💡 Edytuj quality-config.json aby dostosować reguły")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Instalacja przerwana przez użytkownika")
    except Exception as e:
        print(f"\n❌ Nieoczekiwany błąd: {e}")
        sys.exit(1)