import pytest
from pathlib import Path
import tempfile
import shutil
from src.core.scanner import AssetScanner
from src.core.parser import ClassParser, InidbiParser
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
    """Create sample INIDBI2 format file"""
    content = """
    [CategoryData_Vehicles]
    1=Car,vanilla,vehicles,Vehicle,,true,5,2,"a3\car.p3d"
    2=Truck,mod_x,vehicles,Car,,true,7,2,"x\truck.p3d"
    """
    file_path = temp_dir / "vehicles.ini"
    file_path.write_text(content)
    return file_path

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
    classes = parser.parse_file(sample_class_file)
    
    assert len(classes) == 3
    
    vehicle = next((c for c in classes if c.name == "Vehicle"), None)
    assert vehicle is not None
    assert vehicle.parent is None
    assert vehicle.properties["displayName"] == '"Base Vehicle"'
    assert vehicle.properties["scope"] == "2"
    
    car = next((c for c in classes if c.name == "Car"), None)
    assert car is not None
    assert car.parent == "Vehicle"
    assert car.properties["maxSpeed"] == "100"
    
    wheels = next((c for c in classes if c.name == "Car.Wheels"), None)
    assert wheels is not None
    assert wheels.properties["count"] == "4"
    assert wheels.properties["material"] == '"rubber"'

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

# === INIDBI Parser Tests ===

def test_parse_inidbi_format(temp_dir):
    """Test INIDBI2 format parsing"""
    content = """
[CategoryData_CfgVehicles]
header="ClassName,Source,Category,Parent,InheritsFrom,IsSimpleObject,NumProperties,Scope,Model"
0="All,@cup_terrain_core,CfgVehicles,CfgVehicles,,false,313,0,\\A3\\Weapons_F\\empty.p3d"
1="Logic,curator,CfgVehicles,CfgVehicles,All,false,15,2,\\A3\\Weapons_f\\empty"
2="AllVehicles,curator,CfgVehicles,CfgVehicles,All,false,65,0,\\A3\\Weapons_F\\empty.p3d"

[CategoryData_CfgWeapons]
header="ClassName,Source,Category,Parent,InheritsFrom,IsSimpleObject,NumProperties,Scope,Model"
0="Default,A3,CfgWeapons,CfgWeapons,,false,133,0,"
1="PistolCore,A3,CfgWeapons,CfgWeapons,Default,false,4,0,"
"""
    test_file = temp_dir / "config.ini"
    test_file.write_text(content)
    
    parser = InidbiParser()
    classes = parser.parse_file(test_file)
    
    # Check sources
    assert "@cup_terrain_core" in classes
    assert "curator" in classes
    assert "A3" in classes
    
    # Check vehicle class
    logic = next(c for c in classes["curator"] if c.name == "Logic")
    assert logic.parent == "CfgVehicles"
    assert logic.inidbi_meta.inherits_from == "All"
    assert logic.inidbi_meta.scope == 2
    assert logic.inidbi_meta.model == "\\A3\\Weapons_f\\empty"
    
    # Check weapon class
    pistol = next(c for c in classes["A3"] if c.name == "PistolCore")
    assert pistol.parent == "CfgWeapons"
    assert pistol.inidbi_meta.inherits_from == "Default"
    assert pistol.inidbi_meta.scope == 0
    assert pistol.inidbi_meta.num_properties == 4

def test_parse_config_extract_pca():
    """Test parsing of ConfigExtract_pca.ini file"""
    file_source = Path("D:/git/mission_checker/data/ConfigExtract_pca.ini")
    if not file_source.exists():
        pytest.skip("ConfigExtract_pca.ini not found, skipping test.")
    parser = InidbiParser()
    classes = parser.parse_file(file_source)
    assert classes, "Expected to parse at least one class from ConfigExtract_pca.ini"

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
    """Test adding and retrieving class definitions"""
    test_class = ClassDef(
        name="TestVehicle",
        parent="Vehicle",
        properties={"displayName": "Test", "scope": "2"},
        source="test_mod"
    )
    in_memory_db.add_class(test_class)

    history = in_memory_db.get_class_history("TestVehicle")
    assert len(history) == 1

    chain = in_memory_db.get_inheritance_chain("TestVehicle")
    assert len(chain) == 1
    assert chain[0].name == "TestVehicle"

