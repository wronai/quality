# File: setup.py
from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Uruchom nasz skrypt instalacyjny
        import spyq.install
        spyq.install.install()

setup(
    name="spyq",
    version="0.1.10",  # Zwiększ wersję
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "spyq=spyq.cli:main",
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    include_package_data=True,
    python_requires=">=3.7",
    author="Tom Sapletta",
    author_email="tom@sapletta.com",
    description="SPYQ - Shell Python Quality Guard",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wronai/quality",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)