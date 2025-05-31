"""
Tests for good_example module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from good_example import process_user_data, calculate_sum


def test_process_user_data_valid():
    """Test processing valid user data."""
    user_data = {
        "user_id": "123",
        "name": "  john doe  ",
        "email": "  JOHN@EXAMPLE.COM  "
    }

    result = process_user_data(user_data)

    assert result is not None
    assert result["user_id"] == "123"
    assert result["name"] == "John Doe"
    assert result["email"] == "john@example.com"
    assert result["status"] == "active"


def test_process_user_data_invalid():
    """Test processing invalid user data."""
    assert process_user_data(None) is None
    assert process_user_data({}) is None
    assert process_user_data({"user_id": "123"}) is None  # Missing required fields


def test_calculate_sum():
    """Test calculate_sum function."""
    assert calculate_sum([1, 2, 3, 4, 5]) == 15
    assert calculate_sum([]) == 0
    assert calculate_sum([-1, 1]) == 0
