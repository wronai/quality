
from setuptools import setup, find_packages

setup(
    name="quality-guard",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'quality-guard=quality_guard.cli:main',
        ],
    },
    python_requires='>=3.7',
)
