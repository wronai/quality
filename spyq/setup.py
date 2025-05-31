# File: setup.py
from setuptools import setup, find_packages

setup(
    name="spyq",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "spyq": ["py.typed"],
    },
    entry_points={
        'console_scripts': [
            'spyq-python=spyq.scripts.spyq_python:main',
            'python-spyq=spyq.__main__:main',
        ],
    },
    python_requires='>=3.6',
)