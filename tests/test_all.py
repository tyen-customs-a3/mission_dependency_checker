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
    classes = parser.parse_file(sample_class_file)
    
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
    """Test parsing of loadout file with LIST macros and equipment"""
    parser = ClassParser()
    classes = parser.parse_file(sample_loadout_file)
    
    # Should find base class and rm class
    assert len(classes) >= 2, "Expected at least baseMan and rm classes"
    
    # Check baseMan class
    base_man = next((c for c in classes if c.name == "baseMan"), None)
    assert base_man is not None
    assert base_man.parent is None
    assert "displayName" in base_man.properties
    assert base_man.properties["displayName"] == '"Unarmed"'
    
    # Check rm (rifleman) class
    rm = next((c for c in classes if c.name == "rm"), None)
    assert rm is not None
    assert rm.parent == "baseMan"
    
    # Verify equipment references are found
    equipment_refs = {c.name for c in classes if c.is_reference}
    expected_items = {
        "rhs_weap_rpg7",
        "ACE_fieldDressing",
        "ACE_packingBandage",
        "ACE_epinephrine",
        "ACE_morphine",
        "ACE_bloodIV",
        "ACE_splint",
        "ACE_surgicalKit",
        "rhs_rpg7_PG7VL_mag",
        "CUP_30Rnd_45ACP_Green_Tracer_MAC10_M",
        "CUP_hgun_Mac10",
        "pca_vest_invisible_plate",
        "pca_backpack_invisible_large"
    }
    
    assert expected_items.issubset(equipment_refs), \
        f"Missing equipment references. Expected {expected_items - equipment_refs}"
    
    # Verify LIST macro expansions
    list_refs = {c for c in classes if c.is_reference and 'list_count' in c.properties}
    
    # Check a few specific LIST items
    field_dressing = next((c for c in list_refs if c.name == "ACE_fieldDressing"), None)
    assert field_dressing is not None
    assert field_dressing.properties["list_count"] == "20"
    
    rpg_mag = next((c for c in list_refs if c.name == "rhs_rpg7_PG7VL_mag"), None)
    assert rpg_mag is not None
    assert rpg_mag.properties["list_count"] == "10"

# === INIDBI Parser Tests ===

