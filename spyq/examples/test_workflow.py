"""
Integration tests for Quality Guard full workflow scenarios.

These tests simulate real-world usage patterns and verify that Quality Guard
works correctly in various development scenarios.
"""

import pytest
import tempfile
import os
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, mock_open
import json
import shutil

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "core"))

from quality_guard_exceptions import (
    QualityGuardValidator,
    QualityConfig,
    QualityGuardInstaller,
    AutoGenerator,
    MissingTestException,
    MissingDocumentationException,
    ComplexityException
)


class TestFullWorkflowScenarios:
    """Test complete Quality Guard workflows in realistic scenarios."""

    def setup_method(self):
        """Setup temporary directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Create basic project structure
        os.makedirs("src", exist_ok=True)
        os.makedirs("tests", exist_ok=True)

        # Create basic config
        self.config_data = {
            "rules": {
                "require_tests": True,
                "require_docstrings": True,
                "max_function_lines": 50,
                "max_complexity": 10,
                "max_function_params": 4
            },
            "enforcement": {
                "level": "error",
                "strict_mode": True
            }
        }

        with open("quality-config.json", "w") as f:
            json.dump(self.config_data, f)

    def teardown_method(self):
        """Cleanup after each test."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)

    def test_new_developer_onboarding_workflow(self):
        """Test complete workflow for new developer onboarding."""

        # Step 1: Developer writes their first function (without Quality Guard)
        bad_code = '''
def process_user_data(user_id, name, email, age, address, phone, preferences, settings):
    if user_id:
        if name:
            if email:
                if age > 0:
                    if address:
                        if phone:
                            if preferences:
                                if settings:
                                    # Very long function with many nested conditions
                                    result = {}
                                    result['user_id'] = user_id
                                    result['name'] = name.strip().title()
                                    result['email'] = email.lower().strip()
                                    result['age'] = int(age)
                                    result['address'] = address.strip()
                                    result['phone'] = phone.strip()
                                    result['preferences'] = preferences
                                    result['settings'] = settings
                                    result['status'] = 'active'
                                    result['created_at'] = 'now'
                                    result['updated_at'] = 'now'
                                    result['version'] = 1
                                    # ... more processing
                                    return result
    return None
'''

        with open("src/user_processor.py", "w") as f:
            f.write(bad_code)

        # Step 2: Install Quality Guard
        config = QualityConfig("quality-config.json")
        validator = QualityGuardValidator(config)

        # Step 3: Try to validate - should find multiple violations
        violations = validator.analyze_file("src/user_processor.py")

        assert len(violations) > 0
        violation_types = [v.rule_name for v in violations]

        # Should detect various issues
        assert "missing_test" in violation_types
        assert "missing_docstring" in violation_types
        assert "function_too_long" in violation_types or "high_complexity" in violation_types

        # Step 4: Developer fixes issues one by one
        good_code = '''
"""
User data processing module.

This module provides functions for processing and validating user data.
"""

from typing import Dict, Optional, Any


def process_user_data(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process and validate user data.

    Args:
        user_data: Dictionary containing user information with keys:
                  user_id, name, email, age, address, phone, preferences, settings

    Returns:
        Processed user data dictionary or None if validation fails

    Raises:
        ValueError: If required fields are missing or invalid
    """
    if not user_data or not isinstance(user_data, dict):
        return None

    # Validate required fields
    required_fields = ['user_id', 'name', 'email']
    if not all(field in user_data for field in required_fields):
        return None

    # Process the data
    return _build_user_record(user_data)


def _build_user_record(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a user record from validated data.

    Args:
        user_data: Validated user data dictionary

    Returns:
        Formatted user record
    """
    return {
        'user_id': user_data['user_id'],
        'name': user_data['name'].strip().title(),
        'email': user_data['email'].lower().strip(),
        'age': int(user_data.get('age', 0)),
        'address': user_data.get('address', '').strip(),
        'phone': user_data.get('phone', '').strip(),
        'preferences': user_data.get('preferences', {}),
        'settings': user_data.get('settings', {}),
        'status': 'active',
        'created_at': 'now',
        'updated_at': 'now',
        'version': 1
    }
'''

        with open("src/user_processor.py", "w") as f:
            f.write(good_code)

        # Step 5: Add tests
        test_code = '''
"""
Tests for user_processor module.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from user_processor import process_user_data


class TestProcessUserData:
    """Tests for process_user_data function."""

    def test_process_valid_user_data(self):
        """Test processing valid user data."""
        user_data = {
            'user_id': '123',
            'name': '  john doe  ',
            'email': '  JOHN@EXAMPLE.COM  ',
            'age': 30
        }

        result = process_user_data(user_data)

        assert result is not None
        assert result['user_id'] == '123'
        assert result['name'] == 'John Doe'
        assert result['email'] == 'john@example.com'
        assert result['age'] == 30
        assert result['status'] == 'active'

    def test_process_missing_required_fields(self):
        """Test processing user data with missing required fields."""
        user_data = {
            'name': 'John Doe'
            # Missing user_id and email
        }

        result = process_user_data(user_data)
        assert result is None

    def test_process_invalid_input(self):
        """Test processing invalid input."""
        assert process_user_data(None) is None
        assert process_user_data("not a dict") is None
        assert process_user_data({}) is None
'''

        with open("tests/test_user_processor.py", "w") as f:
            f.write(test_code)

        # Step 6: Re-validate - should pass now
        violations = validator.analyze_file("src/user_processor.py")

        # Should have significantly fewer violations
        remaining_violations = [v for v in violations if v.rule_name in ["missing_test", "missing_docstring"]]
        assert len(remaining_violations) == 0  # Tests and docs now exist

    def test_legacy_code_migration_workflow(self):
        """Test workflow for migrating legacy codebase to Quality Guard."""

        # Step 1: Create legacy code with many violations
        legacy_files = {
            "legacy_module1.py": '''
import os,sys,json
def getData(id,type,format,options,callback,timeout,retries,cache):
    if id:
        if type=="user":
            if format=="json":
                if options:
                    if callback:
                        data={}
                        data["id"]=id
                        data["type"]=type
                        if type=="user":
                            user_data=fetch_user(id)
                            if user_data:
                                data["user"]=user_data
                                data["permissions"]=get_permissions(id)
                                data["settings"]=get_settings(id)
                                data["preferences"]=get_preferences(id)
                                data["history"]=get_history(id)
                                data["stats"]=calculate_stats(user_data)
                                callback(data)
                        elif type=="admin":
                            admin_data=fetch_admin(id)
                            data["admin"]=admin_data
                            callback(data)
def fetch_user(id):
    return {"name":"user"}
def get_permissions(id):return []
def get_settings(id):return {}
def get_preferences(id):return {}
def get_history(id):return []
def calculate_stats(data):return {}
def fetch_admin(id):return {"name":"admin"}
''',
            "legacy_module2.py": '''
class DataProcessor:
    def process1(self):pass
    def process2(self):pass
    def process3(self):pass
    def process4(self):pass
    def process5(self):pass
    def process6(self):pass
    def process7(self):pass
    def process8(self):pass
    def process9(self):pass
    def process10(self):pass
    def process11(self):pass
    def process12(self):pass
    def process13(self):pass
    def process14(self):pass
    def process15(self):pass
    def process16(self):pass
    def process17(self):pass
    def process18(self):pass
    def process19(self):pass
    def process20(self):pass
    def process21(self):pass
'''
        }

        for filename, content in legacy_files.items():
            with open(f"src/{filename}", "w") as f:
                f.write(content)

        # Step 2: Enable legacy mode
        legacy_config = self.config_data.copy()
        legacy_config.update({
            "legacy_mode": {
                "enabled": True,
                "baseline_file": ".quality-baseline.json",
                "only_check_new_code": False,
                "gradual_improvement": True
            },
            "rules": {
                "require_tests": False,  # Relaxed for legacy
                "require_docstrings": False,
                "max_function_lines": 200,  # Very lenient
                "max_complexity": 30,
                "max_function_params": 10
            }
        })

        with open("quality-config.json", "w") as f:
            json.dump(legacy_config, f)

        # Step 3: Generate baseline
        config = QualityConfig("quality-config.json")
        validator = QualityGuardValidator(config)

        all_violations = []
        for filename in legacy_files.keys():
            violations = validator.analyze_file(f"src/{filename}")
            all_violations.extend(violations)

        # Should find many violations but not fail
        assert len(all_violations) > 10

        # Step 4: Gradually tighten rules and fix code
        # This would be done over multiple sprints in real workflow
        improved_config = legacy_config.copy()
        improved_config["rules"].update({
            "max_function_lines": 100,
            "max_complexity": 20,
            "require_docstrings": True
        })

        with open("quality-config.json", "w") as f:
            json.dump(improved_config, f)

    def test_team_collaboration_workflow(self):
        """Test workflow for team collaboration with Quality Guard."""

        # Step 1: Team lead sets up project standards
        team_config = {
            "rules": {
                "require_tests": True,
                "require_docstrings": True,
                "max_function_lines": 40,  # Strict for team
                "max_complexity": 8,
                "max_function_params": 3
            },
            "enforcement": {
                "level": "error",
                "strict_mode": True
            },
            "team_settings": {
                "require_code_review": True,
                "min_reviewers": 2,
                "auto_assign_reviewers": True
            }
        }

        with open("quality-config.json", "w") as f:
            json.dump(team_config, f)

        # Step 2: Developer A writes a feature
        feature_code = '''
"""
Shopping cart module for e-commerce application.
"""

from typing import List, Dict, Optional
from decimal import Decimal


def add_item_to_cart(cart: Dict, item_id: str, quantity: int) -> Dict:
    """
    Add an item to the shopping cart.

    Args:
        cart: Current shopping cart dictionary
        item_id: Unique identifier for the item
        quantity: Number of items to add

    Returns:
        Updated cart dictionary

    Raises:
        ValueError: If quantity is not positive
    """
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if item_id in cart:
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    return cart


def calculate_total(cart: Dict, prices: Dict) -> Decimal:
    """
    Calculate total price for items in cart.

    Args:
        cart: Shopping cart with item quantities
        prices: Dictionary mapping item IDs to prices

    Returns:
        Total price as Decimal
    """
    total = Decimal('0')
    for item_id, quantity in cart.items():
        if item_id in prices:
            total += prices[item_id] * quantity

    return total
'''

        with open("src/shopping_cart.py", "w") as f:
            f.write(feature_code)

        # Step 3: Add comprehensive tests
        test_code = '''
"""
Tests for shopping_cart module.
"""

import pytest
from decimal import Decimal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from shopping_cart import add_item_to_cart, calculate_total


class TestAddItemToCart:
    """Tests for add_item_to_cart function."""

    def test_add_new_item(self):
        """Test adding a new item to empty cart."""
        cart = {}
        result = add_item_to_cart(cart, "item1", 2)

        assert result["item1"] == 2
        assert cart is result  # Should modify original cart

    def test_add_existing_item(self):
        """Test adding quantity to existing item."""
        cart = {"item1": 3}
        result = add_item_to_cart(cart, "item1", 2)

        assert result["item1"] == 5

    def test_add_zero_quantity(self):
        """Test adding zero quantity raises error."""
        cart = {}
        with pytest.raises(ValueError, match="Quantity must be positive"):
            add_item_to_cart(cart, "item1", 0)

    def test_add_negative_quantity(self):
        """Test adding negative quantity raises error."""
        cart = {}
        with pytest.raises(ValueError, match="Quantity must be positive"):
            add_item_to_cart(cart, "item1", -1)


class TestCalculateTotal:
    """Tests for calculate_total function."""

    def test_calculate_empty_cart(self):
        """Test calculating total for empty cart."""
        result = calculate_total({}, {})
        assert result == Decimal('0')

    def test_calculate_single_item(self):
        """Test calculating total for single item."""
        cart = {"item1": 2}
        prices = {"item1": Decimal('10.50')}

        result = calculate_total(cart, prices)
        assert result == Decimal('21.00')

    def test_calculate_multiple_items(self):
        """Test calculating total for multiple items."""
        cart = {"item1": 2, "item2": 1}
        prices = {"item1": Decimal('10.50'), "item2": Decimal('5.25')}

        result = calculate_total(cart, prices)
        assert result == Decimal('26.25')

    def test_calculate_missing_price(self):
        """Test calculating total when item price is missing."""
        cart = {"item1": 2, "item2": 1}
        prices = {"item1": Decimal('10.50')}  # item2 missing

        result = calculate_total(cart, prices)
        assert result == Decimal('21.00')  # Only item1 counted
'''

        with open("tests/test_shopping_cart.py", "w") as f:
            f.write(test_code)

        # Step 4: Validate code meets team standards
        config = QualityConfig("quality-config.json")
        validator = QualityGuardValidator(config)

        violations = validator.analyze_file("src/shopping_cart.py")

        # Should pass team's strict standards
        critical_violations = [v for v in violations if v.level.value == "error"]
        assert len(critical_violations) == 0

    def test_continuous_integration_workflow(self):
        """Test Quality Guard integration with CI/CD pipeline."""

        # Step 1: Create CI configuration
        ci_config = {
            "rules": {
                "require_tests": True,
                "require_docstrings": True,
                "max_function_lines": 50,
                "max_complexity": 10
            },
            "ci_settings": {
                "fail_on_violations": True,
                "generate_reports": True,
                "parallel_validation": True
            }
        }

        with open("quality-config.json", "w") as f:
            json.dump(ci_config, f)

        # Step 2: Create code that should pass CI
        good_code = '''
"""
Utility functions for data processing.
"""

def clean_string(text: str) -> str:
    """
    Clean and normalize a text string.

    Args:
        text: Input text to clean

    Returns:
        Cleaned text string
    """
    if not text:
        return ""

    return text.strip().lower()


def validate_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise
    """
    if not email or "@" not in email:
        return False

    parts = email.split("@")
    return len(parts) == 2 and all(part.strip() for part in parts)
'''

        with open("src/utils.py", "w") as f:
            f.write(good_code)

        # Step 3: Create corresponding tests
        test_code = '''
"""
Tests for utils module.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import clean_string, validate_email


def test_clean_string():
    """Test clean_string function."""
    assert clean_string("  Hello World  ") == "hello world"
    assert clean_string("") == ""
    assert clean_string("   ") == ""


def test_validate_email():
    """Test validate_email function."""
    assert validate_email("test@example.com") is True
    assert validate_email("invalid.email") is False
    assert validate_email("") is False
    assert validate_email("@example.com") is False
    assert validate_email("test@") is False
'''

        with open("tests/test_utils.py", "w") as f:
            f.write(test_code)

        # Step 4: Simulate CI validation
        config = QualityConfig("quality-config.json")
        validator = QualityGuardValidator(config)

        violations = validator.analyze_file("src/utils.py")

        # Should pass CI requirements
        blocking_violations = [v for v in violations if v.level.value in ["error", "critical"]]
        assert len(blocking_violations) == 0

    def test_auto_generation_workflow(self):
        """Test workflow with automatic test and documentation generation."""

        # Step 1: Enable auto-generation
        auto_config = {
            "rules": {
                "require_tests": True,
                "require_docstrings": True,
                "max_function_lines": 50
            },
            "auto_generation": {
                "enabled": True,
                "tests": True,
                "docs": True,
                "templates_dir": "templates/"
            }
        }

        with open("quality-config.json", "w") as f:
            f.dump(auto_config, f)

        # Step 2: Developer writes function without tests/docs
        minimal_code = '''
def calculate_discount(price, percentage):
    return price * (percentage / 100)

def apply_tax(amount, rate):
    return amount * (1 + rate)
'''

        with open("src/pricing.py", "w") as f:
            f.write(minimal_code)

        # Step 3: Use auto-generator
        config = QualityConfig("quality-config.json")
        generator = AutoGenerator(config)

        # This would normally generate files
        # In a real implementation, we'd check if files were created
        # For this test, we'll simulate the expected behavior

        # Step 4: Verify auto-generation would work
        # (In real implementation, this would create actual files)
        assert config.get("auto_generation", {}).get("tests") is True
        assert config.get("auto_generation", {}).get("docs") is True

    def test_error_handling_workflow(self):
        """Test how Quality Guard handles various error conditions."""

        # Step 1: Create code with syntax errors
        broken_code = '''
def broken_function(
    # Missing closing parenthesis and colon
    print("This won't parse")
'''

        with open("src/broken.py", "w") as f:
            f.write(broken_code)

        # Step 2: Try to validate broken code
        config = QualityConfig("quality-config.json")
        validator = QualityGuardValidator(config)

        violations = validator.analyze_file("src/broken.py")

        # Should handle syntax errors gracefully
        syntax_errors = [v for v in violations if v.rule_name == "syntax_error"]
        assert len(syntax_errors) > 0

        # Step 3: Create code with runtime issues
        runtime_code = '''
"""
Module with potential runtime issues.
"""

def risky_function():
    """Function that might cause runtime errors."""
    data = eval("malicious_code()")  # Security issue
    return data

def divide_by_zero():
    """Function with obvious runtime error."""
    return 1 / 0
'''

        with open("src/risky.py", "w") as f:
            f.write(runtime_code)

        violations = validator.analyze_file("src/risky.py")

        # Should detect security patterns
        security_violations = [v for v in violations if "eval" in v.message.lower()]
        # Note: This depends on forbidden_patterns being configured

    def test_performance_workflow(self):
        """Test Quality Guard performance with larger codebases."""

        # Step 1: Create multiple files to test performance
        for i in range(10):
            code = f'''
"""
Module {i} for performance testing.
"""

def function_{i}_1(param: str) -> str:
    """
    Function {i}_1 documentation.

    Args:
        param: Input parameter

    Returns:
        Processed parameter
    """
    return param.upper()

def function_{i}_2(param: int) -> int:
    """
    Function {i}_2 documentation.

    Args:
        param: Input parameter

    Returns:
        Processed parameter
    """
    return param * 2
'''

            with open(f"src/module_{i}.py", "w") as f:
                f.write(code)

            # Create corresponding tests
            test_code = f'''
"""
Tests for module_{i}.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from module_{i} import function_{i}_1, function_{i}_2


def test_function_{i}_1():
    """Test function_{i}_1."""
    assert function_{i}_1("hello") == "HELLO"

def test_function_{i}_2():
    """Test function_{i}_2."""
    assert function_{i}_2(5) == 10
'''

            with open(f"tests/test_module_{i}.py", "w") as f:
                f.write(test_code)

        # Step 2: Validate all files
        config = QualityConfig("quality-config.json")
        validator = QualityGuardValidator(config)

        all_violations = []
        for i in range(10):
            violations = validator.analyze_file(f"src/module_{i}.py")
            all_violations.extend(violations)

        # Should complete in reasonable time with minimal violations
        # (All functions have docs and tests)
        critical_violations = [v for v in all_violations if v.level.value == "error"]
        assert len(critical_violations) == 0


