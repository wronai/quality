#!/usr/bin/env python3
"""
Setup script for Quality Guard
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "docs" / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Quality Guard - Automatic Code Quality Enforcement"

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, "r") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
else:
    requirements = []

setup(
    name="quality-guard",
    version="1.0.0",
    author="Quality Guard Team",
    author_email="team@qualityguard.dev",
    description="Automatic code quality enforcement at interpreter level",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quality-guard/quality-guard",
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
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "full": [
            "jq>=1.2",
            "complexity-report>=2.0",
            "jsinspect>=0.8",
        ]
    },
    entry_points={
        "console_scripts": [
            "quality-guard=core.setup_quality_guard:main",
            "qg=core.setup_quality_guard:main",
        ],
    },
    include_package_data=True,
    package_data={
        "quality_guard": [
            "config/*.json",
            "config/*.js",
            "templates/*.py",
            "templates/*.json",
        ],
    },
    scripts=[
        "wrappers/python-quality-wrapper.py",
        "wrappers/nodejs-quality-wrapper.js",
        "scripts/setup-quality-aliases.sh",
    ],
)
