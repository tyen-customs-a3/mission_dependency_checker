import os
import sys
from pathlib import Path
import pytest
import tempfile
import shutil

# Add the src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def mock_database(temp_dir):
    db_path = temp_dir / "test.db"
    from src.core.database import ClassDatabase
    return ClassDatabase(db_path)