import pytest
from pathlib import Path
import tempfile
import shutil
from src.core.scanner import AssetScanner
from src.core.parser_class import ClassParser
from src.core.parser_ini import InidbiParser
from src.core.database import ClassDatabase
from src.core.models import ClassDef, Asset

# === Fixtures ===

@pytest.fixture
def temp_dir():
    """Provide temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def cache_dir(temp_dir):
    """Set up temporary cache directory"""
    cache_path = temp_dir / ".cache"
    cache_path.mkdir()
    return cache_path

@pytest.fixture
def sample_class_file(temp_dir):
    """Create sample class definition file"""
    content = """
    class Vehicle {
        displayName = "Base Vehicle";
        scope = 2;
    };
    
    class Car: Vehicle {
        maxSpeed = 100;
        class Wheels {
            count = 4;
            material = "rubber";
        };
    };
    """
    file_path = temp_dir / "classes.cpp"
    file_path.write_text(content)
    return file_path

@pytest.fixture
def sample_inidbi_file(temp_dir):
    """Create sample INIDBI2 sformat file"""
    content = """
    [CategoryData_Vehicles]
    1=Car,vanilla,vehicles,Vehicle,,true,5,2,"a3/car.p3d"
    2=Truck,mod_x,vehicles,Car,,true,7,2,"x/truck.p3d"
    """
    file_path = temp_dir / "vehicles.ini"
    file_path.write_text(content)
    return file_path

@pytest.fixture
def sample_loadout_file(temp_dir):
    """Copy and provide sample loadout file"""
    loadout_path = Path(__file__).parent / "blufor_loadout.hpp"
    if not loadout_path.exists():
        pytest.skip("blufor_loadout.hpp not found in tests directory")
    return loadout_path

# === Scanner Tests ===

def test_scan_directory(temp_dir, cache_dir):
    """Test basic asset scanning"""
    # Create test files
    (temp_dir / "texture.paa").touch()
    (temp_dir / "model.p3d").touch()
    (temp_dir / "script.sqf").touch()
    (temp_dir / "ignored.txt").touch()
    
    scanner = AssetScanner(cache_dir)
    assets = scanner.scan_directory(temp_dir)
    
    assert len(assets) == 3  # Should find 3 valid assets
    
    extensions = {a.path.suffix for a in assets}
    assert extensions == {".paa", ".p3d", ".sqf"}

def test_scan_caching(temp_dir, cache_dir):
    """Test that scanning uses cache correctly"""
    test_file = temp_dir / "test.paa"
    test_file.touch()
    
    scanner = AssetScanner(cache_dir)
    
    assets1 = scanner.scan_directory(temp_dir)
    assert len(assets1) == 1
    
    assets2 = scanner.scan_directory(temp_dir)
    assert len(assets2) == 1
    
    assert next(iter(assets1)).checksum == next(iter(assets2)).checksum

def test_scan_arma3_install(cache_dir):
    """Test scanning limited set of ARMA 3 files."""
    arma3_path = Path("C:/Program Files (x86)/Steam/steamapps/common/Arma 3")
    if not arma3_path.exists():
        pytest.skip("Arma 3 folder not found, skipping test.")
        
    scanner = AssetScanner(cache_dir)
    assets = scanner.scan_directory(arma3_path, max_files=10)  # Only scan 10 files
    
    assert 0 < len(assets) <= 10, "Expected to find up to 10 assets"
    assert all(isinstance(a, Asset) for a in assets), "All results should be Asset objects"

def test_scan_pca_modpack(cache_dir):
    """Optionally scan PCA modpack if present."""
    pca_path = Path("C:/pca")
    if not pca_path.exists():
        pytest.skip("PCA modpack folder not found, skipping test.")
    scanner = AssetScanner(cache_dir)
    assets = scanner.scan_directory(pca_path, max_files=10)  # Only scan 10 files
    assert len(assets) > 0, "Expected to find assets in PCA modpack."

# === Parser Tests ===

def test_parse_basic_class(sample_class_file):
    parser = ClassParser()
    # Basic class parsing - don't treat as mission file
    classes = parser.parse_file(sample_class_file, treat_as_mission=False)
    
    assert len(classes) == 3, f"Expected exactly 3 classes, got {len(classes)}: {[c.name for c in classes]}"
    
    # Check for specific class names
    class_names = {c.name for c in classes}
    expected_names = {"Vehicle", "Car", "Car.Wheels"}
    assert class_names == expected_names, f"Expected {expected_names}, got {class_names}"
    
    # Check that nested Wheels class is found
    wheels = next((c for c in classes if c.name == "Car.Wheels"), None)
    assert wheels is not None, "Nested Wheels class not found"
    assert "count" in wheels.properties, "Wheels class missing count property"
    assert wheels.properties["count"] == "4", "Wheels count property incorrect"

def test_inheritance_graph(temp_dir):
    """Test building and querying inheritance graph"""
    parser = ClassParser()
    
    classes = {
        ClassDef("Vehicle", None, "base", {}),
        ClassDef("Car", "Vehicle", "mod1", {}),
        ClassDef("Truck", "Car", "mod2", {}),
        ClassDef("Bus", "Car", "mod2", {})
    }
    
    parser.build_inheritance_graph(classes)
    
    derived = parser.get_derived_classes("Vehicle")
    assert derived == {"Car", "Truck", "Bus"}
    
    car_derived = parser.get_derived_classes("Car")
    assert car_derived == {"Truck", "Bus"}

def test_class_usage_analysis(temp_dir):
    """Test analysis of class usage patterns"""
    parser = ClassParser()
    
    classes = {
        ClassDef("Vehicle", None, "base", {"type": "land"}),
        ClassDef("Car", "Vehicle", "mod1", {
            "parent": "Vehicle",
            "cargo": "CargoBox"
        }),
        ClassDef("CargoBox", None, "mod1", {})
    }
    
    usage = parser.analyze_class_usage(classes)
    
    assert usage["Vehicle"]["child_count"] == 1
    assert usage["CargoBox"]["reference_count"] == 1

def test_circular_inheritance_detection(temp_dir):
    """Test detection of circular inheritance"""
    parser = ClassParser()
    
    classes = {
        ClassDef("A", "C", "mod1", {}),
        ClassDef("B", "A", "mod1", {}),
        ClassDef("C", "B", "mod1", {})
    }
    
    warnings = parser.validate_class_hierarchy(classes.pop(), classes)
    assert any("Circular inheritance" in w for w in warnings)

def test_parse_loadout_file(sample_loadout_file):
    parser = ClassParser()
    # Loadout parsing - treat as mission file (default behavior)
    classes = parser.parse_file(sample_loadout_file)
    
    # Verify equipment references are found
    equipment_refs = {c.name for c in classes}  # All classes should be references now
    expected_items = {
        "ACRE_PRC343",
        "ACE_fieldDressing",
        "ACE_packingBandage", 
        "ACE_epinephrine",
        "ACE_morphine",
        "ACE_bloodIV",
        "ACE_splint",
        "ACE_surgicalKit",
        "rhs_weap_rpg7",
        "rhs_rpg7_PG7VL_mag",
        "CUP_30Rnd_45ACP_Green_Tracer_MAC10_M",
        "pca_backpack_invisible_large",
        "pca_vest_invisible_plate"
    }
    
    assert expected_items.issubset(equipment_refs), \
        f"Missing equipment references. Expected {expected_items - equipment_refs}"
    
    # Verify LIST macro expansions are captured
    list_refs = {c for c in classes if 'list_count' in c.properties}
    
    # Check a few specific LIST items
    field_dressing = next((c for c in list_refs if c.name == "ACE_fieldDressing"), None)
    assert field_dressing is not None, "ACE_fieldDressing not found"
    assert field_dressing.properties["list_count"] == "20"
    
    rpg_mag = next((c for c in list_refs if c.name == "rhs_rpg7_PG7VL_mag"), None)
    assert rpg_mag is not None, "rhs_rpg7_PG7VL_mag not found"
    assert rpg_mag.properties["list_count"] == "10"

# === INIDBI Parser Tests ===

def test_parse_inidbi_format(temp_dir):
    """Test INIDBI2 format parsing"""
    file_source = Path("D:/git/mission_checker/data/ConfigExtract_pca.ini")
    if not file_source.exists():
        pytest.skip("ConfigExtract_pca.ini not found, skipping test.")
        
    parser = InidbiParser()
    classes_by_source = parser.parse_file(file_source)

    # Check sources are present
    assert "@cup_terrain_core" in classes_by_source
    assert "curator" in classes_by_source
    assert "A3" in classes_by_source

def test_class_lookup(sample_inidbi_file):
    """Test exact class name lookup"""
    parser = InidbiParser()
    classes_by_source = parser.parse_file(sample_inidbi_file)

    # Test exact class lookup
    truck_class = parser.get_class("Truck")
    assert truck_class is not None
    assert truck_class.source == "mod_x"
    assert truck_class.properties["Parent"] == "Car"
    
    # Test pattern matching using Car.*
    car_classes = parser.find_classes("Car.*")
    assert len(car_classes) == 1
    assert next(iter(car_classes)).name == "Car"

    # Test non-existent class
    assert parser.get_class("NonExistent") is None

def test_parse_config_extract_pca():
    """Test parsing of ConfigExtract_pca.ini file"""
    file_source = Path("D:/git/mission_checker/data/ConfigExtract_pca.ini")
    if not file_source.exists():
        pytest.skip("ConfigExtract_pca.ini not found, skipping test.")
        
    parser = InidbiParser()
    classes_by_source = parser.parse_file(file_source)
    assert classes_by_source, "Expected to parse at least one class from ConfigExtract_pca.ini"

    # Test looking up specific classes
    # 7=""USP_GearUniforms,@usp,CfgMods,CfgMods,Mod_Base,false,15,0,""
    # 8=""Curator,curator,CfgMods,CfgMods,Mod_Base,false,20,0,""
    # 9=""Kart,kart,CfgMods,CfgMods,Mod_Base,false,35,0,""
    
    usp_gear = parser.get_class("USP_GearUniforms")
    assert usp_gear is not None
    assert usp_gear.source == "@usp"
    assert usp_gear.properties["NumProperties"] == "15"
    assert usp_gear.properties["Parent"] == "CfgMods"
    
    curator = parser.get_class("Curator")
    assert curator is not None
    assert curator.source == "curator"
    
    kart = parser.get_class("Kart")
    assert kart is not None
    assert kart.source == "kart"


# === Database Tests ===

@pytest.fixture
def in_memory_db():
    """Provide in-memory database for tests"""
    db = ClassDatabase()
    try:
        yield db
    finally:
        db.close()

def test_add_and_retrieve_class(in_memory_db):
    """Test adding and retrieving class definitions with inheritance"""
    # Add base vehicle class
    base_vehicle = ClassDef(
        name="Vehicle",
        parent=None,
        properties={"displayName": "Base Vehicle", "scope": "2"},
        source="base_mod"
    )
    in_memory_db.add_class(base_vehicle)
    
    # Add derived test vehicle class
    test_vehicle = ClassDef(
        name="TestVehicle",
        parent="Vehicle",
        properties={"displayName": "Test", "scope": "2"},
        source="test_mod"
    )
    in_memory_db.add_class(test_vehicle)

    # Add further derived class
    test_truck = ClassDef(
        name="TestTruck",
        parent="TestVehicle",
        properties={"cargoCapacity": "100"},
        source="test_mod"
    )
    in_memory_db.add_class(test_truck)

    # Test basic class retrieval
    history = in_memory_db.get_class_history("TestVehicle")
    assert len(history) == 1
    assert history[0].name == "TestVehicle"
    assert history[0].parent == "Vehicle"

    # Test inheritance chain retrieval
    chain = in_memory_db.get_inheritance_chain("TestTruck")
    assert len(chain) == 3, "Should find complete inheritance chain"
    assert [c.name for c in chain] == ["TestTruck", "TestVehicle", "Vehicle"]
    
    # Test properties are preserved
    assert chain[0].properties["cargoCapacity"] == "100"
    assert chain[1].properties["displayName"] == "Test"
    assert chain[2].properties["displayName"] == "Base Vehicle"

    # Verify case-insensitive lookup
    assert in_memory_db.get_class("testvehicle"), "Should find class with case-insensitive lookup"
    assert in_memory_db.get_class("TESTVEHICLE"), "Should find class with uppercase lookup"

