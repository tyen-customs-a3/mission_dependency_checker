// File Format Description:
// -----------------------
// Database: ConfigExtract_YYYY-MM-DD_HH-MM-SS.ini
//
// Sections:
// 1. Validation
//    - Keys: TotalClasses, Categories, Stats_CategoryName
// 2. CategoryData_[CategoryName]
//    - Keys: CSV lines with format ClassName,Source,Category,Parent
//
// Note: Ensure INIDBI2 is configured and available before running this script.

// Debug flag to control category scope
private _debugMode = false;  // Set to true for limited testing categories

private ["_classHierarchy", "_configs"];

// Define categories based on debug mode
private _categories = if (_debugMode) then {
    // Limited set for testing/debugging
    ["CfgWeapons", "CfgVehicles"]
} else {
    // Scan for all available categories in configFile
    private _allCategories = [];
    for "_i" from 0 to (count configFile - 1) do {
        private _entry = configFile select _i;
        if (isClass _entry) then {
            _allCategories pushBack (configName _entry);
        };
    };
    _allCategories
};

diag_log text format ["Running in %1 mode with %2 categories", ["FULL", "DEBUG"] select _debugMode, count _categories];

diag_log text format ["Starting config extraction..."];

// Initialize database early
private _timestamp = systemTime apply { if (_x < 10) then { "0" + str _x } else { str _x } };
private _dbName = format ["ConfigExtract_%1-%2-%3_%4-%5-%6", 
    _timestamp#0, _timestamp#1, _timestamp#2,
    _timestamp#3, _timestamp#4, _timestamp#5
];
private _db = ["new", _dbName] call OO_INIDBI;

// Track statistics during processing
private _totalClasses = 0;
private _categoryStats = createHashMap;

// Simplified CSV line writer
private _writeCsvLine = {
    params ["_section", "_className", "_source", "_category", "_parent"];
    private _csvLine = format ["%1,%2,%3,%4", _className, _source, _category, _parent];
    ["write", [_section, _className, _csvLine]] call _db;
};

// Process each category
{
    private _category = _x;
    private _sectionName = format ["CategoryData_%1", _category];
    private _categoryCount = 0;
    
    // Write header
    ["write", [_sectionName, "header", "ClassName,Source,Category,Parent"]] call _db;
    
    // Combined class collection and processing
    private _processConfig = {
        params ["_config"];
        
        for "_i" from 0 to (count _config - 1) do {
            private _entry = _config select _i;
            if (isClass _entry) then {
                private _className = configName _entry;
                if (_className != "") then {
                    // Process class data
                    private _sourceList = configSourceModList _entry;
                    private _source = if (count _sourceList > 0) then { _sourceList select 0 } else { "A3" };
                    private _parent = inheritsFrom _entry;
                    private _parentName = if (!isNull _parent) then { configName _parent } else { "" };
                    
                    // Write immediately
                    [_sectionName, _className, _source, _category, _parentName] call _writeCsvLine;
                    
                    // Update statistics
                    _totalClasses = _totalClasses + 1;
                    _categoryCount = _categoryCount + 1;
                    
                    // Process child classes
                    [_entry] call _processConfig;
                };
            };
        };
    };
    
    diag_log text format ["Processing %1...", _category];
    [(configFile >> _category)] call _processConfig;
    
    // Store category statistics
    _categoryStats set [_category, _categoryCount];
    
    diag_log text format ["Processed %1 classes for %2", _categoryCount, _category];
} forEach _categories;

// Write validation info at the end
["write", ["Validation", "TotalClasses", _totalClasses]] call _db;
["write", ["Validation", "Categories", _categories]] call _db;

{
    private _statsKey = format ["Stats_%1", _x];
    ["write", ["Validation", _statsKey, _categoryStats get _x]] call _db;
} forEach _categories;

// Clean up
["delete", _db] call OO_INIDBI;

diag_log text format ["Completed config extraction to %1", _dbName];