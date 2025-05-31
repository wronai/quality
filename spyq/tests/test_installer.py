"""
Tests for the QualityGuardInstaller class.
"""

import os
import sys
import shutil
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from spyq.setup_quality_guard import QualityGuardInstaller

class TestQualityGuardInstaller:
    """Tests for the QualityGuardInstaller class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = Path("test_temp_dir")
        self.temp_dir.mkdir(exist_ok=True)
        self.installer = QualityGuardInstaller()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_create_setup_py(self):
        """Test creating setup.py file."""
        setup_path = self.temp_dir / "setup.py"
        self.installer._create_setup_py()
        assert setup_path.exists()
        
        content = setup_path.read_text()
        assert "setuptools" in content
        assert "quality-guard" in content
    
    def test_create_pyproject_toml(self):
        """Test creating pyproject.toml file."""
        toml_path = self.temp_dir / "pyproject.toml"
        self.installer._create_pyproject_toml()
        assert toml_path.exists()
        
        content = toml_path.read_text()
        assert "[build-system]" in content
        assert "quality-guard" in content
    
    @patch("subprocess.run")
    def test_install_option_1_pip_package(self, mock_run):
        """Test pip package installation option."""
        # Mock subprocess.run to simulate successful pip install
        mock_run.return_value.returncode = 0
        
        # Create dummy setup.py and pyproject.toml
        (self.temp_dir / "setup.py").write_text("# Dummy setup.py")
        (self.temp_dir / "pyproject.toml").write_text("# Dummy pyproject.toml")
        
        result = self.installer.install_option_1_pip_package()
        assert result is True
        assert mock_run.called
    
    @patch("builtins.print")
    def test_install_option_3_project_local(self, mock_print):
        """Test local project installation option."""
        # Create source directory structure
        (self.temp_dir / "core").mkdir(exist_ok=True)
        (self.temp_dir / "core" / "quality_guard_exceptions.py").write_text("# Dummy")
        (self.temp_dir / "config").mkdir(exist_ok=True)
        (self.temp_dir / "config" / "quality-config.json").write_text("{}")
        (self.temp_dir / "wrappers").mkdir(exist_ok=True)
        (self.temp_dir / "wrappers" / "python-quality-wrapper.py").write_text("# Dummy")
        (self.temp_dir / "wrappers" / "nodejs-quality-wrapper.js").write_text("// Dummy")
        
        # Set is_source_dir to True for this test
        self.installer.is_source_dir = True
        
        result = self.installer.install_option_3_project_local()
        assert result is True
        
        # Check if files were created
        assert (self.temp_dir / "demo_project").exists()
        assert (self.temp_dir / "demo_project" / "quality_guard_activator.py").exists()
        assert (self.temp_dir / "demo_project" / "run_with_quality.py").exists()
        
        # Check if demo files were created
        assert (self.temp_dir / "demo_project" / "main.py").exists()
        assert (self.temp_dir / "demo_project" / "src" / "good_example.py").exists()
        assert (self.temp_dir / "demo_project" / "tests" / "test_good_example.py").exists()
    
    @patch("builtins.input", side_effect=["1"])  # Choose option 1
    @patch.object(QualityGuardInstaller, 'install_option_1_pip_package', return_value=True)
    def test_interactive_install_option_1(self, mock_install, mock_input):
        """Test interactive installation with option 1."""
        self.installer.interactive_install()
        mock_install.assert_called_once()
    
    @patch("builtins.input", side_effect=["invalid", "1"])  # Invalid input, then option 1
    @patch.object(QualityGuardInstaller, 'install_option_1_pip_package', return_value=True)
    def test_interactive_install_invalid_input(self, mock_install, mock_input):
        """Test interactive installation with invalid input."""
        self.installer.interactive_install()
        mock_install.assert_called_once()
    
    @patch("builtins.input", side_effect=KeyboardInterrupt())
    def test_interactive_install_keyboard_interrupt(self, mock_input):
        """Test handling of keyboard interrupt during interactive install."""
        with pytest.raises(SystemExit):
            self.installer.interactive_install()
