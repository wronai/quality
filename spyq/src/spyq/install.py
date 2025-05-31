import os
import sys
import site
from pathlib import Path

def create_sitecustomize():
    """Tworzy plik sitecustomize.py z hookiem SPYQ"""
    sitecustomize_content = '''import sys
import os
import site

# Dodaj katalog site-packages do ścieżki
site.addsitedir(os.path.expanduser("~/.local/lib/python{sys_version}/site-packages"))

# Sprawdź, czy nie jest to środowisko wirtualne
if not hasattr(sys, 'real_prefix') and 'VIRTUAL_ENV' not in os.environ:
    try:
        import spyq
        # Sprawdź, czy plik nie jest wykonywany przez samego SPYQ
        if not any('spyq' in str(p).lower() for p in sys.argv):
            spyq.install_import_hook()
    except ImportError as e:
        sys.stderr.write(f"SPYQ import error: {e}\\n")
'''

    # Pobierz wersję Pythona
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    # Ścieżka do site-packages użytkownika
    user_site = site.getusersitepackages()
    sitecustomize_path = os.path.join(user_site, "sitecustomize.py")
    
    # Utwórz katalog jeśli nie istnieje
    os.makedirs(user_site, exist_ok=True)
    
    # Zapisz plik sitecustomize.py
    with open(sitecustomize_path, 'w') as f:
        f.write(sitecustomize_content.format(sys_version=py_version))
    
    return sitecustomize_path

def create_default_config():
    """Tworzy domyślną konfigurację SPYQ"""
    config_content = '''{
    "max_file_lines": 300,
    "max_function_lines": 50,
    "max_function_params": 4,
    "max_nesting_depth": 4,
    "require_docstrings": true,
    "require_type_hints": true,
    "forbid_global_vars": true,
    "forbid_bare_except": true,
    "forbid_print_statements": true
}'''
    config_dir = os.path.expanduser("~/.config/spyq")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.json")
    
    # Zapisz tylko jeśli plik nie istnieje
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write(config_content)
    
    return config_path

def install():
    """Instaluje hooki SPYQ"""
    try:
        sitecustomize = create_sitecustomize()
        config = create_default_config()
        print(f"SPYQ hook zainstalowany: {sitecustomize}")
        print(f"Domyślna konfiguracja: {config}")
    except Exception as e:
        print(f"Błąd podczas instalacji SPYQ: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(install())
