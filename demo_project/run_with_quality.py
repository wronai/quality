#!/usr/bin/env python3
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