# Const data for INIDBI parsing tests
INI_TEST_CONTENT = """
[CategoryData_CfgVehicles]
header=""ClassName,Source,Category,Parent,InheritsFrom,IsSimpleObject,NumProperties,Scope,Model""
0=""All,@cup_terrain_core,CfgVehicles,CfgVehicles,,false,313,0,\A3\Weapons_F\empty.p3d""
1=""Logic,curator,CfgVehicles,CfgVehicles,All,false,15,2,\A3\Weapons_f\empty""
2=""AllVehicles,curator,CfgVehicles,CfgVehicles,All,false,65,0,\A3\Weapons_F\empty.p3d""
3=""Land,A3,CfgVehicles,CfgVehicles,AllVehicles,false,20,0,\A3\Weapons_F\empty.p3d""
4=""LandVehicle,A3,CfgVehicles,CfgVehicles,Land,false,25,0,\A3\Weapons_F\empty.p3d""
5=""Car,@em,CfgVehicles,CfgVehicles,LandVehicle,false,104,0,\A3\Weapons_F\empty.p3d""
6=""Motorcycle,@cup_terrain_core,CfgVehicles,CfgVehicles,LandVehicle,false,73,0,\A3\Weapons_F\empty.p3d""
7=""Bicycle,A3,CfgVehicles,CfgVehicles,Motorcycle,false,11,0,\A3\Weapons_F\empty.p3d""
8=""Tank,@em,CfgVehicles,CfgVehicles,LandVehicle,false,96,0,\A3\Weapons_F\empty.p3d""
9=""APC,A3,CfgVehicles,CfgVehicles,Tank,false,20,0,\A3\Weapons_F\empty.p3d""
10=""Man,curator,CfgVehicles,CfgVehicles,Land,false,227,0,""
11=""Animal,A3,CfgVehicles,CfgVehicles,Man,false,22,0,""
12=""Air,@em,CfgVehicles,CfgVehicles,AllVehicles,false,88,0,\A3\Weapons_F\empty.p3d""
13=""Helicopter,@ace,CfgVehicles,CfgVehicles,Air,false,116,0,\A3\Weapons_F\empty.p3d""
14=""Plane,@ace,CfgVehicles,CfgVehicles,Air,false,130,0,\A3\Weapons_F\empty.p3d""
15=""Ship,A3,CfgVehicles,CfgVehicles,AllVehicles,false,69,0,\A3\Weapons_F\empty.p3d""
16=""SmallShip,A3,CfgVehicles,CfgVehicles,Ship,false,20,0,\A3\Weapons_F\empty.p3d""
17=""BigShip,A3,CfgVehicles,CfgVehicles,Ship,false,15,0,\A3\Weapons_F\empty.p3d""
18=""Truck,A3,CfgVehicles,CfgVehicles,Car,false,18,0,\A3\Weapons_F\empty.p3d""
19=""ParachuteBase,curator,CfgVehicles,CfgVehicles,Helicopter,false,71,0,\A3\air_f_beta\Parachute_01\Parachute_01_F.p3d""
20=""LaserTarget,@cup_terrain_core,CfgVehicles,CfgVehicles,All,false,29,0,\A3\Weapons_f\laserTgt.p3d""
21=""NVTarget,@cup_terrain_core,CfgVehicles,CfgVehicles,All,false,24,0,laserTgt.p3d""
22=""ArtilleryTarget,@cba_a3,CfgVehicles,CfgVehicles,All,false,25,1,""
23=""ArtilleryTargetW,A3,CfgVehicles,CfgVehicles,ArtilleryTarget,false,2,1,""
24=""ArtilleryTargetE,A3,CfgVehicles,CfgVehicles,ArtilleryTarget,false,2,1,""
25=""SuppressTarget,A3,CfgVehicles,CfgVehicles,LaserTarget,false,19,1,""
26=""PaperCar,@cup_terrain_core,CfgVehicles,CfgVehicles,Car,false,8,0,\ca\data\papAuto.p3d""
27=""FireSectorTarget,@cba_a3,CfgVehicles,CfgVehicles,All,false,37,1,\core\default\default.p3d""
28=""Static,@cba_a3,CfgVehicles,CfgVehicles,All,false,30,0,\A3\Weapons_F\empty.p3d""
29=""Rope,@em_rework,CfgVehicles,CfgVehicles,All,false,23,1,\A3\Data_f\proxies\Rope\rope.p3d""
30=""Fortress,A3,CfgVehicles,CfgVehicles,Static,false,10,0,\A3\Weapons_F\empty.p3d""
31=""Building,A3,CfgVehicles,CfgVehicles,Static,false,11,1,\A3\Weapons_F\empty.p3d""
32=""NonStrategic,A3,CfgVehicles,CfgVehicles,Building,false,8,1,\A3\Weapons_F\empty.p3d""
33=""HeliH,@cup_terrain_core,CfgVehicles,CfgVehicles,NonStrategic,false,19,2,\ca\misc\heli_h_army.p3d""
34=""AirportBase,A3,CfgVehicles,CfgVehicles,NonStrategic,false,5,1,\A3\Weapons_F\empty.p3d""
35=""Strategic,A3,CfgVehicles,CfgVehicles,Building,false,9,1,\A3\Weapons_F\empty.p3d""
36=""FlagCarrierCore,A3,CfgVehicles,CfgVehicles,Strategic,false,14,1,""
37=""Land_VASICore,A3,CfgVehicles,CfgVehicles,NonStrategic,false,24,1,""
38=""Thing,A3,CfgVehicles,CfgVehicles,All,false,36,0,\A3\Weapons_F\empty.p3d""
39=""ThingEffect,A3,CfgVehicles,CfgVehicles,Thing,false,10,1,\A3\Weapons_F\empty.p3d""
40=""ThingEffectLight,A3,CfgVehicles,CfgVehicles,ThingEffect,false,9,0,\A3\Weapons_F\empty.p3d""
41=""ThingEffectFeather,A3,CfgVehicles,CfgVehicles,ThingEffectLight,false,7,0,\A3\Weapons_F\empty.p3d""
42=""FxExploArmor1,A3,CfgVehicles,CfgVehicles,ThingEffect,false,6,1,\A3\Weapons_f\metal_plate""
43=""FxExploArmor2,A3,CfgVehicles,CfgVehicles,ThingEffect,false,6,1,\A3\Weapons_f\metal_plate_2""
44=""FxExploArmor3,A3,CfgVehicles,CfgVehicles,ThingEffect,false,6,1,\A3\Weapons_f\debris""
45=""FxExploArmor4,A3,CfgVehicles,CfgVehicles,ThingEffect,false,6,1,\A3\Weapons_f\fragment""
46=""FxCartridge,A3,CfgVehicles,CfgVehicles,ThingEffect,false,11,1,\A3\Weapons_f\ammo\cartridge""
47=""WindAnomaly,A3,CfgVehicles,CfgVehicles,All,false,9,0,\A3\Weapons_F\empty.p3d""
48=""HouseBase,A3,CfgVehicles,CfgVehicles,NonStrategic,false,11,1,""
49=""House,A3,CfgVehicles,CfgVehicles,HouseBase,false,7,1,""
[CategoryData_CfgWeapons]
header=""ClassName,Source,Category,Parent,InheritsFrom,IsSimpleObject,NumProperties,Scope,Model""
0=""Default,A3,CfgWeapons,CfgWeapons,,false,133,0,""
1=""PistolCore,A3,CfgWeapons,CfgWeapons,Default,false,4,0,""
2=""RifleCore,A3,CfgWeapons,CfgWeapons,Default,false,6,0,""
3=""MGunCore,A3,CfgWeapons,CfgWeapons,Default,false,5,0,""
4=""LauncherCore,A3,CfgWeapons,CfgWeapons,Default,false,6,0,""
5=""GrenadeCore,A3,CfgWeapons,CfgWeapons,Default,false,6,0,""
6=""CannonCore,A3,CfgWeapons,CfgWeapons,Default,false,2,0,""
7=""FakeWeapon,A3,CfgWeapons,CfgWeapons,MGunCore,false,8,1,""
8=""DetectorCore,A3,CfgWeapons,CfgWeapons,Default,false,7,0,""
9=""ItemCore,A3,CfgWeapons,CfgWeapons,Default,false,5,0,\A3\weapons_F\ammo\mag_univ.p3d""
10=""HeadgearItem,@cup_units,CfgWeapons,CfgWeapons,InventoryItem_Base_F,false,6,0,""
11=""VestItem,@cup_units,CfgWeapons,CfgWeapons,InventoryItem_Base_F,false,13,0,""
12=""NVGoggles,@ace,CfgWeapons,CfgWeapons,Binocular,false,22,2,\A3\Weapons_f\binocular\nvg_proxy""
"""

def test_parse_inidbi_format(temp_dir):
    """Test INIDBI2 format parsing"""
    test_file = temp_dir / "config.ini"
    test_file.write_text(INI_TEST_CONTENT)

    parser = InidbiParser()
    classes_by_source = parser.parse_file(test_file)

    # Check sources are present
    assert "@cup_terrain_core" in classes_by_source
    assert "curator" in classes_by_source
    assert "A3" in classes_by_source

def test_class_lookup(temp_dir):
    """Test exact class name lookup"""

    test_file = temp_dir / "config.ini"
    test_file.write_text(INI_TEST_CONTENT)

    parser = InidbiParser()
    classes_by_source = parser.parse_file(test_file)

    # Test exact class lookup
    all_class = parser.get_class("All")
    assert all_class is not None
    assert all_class.source == "@cup_terrain_core"
    
    # Test pattern matching
    logic_classes = parser.find_classes("Logic.*")
    assert len(logic_classes) == 1
    assert next(iter(logic_classes)).name == "Logic"

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

