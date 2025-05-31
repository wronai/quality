# File: spyq/sitecustomize.py
import os
import sys
import site
from pathlib import Path


def install_spyq_wrapper():
    # Skip if already installed or in a virtual environment
    if hasattr(sys, 'real_prefix') or os.environ.get('VIRTUAL_ENV'):
        return

    # Skip if SPYQ_DISABLE is set
    if os.environ.get('SPYQ_DISABLE'):
        return

    # Get the user's site-packages directory
    site_packages = site.getusersitepackages()
    if not os.path.exists(site_packages):
        os.makedirs(site_packages, exist_ok=True)

    # Create a .pth file to add our wrapper to the path
    pth_path = os.path.join(site_packages, 'spyq.pth')
    spyq_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    with open(pth_path, 'w') as f:
        f.write(f"{spyq_dir}\n")

    # Set up the PATH
    bin_dir = os.path.join(spyq_dir, 'scripts')
    if os.path.exists(bin_dir):
        os.environ['PATH'] = f"{bin_dir}:{os.environ.get('PATH', '')}"


# Install the wrapper
install_spyq_wrapper()