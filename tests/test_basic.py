"""
Basic tests for Personal AI Advisor
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_imports():
    """Test that all required modules can be imported"""
    try:
        import streamlit
        import pandas
        import PyPDF2
        import docx
        assert True
    except ImportError as e:
        assert False, f"Import failed: {e}"


def test_app_file_exists():
    """Test that app.py exists"""
    app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
    assert os.path.exists(app_path), "app.py not found"


def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    assert os.path.exists(req_path), "requirements.txt not found"


def test_dockerfile_exists():
    """Test that Dockerfile exists"""
    dockerfile_path = os.path.join(os.path.dirname(__file__), '..', 'Dockerfile')
    assert os.path.exists(dockerfile_path), "Dockerfile not found"


def test_app_syntax():
    """Test that app.py has valid Python syntax"""
    app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
    with open(app_path, 'r', encoding='utf-8') as f:
        code = f.read()
    try:
        compile(code, 'app.py', 'exec')
        assert True
    except SyntaxError as e:
        assert False, f"Syntax error in app.py: {e}"


if __name__ == "__main__":
    print("Running basic tests...")
    test_imports()
    print("✅ Import test passed")
    test_app_file_exists()
    print("✅ App file exists")
    test_requirements_file_exists()
    print("✅ Requirements file exists")
    test_dockerfile_exists()
    print("✅ Dockerfile exists")
    test_app_syntax()
    print("✅ Python syntax valid")
    print("🎉 All tests passed!")