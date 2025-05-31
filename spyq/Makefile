# Makefile for SPYQ - Shell Python Quality Guard

# Python interpreter to use
PYTHON ?= python3
PIP ?= pip

# Package information
PACKAGE = spyq
TEST_PATH = tests/
SRC_PATH = src/$(PACKAGE)

# Default target
.DEFAULT_GOAL := help
.PHONY: all setup install test lint type-check security-check format check clean build publish help \
	docker-test docker-ansible docker-examples run-examples run-ansible \
	coverage docs pre-commit-install pre-commit-run

# Help target
help: ## Show this help message
	@echo "SPYQ - Shell Python Quality Guard"
	@echo ""
	@echo "Development:"
	@echo "  setup             Create virtual environment and install development dependencies"
	@echo "  install           Install the package in development mode"
	@echo "  pre-commit-install  Install pre-commit hooks"
	@echo "  pre-commit-run     Run pre-commit checks"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  test              Run tests with pytest"
	@echo "  test-cov          Run tests with coverage report"
	@echo "  lint              Run code linter (flake8)"
	@echo "  type-check        Run static type checking (mypy)"
	@echo "  security-check    Run security checks (bandit)"
	@echo "  format            Format code with black and isort"
	@echo "  check             Run all checks (lint, type-check, test)"
	@echo ""
	@echo "Build & Publish:"
	@echo "  build             Build package"
	@echo "  publish           Publish package to PyPI"
	@echo "  version           Bump version using poetry"
	@echo ""
	@echo "Documentation:"
	@echo "  docs              Generate API documentation"
	@echo ""
	@echo "Docker:"
	@echo "  docker-test       Run tests in Docker"
	@echo "  docker-ansible    Run Ansible tests in Docker"
	@echo "  docker-examples   Run validation examples in Docker"
	@echo ""
	@echo "Utilities:"
	@echo "  clean             Remove build artifacts and caches"
	@echo "  help              Show this help message"
	@echo ""
	@echo "Run 'make <target>' to execute a command. For example: make test"

# Create virtual environment and install dependencies
setup:
	@echo "Setting up development environment..."
	$(PYTHON) -m venv .venv
	@echo "Activate with: source .venv/bin/activate"

# Install the package in development mode
install:
	@echo "Installing SPYQ in development mode..."
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

# Install pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install

# Run pre-commit checks
pre-commit-run:
	@echo "Running pre-commit checks..."
	pre-commit run --all-files

# Run tests
test:
	@echo "Running tests..."
	pytest $(TEST_PATH) -v

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	pytest --cov=$(PACKAGE) --cov-report=term-missing --cov-report=xml $(TEST_PATH) -v

# Run code linter
lint:
	@echo "Running linter..."
	flake8 $(SRC_PATH) $(TEST_PATH)

# Run static type checking
type-check:
	@echo "Running type checking..."
	mypy $(SRC_PATH) $(TEST_PATH)

# Run security checks
security-check:
	@echo "Running security checks..."
	bandit -r $(SRC_PATH)

# Run validation examples locally
run-examples:
	@echo "Running validation examples..."
	$(PYTHON) examples/run_validation_examples.py

# Run Ansible tests locally
run-ansible:
	@echo "Running Ansible tests..."
	ansible-playbook tests/integration/playbooks/test_spyq_validations.yml -v

# Docker targets
docker-test:
	@echo "Running tests in Docker..."
	docker-compose up --build test

docker-ansible:
	@echo "Running Ansible tests in Docker..."
	docker-compose up --build ansible-test

docker-examples:
	@echo "Running validation examples in Docker..."
	docker-compose up --build validation-examples

# Format code with black and isort
format:
	@echo "Formatting code with black..."
	black $(SRC_PATH) $(TEST_PATH)
	@echo "Sorting imports with isort..."
	isort $(SRC_PATH) $(TEST_PATH)

# Generate API documentation
docs:
	@echo "Generating API documentation..."
	$(PIP) install pdoc3
	pdoc3 --html -o docs/ --force $(PACKAGE)
	@echo "Documentation generated in docs/"

# Run all checks
check: lint type-check security-check test
	@echo "All checks passed!"

# Clean build artifacts and caches
clean:
	@echo "Cleaning up..."
	rm -rf build/ dist/ *.egg-info/ .coverage* htmlcov/ || true
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.pyc' -exec rm -f {} + 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.coverage' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.py,cover' -exec rm -f {} + 2>/dev/null || true

# Build package
build:
	@echo "Building package..."
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

# Bump version using poetry
version:
	@echo "Bumping version..."
	poetry version patch

# Publish package to PyPI
publish: version clean build
	@echo "Publishing to PyPI..."
	$(PYTHON) -m pip install --upgrade twine
	$(PYTHON) -m twine upload dist/*

# Show help
.PHONY: help
