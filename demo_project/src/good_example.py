"""
Good example module demonstrating Quality Guard compliance.
"""

from typing import Dict, Any, Optional


def process_user_data(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process and validate user data input.

    Args:
        user_data: Dictionary containing user information

    Returns:
        Processed user data or None if invalid

    Example:
        >>> data = {"user_id": "123", "name": "John", "email": "john@example.com"}
        >>> result = process_user_data(data)
        >>> result["status"]
        'active'
    """
    if not user_data or not isinstance(user_data, dict):
        return None

    required_fields = ["user_id", "name", "email"]
    if not all(field in user_data for field in required_fields):
        return None

    return _build_user_record(user_data)


def _build_user_record(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build formatted user record from validated data.

    Args:
        user_data: Validated user data dictionary

    Returns:
        Formatted user record
    """
    return {
        "user_id": user_data["user_id"],
        "name": user_data["name"].strip().title(),
        "email": user_data["email"].lower().strip(),
        "status": "active",
        "created_at": "now"
    }


def calculate_sum(numbers: list) -> int:
    """
    Calculate sum of a list of numbers.

    Args:
        numbers: List of numbers to sum

    Returns:
        Sum of all numbers

    Example:
        >>> calculate_sum([1, 2, 3, 4, 5])
        15
    """
    return sum(numbers)
