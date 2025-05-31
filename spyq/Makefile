# Makefile for SPYQ - Shell Python Quality Guard

.PHONY: all setup install test lint format clean build publish help

# Default target
all: help

# Help target
help:
	@echo "SPYQ - Shell Python Quality Guard"
	@echo ""
	@echo "Available targets:"
	@echo "  setup     Create virtual environment and install dependencies"
	@echo "  install   Install the package in development mode"
	@echo "  test      Run tests"
	@echo "  lint      Run code linter"
	@echo "  format    Format code with black"
	@echo "  clean     Remove build artifacts and caches"
	@echo "  build     Build package"
	@echo "  publish   Publish package to PyPI"
	@echo "  help      Show this help message"

# Create virtual environment and install dependencies
setup:
	@echo "Setting up development environment..."
	python -m venv venv
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -e ".[dev]"

# Install the package in development mode
install:
	@echo "Installing SPYQ in development mode..."
	pip install -e .


# Run tests
test:
	@echo "Running tests..."
	pytest tests/

# Run code linter
lint:
	@echo "Running linter..."
	flake8 src/spyq tests

# Format code with black
format:
	@echo "Formatting code..."
	black src/spyq tests

# Clean build artifacts and caches
clean:
	@echo "Cleaning up..."
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} \;
	find . -type d -name .pytest_cache -exec rm -rf {} \;
	find . -type d -name .mypy_cache -exec rm -rf {} \;

# Build package
build:
	@echo "Building package..."
	python -m pip install --upgrade build
	python -m build

# Publish package to PyPI
publish: clean build
	@echo "Publishing to PyPI..."
	python -m pip install --upgrade twine
	python -m twine upload dist/*

# Show help
.PHONY: help
