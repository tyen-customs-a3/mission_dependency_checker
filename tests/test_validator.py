import pytest
from pathlib import Path
from src.core.validator import MissionValidator, MissionValidationError
from src.core.database import ClassDatabase
from src.core.models import ClassDef
import tempfile

@pytest.fixture
def database():
    """Provide test database with some classes"""
    db = ClassDatabase()
    db.add_class(ClassDef("BaseVehicle", None, "test", {}))
    db.add_class(ClassDef("Car", "BaseVehicle", "test", {}))
    db.add_class(ClassDef("Truck", "Car", "test", {}))
    return db

@pytest.fixture
def validator(database):
    """Provide configured validator"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        cache_dir = Path(tmp_dir) / ".cache"
        cache_dir.mkdir()
        return MissionValidator(
            cache_dir=cache_dir,
            database=database
        )

def test_validate_empty_mission(validator, tmp_path):
    """Test validation of empty mission folder"""
    with pytest.raises(MissionValidationError) as exc:
        validator.validate_mission_folder(tmp_path)
    assert "Mission folder is empty" in str(exc.value)

def test_validate_basic_mission(validator, tmp_path):
    """Test validation of basic mission structure"""
    # Create minimal mission structure
    mission_path = tmp_path / "test_mission.vr"
    mission_path.mkdir()
    
    # Create test files
    (mission_path / "mission.sqm").write_text("""
class Vehicles {
    class Car_1 {
        vehicle = "Car";
    };
};
""")
    
    (mission_path / "description.ext").write_text("""
class CfgVehicles {
    class Truck_1: Truck {};
};
""")
    
    warnings = validator.validate_mission_folder(mission_path)
    assert len(warnings) == 0  # Should find valid classes

def test_get_missing_items_report(validator, tmp_path):
    """Test missing items report generation"""
    mission_path = tmp_path / "test_mission.vr"
    mission_path.mkdir()
    
    # Add a loadout file with a non-existent equipment reference
    (mission_path / "loadout.hpp").write_text("""
class baseMan {
    displayName = "Rifleman";
    items[] = {
        "NonExistentMedkit",
        LIST_2("ACRE_PRC343")
    };
    linkedItems[] = {
        "NonExistentNVG",
        "ItemCompass"
    };
};
""")
    
    validator.validate_mission_folder(mission_path)
    report = validator.get_missing_items_report()
    
    # Check that missing equipment is reported
    assert "Missing Equipment References" in report
    assert "NonExistentMedkit" in report
    assert "NonExistentNVG" in report

def test_validation_error_handling(validator, tmp_path):
    """Test error handling during validation"""
    non_existent = tmp_path / "non_existent"
    
    with pytest.raises(MissionValidationError) as exc:
        validator.validate_mission_folder(non_existent)
    assert "does not exist" in str(exc.value)

def test_cache_functionality(validator, tmp_path):
    """Test caching of validation results"""
    mission_path = tmp_path / "test_mission.vr"
    mission_path.mkdir()
    
    # Create test file
    (mission_path / "mission.sqm").write_text("""
class Vehicles {
    class Car_1 {
        vehicle = "Car";
    };
};
""")
    
    # First validation
    warnings1 = validator.validate_mission_folder(mission_path)
    
    # Second validation - should use cache
    warnings2 = validator.validate_mission_folder(mission_path)
    
    assert warnings1 == warnings2  # Results should be identical
