"""Shared pytest fixtures for the test suite."""
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    # Cleanup after test
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_file(temp_dir):
    """Create a temporary file in the temp directory."""
    def _make_temp_file(name="test_file.txt", content=""):
        file_path = temp_dir / name
        file_path.write_text(content)
        return file_path
    return _make_temp_file


@pytest.fixture
def mock_config():
    """Create a mock configuration object."""
    config = Mock()
    config.debug = False
    config.verbose = True
    config.timeout = 30
    config.max_retries = 3
    return config


@pytest.fixture
def mock_network_response():
    """Create a mock network response."""
    response = Mock()
    response.status_code = 200
    response.text = "Mock response content"
    response.json.return_value = {"status": "success", "data": []}
    response.headers = {"Content-Type": "application/json"}
    return response


@pytest.fixture
def mock_socket():
    """Create a mock socket object."""
    sock = MagicMock()
    sock.connect.return_value = None
    sock.send.return_value = 10
    sock.recv.return_value = b"Mock data"
    sock.close.return_value = None
    return sock


@pytest.fixture
def sample_pcap_data():
    """Provide sample PCAP packet data for testing."""
    # This would contain mock packet data
    # In real tests, you might load actual test PCAP files
    return b"\xd4\xc3\xb2\xa1\x02\x00\x04\x00"  # PCAP magic number


@pytest.fixture
def sample_credentials():
    """Provide sample credentials for testing."""
    return {
        "username": "test_user",
        "password": "test_pass",
        "host": "127.0.0.1",
        "port": 22
    }


@pytest.fixture
def mock_ssh_client():
    """Create a mock SSH client."""
    client = Mock()
    client.connect.return_value = None
    client.exec_command.return_value = (
        Mock(),  # stdin
        Mock(read=lambda: b"command output"),  # stdout
        Mock(read=lambda: b"")  # stderr
    )
    client.close.return_value = None
    return client


@pytest.fixture
def sample_pdf_content():
    """Provide sample PDF content for testing."""
    # Minimal PDF structure
    return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n%%EOF"


@pytest.fixture
def sample_html_content():
    """Provide sample HTML content for testing."""
    return """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <h1>Test Content</h1>
        <img src="test.jpg" alt="Test Image">
        <p>Sample paragraph</p>
    </body>
    </html>
    """


@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment variables for each test."""
    # Store original environment
    original_env = os.environ.copy()
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def capture_stdout(monkeypatch):
    """Capture stdout for testing print statements."""
    import io
    import sys
    
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)
    
    yield captured_output
    
    # Reset stdout
    monkeypatch.undo()


# Markers for test organization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "network: mark test as requiring network access"
    )
    config.addinivalue_line(
        "markers", "skipif_no_bluetooth: skip if bluetooth is not available"
    )