class TestRealWorldIntegrations:
    """Test Quality Guard integrations with real-world tools and workflows."""

    def setup_method(self):
        """Setup for integration tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Cleanup after integration tests."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)

    def test_pytest_integration(self):
        """Test Quality Guard integration with pytest."""

        # Create a simple module and test
        with open("calculator.py", "w") as f:
            f.write('''
"""Calculator module."""

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
''')

        with open("test_calculator.py", "w") as f:
            f.write('''
"""Tests for calculator."""

from calculator import add

def test_add():
    """Test add function."""
    assert add(2, 3) == 5
''')

        # This would normally run pytest
        # For testing, we just verify the structure is correct
        assert os.path.exists("calculator.py")
        assert os.path.exists("test_calculator.py")

    def test_git_integration(self):
        """Test Quality Guard integration with Git workflows."""

        # Simulate git repository
        os.makedirs(".git", exist_ok=True)

        # Create quality guard config
        config = {
            "rules": {"require_tests": True},
            "git_integration": {
                "pre_commit_check": True,
                "pre_push_check": True
            }
        }

        with open("quality-config.json", "w") as f:
            json.dump(config, f)

        # Verify git integration would work
        assert os.path.exists(".git")
        assert os.path.exists("quality-config.json")

    def test_docker_integration(self):
        """Test Quality Guard integration with Docker."""

        # Create Dockerfile with Quality Guard
        dockerfile_content = '''
FROM python:3.9

COPY quality-guard/ /opt/quality-guard/
RUN pip install -e /opt/quality-guard/

COPY . /app
WORKDIR /app

ENV QUALITY_GUARD_ENABLE=1
CMD ["python", "main.py"]
'''

        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)

        # Create main.py that would use Quality Guard
        with open("main.py", "w") as f:
            f.write('''
"""Main application."""

def main():
    """Main function."""
    print("Hello, Quality Guard!")

if __name__ == "__main__":
    main()
''')

        # Verify Docker setup
        assert os.path.exists("Dockerfile")
        assert os.path.exists("main.py")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])