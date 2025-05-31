""
Tests for the SPYQ CLI.
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from spyq.cli import main, parse_args

def test_parse_args_setup():
    """Test parsing setup command arguments."""
    args = ["setup", "--path", "/test/path", "--force"]
    parsed = parse_args(args)
    assert parsed.command == "setup"
    assert parsed.path == "/test/path"
    assert parsed.force is True

def test_parse_args_version():
    """Test parsing version command."""
    args = ["version"]
    parsed = parse_args(args)
    assert parsed.command == "version"

@patch("spyq.cli.setup_quality_guard")
def test_main_setup(mock_setup):
    """Test main function with setup command."""
    test_path = "/test/path"
    with patch("sys.argv", ["spyq", "setup", "--path", test_path]):
        result = main()
        assert result == 0
        mock_setup.assert_called_once_with(Path(test_path).resolve(), force=False)

@patch("builtins.print")
def test_main_version(mock_print):
    """Test main function with version command."""
    with patch("sys.argv", ["spyq", "version"]):
        result = main()
        assert result == 0
        mock_print.assert_called()

@patch("spyq.cli.setup_quality_guard")
def test_main_error_handling(mock_setup):
    """Test error handling in main function."""
    mock_setup.side_effect = Exception("Test error")
    with patch("sys.argv", ["spyq", "setup"]):
        result = main()
        assert result == 1
