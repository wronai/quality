# File: spyq/post_install.py
import os
import site
from pathlib import Path


def create_wrapper_script():
    # Get the installation directory
    site_packages = site.getsitepackages()[0]
    wrapper_script = Path(site_packages) / 'spyq' / 'scripts' / 'spyq-python'

    # Create a symlink in a directory in PATH
    bin_dir = Path.home() / '.local' / 'bin'
    bin_dir.mkdir(parents=True, exist_ok=True)

    # Add to PATH if not already there
    if str(bin_dir) not in os.environ['PATH'].split(':'):
        with open(Path.home() / '.bashrc', 'a') as f:
            f.write(f'\nexport PATH="$HOME/.local/bin:$PATH"')

    # Create the symlink
    target = bin_dir / 'python'
    if target.exists():
        target.unlink()
    target.symlink_to(wrapper_script)
    target.chmod(0o755)


if __name__ == "__main__":
    create_wrapper_script()