# quality_guard_activator.py
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
