# Makefile for Bexy

.PHONY: all setup clean test lint format run help venv docker-test docker-build docker-clean test-package update-version publish publish-test

# Default values
PORT ?= 8000
HOST ?= 0.0.0.0

# Default target
all: help

# Create virtual environment if it doesn't exist
venv:
	@test -d venv || python3 -m venv venv

# Setup project
setup: venv
	@echo "Setting up Bexy..."
	@. venv/bin/activate && pip install -e .

# Clean project
clean:
	@echo "Cleaning Bexy..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name *.egg-info -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

# Run tests
test: setup
	@echo "Testing Bexy..."
	@. venv/bin/activate && python -m unittest discover

# Lint code
lint: setup
	@echo "Linting BEXY..."
	@. venv/bin/activate && flake8 bexy

# Format code
format: setup
	@echo "Formatting BEXY..."
	@. venv/bin/activate && black bexy

# Run the API server
run: setup
	@echo "Running BEXY API server on default port $(PORT)..."
	@. venv/bin/activate && python -m bexy.api --port $(PORT) --host $(HOST)

# Run with custom port (for backward compatibility)
run-port: setup
	@echo "Running BEXY API server on port $(PORT)..."
	@. venv/bin/activate && python -m bexy.api --port $(PORT) --host $(HOST)

# Docker testing targets
docker-build:
	@echo "Building Docker test images..."
	@./run_docker_tests.sh --build

docker-test: docker-build
	@echo "Running tests in Docker..."
	@./run_docker_tests.sh --run-tests

docker-interactive: docker-build
	@echo "Starting interactive Docker test environment..."
	@./run_docker_tests.sh --interactive

docker-mock: docker-build
	@echo "Starting BEXY mock service in Docker..."
	@./run_docker_tests.sh --mock-service

docker-clean:
	@echo "Cleaning Docker test environment..."
	@./run_docker_tests.sh --clean


# Build package
build: setup
	@echo "Building package..."
	@. venv/bin/activate && pip install -e . && pip install wheel twine build
	@. venv/bin/activate && rm -rf dist/* && python -m build

# Update version (manually update version in pyproject.toml)
update-version:
	@echo "Please update the version in pyproject.toml manually"
	@exit 1

# Publish package to PyPI
publish: build
	@echo "Publishing package to PyPI..."
	@. venv/bin/activate && twine check dist/* && twine upload dist/*

# Publish package to TestPyPI
publish-test: build
	@echo "Publishing package to TestPyPI..."
	@. venv/bin/activate && twine check dist/* && twine upload --repository testpypi dist/*
