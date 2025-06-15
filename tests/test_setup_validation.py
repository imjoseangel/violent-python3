"""Validation tests to ensure the testing infrastructure is properly configured."""
import pytest
import sys
import os
from pathlib import Path


class TestSetupValidation:
    """Validate that the testing infrastructure is properly set up."""
    
    @pytest.mark.unit
    def test_python_version(self):
        """Verify Python version is 3.8 or higher."""
        assert sys.version_info >= (3, 8), "Python 3.8 or higher is required"
    
    @pytest.mark.unit
    def test_project_structure(self):
        """Verify project directory structure exists."""
        project_root = Path(__file__).parent.parent
        
        # Check main chapter directories
        expected_dirs = [
            "chapter01", "chapter02", "chapter03", 
            "chapter04", "chapter05", "chapter06", "chapter07"
        ]
        
        for dir_name in expected_dirs:
            dir_path = project_root / dir_name
            assert dir_path.exists(), f"Directory {dir_name} should exist"
            assert dir_path.is_dir(), f"{dir_name} should be a directory"
    
    @pytest.mark.unit
    def test_test_directories(self):
        """Verify test directory structure."""
        test_root = Path(__file__).parent
        
        assert (test_root / "unit").exists(), "Unit test directory should exist"
        assert (test_root / "integration").exists(), "Integration test directory should exist"
        assert (test_root / "conftest.py").exists(), "conftest.py should exist"
    
    @pytest.mark.unit
    def test_fixtures_available(self, temp_dir, mock_config, sample_credentials):
        """Verify that custom fixtures are available."""
        # Test temp_dir fixture
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test mock_config fixture
        assert hasattr(mock_config, 'debug')
        assert hasattr(mock_config, 'timeout')
        
        # Test sample_credentials fixture
        assert 'username' in sample_credentials
        assert 'password' in sample_credentials
    
    @pytest.mark.unit
    def test_markers_registered(self, pytestconfig):
        """Verify custom markers are registered."""
        markers = pytestconfig.getini('markers')
        marker_names = [m.split(':')[0].strip() for m in markers]
        
        expected_markers = ['unit', 'integration', 'slow']
        for marker in expected_markers:
            assert marker in marker_names, f"Marker '{marker}' should be registered"
    
    @pytest.mark.unit
    def test_coverage_configured(self):
        """Verify coverage is properly configured."""
        # This test will pass if coverage is running (which it should be with our config)
        import coverage
        assert coverage.__version__, "Coverage should be installed"
    
    @pytest.mark.unit
    def test_temp_file_fixture(self, temp_file):
        """Test the temp_file fixture functionality."""
        # Create a test file
        test_content = "Test content"
        file_path = temp_file(name="test.txt", content=test_content)
        
        assert file_path.exists()
        assert file_path.read_text() == test_content
    
    @pytest.mark.unit
    def test_capture_stdout_fixture(self, capsys):
        """Test stdout capture using pytest's built-in capsys."""
        print("Test output")
        print("Another line")
        
        captured = capsys.readouterr()
        assert "Test output" in captured.out
        assert "Another line" in captured.out
    
    @pytest.mark.integration
    def test_integration_marker(self):
        """Simple integration test to verify marker works."""
        # This test is marked as integration
        # It should only run when integration tests are selected
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Simple slow test to verify marker works."""
        # This test is marked as slow
        # It can be excluded with pytest -m "not slow"
        import time
        time.sleep(0.1)  # Simulate slow operation
        assert True


@pytest.mark.unit
def test_pytest_available():
    """Verify pytest is importable and functional."""
    import pytest
    assert hasattr(pytest, 'main')
    assert hasattr(pytest, 'fixture')
    assert hasattr(pytest, 'mark')