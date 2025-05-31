# integrate_quality_guard.py
# !/usr/bin/env python3
"""
Automatyczna integracja Quality Guard z istniejącym projektem Python
"""

import os
import sys
import shutil
import json
from pathlib import Path


def integrate_quality_guard(project_path=".", quality_guard_path="../quality-guard"):
    """Integruje Quality Guard z projektem"""

    project_path = Path(project_path).absolute()
    quality_guard_path = Path(quality_guard_path).absolute()

    print(f"🔧 Integracja Quality Guard z projektem: {project_path}")

    # 1. Skopiuj główne pliki
    core_files = [
        "core/quality_guard_exceptions.py",
        "core/setup_quality_guard.py",
        "config/quality-config.json"
    ]

    for file_path in core_files:
        src = quality_guard_path / file_path
        dst = project_path / Path(file_path).name

        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Skopiowano: {Path(file_path).name}")
        else:
            print(f"  ❌ Brak pliku: {file_path}")

    # 2. Stwórz aktywator
    activator_content = '''# quality_guard_activator.py
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
'''

    activator_path = project_path / "quality_guard_activator.py"
    activator_path.write_text(activator_content)
    print("  ✅ Utworzono: quality_guard_activator.py")

    # 3. Zaktualizuj main.py jeśli istnieje
    main_files = ["main.py", "app.py", "__main__.py", "run.py"]
    for main_file in main_files:
        main_path = project_path / main_file
        if main_path.exists():
            content = main_path.read_text()
            if "quality_guard_activator" not in content:
                # Dodaj import na początku
                lines = content.split('\n')
                lines.insert(0, "import quality_guard_activator  # Aktywuje Quality Guard")
                main_path.write_text('\n'.join(lines))
                print(f"  ✅ Zaktualizowano: {main_file}")
            break

    # 4. Stwórz requirements.txt jeśli nie istnieje
    req_path = project_path / "requirements.txt"
    if not req_path.exists():
        req_path.write_text("# Quality Guard requirements\n# (Quality Guard nie wymaga dodatkowych pakietów)\n")
        print("  ✅ Utworzono: requirements.txt")

    # 5. Stwórz .gitignore jeśli nie istnieje
    gitignore_path = project_path / ".gitignore"
    if not gitignore_path.exists():
        gitignore_content = '''# Python
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
*.swo

# OS
.DS_Store
Thumbs.db
'''
        gitignore_path.write_text(gitignore_content)
        print("  ✅ Utworzono: .gitignore")

    # 6. Stwórz Makefile jeśli nie istnieje
    makefile_path = project_path / "Makefile"
    if not makefile_path.exists():
        makefile_content = '''# Makefile dla projektu z Quality Guard

.PHONY: setup dev test quality clean

setup:
	pip install -r requirements.txt
	python setup_quality_guard.py --local

dev:
	python main.py

test:
	python -m pytest tests/ -v

quality:
	python setup_quality_guard.py --check-project

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f quality-violations.log
	rm -f quality-report-*.html

help:
	@echo "Dostępne komendy:"
	@echo "  setup   - Instalacja zależności i Quality Guard"
	@echo "  dev     - Uruchomienie w trybie deweloperskim"
	@echo "  test    - Uruchomienie testów"
	@echo "  quality - Sprawdzenie jakości kodu"
	@echo "  clean   - Czyszczenie plików tymczasowych"
'''
        makefile_path.write_text(makefile_content)
        print("  ✅ Utworzono: Makefile")

    print("\n🎉 Integracja zakończona!")
    print("\n📋 Następne kroki:")
    print("1. python setup_quality_guard.py --local")
    print("2. python main.py  # (Quality Guard będzie aktywny)")
    print("3. make quality    # (sprawdź jakość kodu)")

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."

    integrate_quality_guard(project_path)