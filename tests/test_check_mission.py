import pytest
from pathlib import Path
from src.check_mission import validate_paths, validate_ini_file, write_validation_report
from src.core.validator import MissionValidator
from src.core.database import ClassDatabase
import tempfile
import yaml

@pytest.fixture
def temp_mission_dir():
    """Create temporary mission directory"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir)
        # Create some test files
        (path / "mission.sqm").touch()
        (path / "description.ext").touch()
        return path

@pytest.fixture
def temp_ini_file():
    """Create temporary INIDBI config file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write("""[CategoryData_Vehicles]
1="Car,vanilla,vehicles,Vehicle,,false,5,2,"
2="Truck,mod_x,vehicles,Car,,false,7,2,"
""")
        return Path(f.name)

def test_validate_paths():
    """Test path validation logic"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Create test paths
        valid_path = tmp_path / "exists"
        valid_path.touch()
        missing_path = tmp_path / "missing"
        
        paths = {
            "Valid": valid_path,
            "Missing": missing_path
        }
        
        result = validate_paths(paths)
        assert result is not None
        assert "Missing" in result
        assert "Valid" not in result

def test_validate_ini_file(temp_ini_file):
    """Test INIDBI config validation"""
    result = validate_ini_file(temp_ini_file)
    assert result is None
    
    # Test missing file
    result = validate_ini_file(Path("nonexistent.ini"))
    assert result is not None
    assert "not found" in result

def test_write_validation_report(temp_mission_dir):
    """Test report generation"""
    database = ClassDatabase()
    validator = MissionValidator(
        cache_dir=Path(temp_mission_dir) / ".cache",
        database=database
    )
    
    # Add some test validation data
    test_summary = {
        'missions': {
            'test_mission': {
                'total_classes': 10,
                'found_in_database': 8,
                'missing_from_database': 2,
                'classes': [
                    {'name': 'TestClass1', 'found_in_database': True},
                    {'name': 'TestClass2', 'found_in_database': False}
                ]
            }
        },
        'warnings': ['Test warning']
    }
    
    # Mock the get_validation_summary method
    validator.get_validation_summary = lambda: test_summary
    
    report_path = write_validation_report(validator, temp_mission_dir)
    assert report_path.exists()
    
    # Check YAML report
    yaml_path = report_path.with_suffix('.yml')
    assert yaml_path.exists()
    
    with open(yaml_path) as f:
        yaml_data = yaml.safe_load(f)
        assert yaml_data['missions']['test_mission']['total_classes'] == 10
        assert len(yaml_data['warnings']) == 1
