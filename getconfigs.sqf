// Output format:
// [{"class":"AllVehicles","source":"A3","category":"CfgVehicles","parent":""}]

private ["_classHierarchy", "_configs"];

// Collect every top-level config category from configFile
private _categories = [];

// Define essential base categories that must be included
_categories = ["CfgVehicles", "CfgWeapons", "CfgMagazines", "CfgAmmo", "CfgGroups"];

// // Add core A3 categories that contain base classes
// _categories append [
//     "CfgFactionClasses",
//     "CfgVehicleClasses", 
//     "CfgEditorSubcategories",
//     "CfgRoles",
//     "CfgMen",
//     "CfgBrains",
//     "CfgSoldierFamilies"
// ];

// // Debug: use important categories only
// _categories = ["CfgVehicles", "CfgWeapons", "CfgMagazines", "CfgAmmo", "CfgGroups", "CfgFactionClasses", "CfgPatches"];

// // Debug: use only one category
// _categories = ["CfgWeapons"];

diag_log text format ["[PCA] Starting config extraction..."];
_classHierarchy = createHashMap;
private _parentCache = createHashMap;

// Process each category
{
    private _category = _x;
    diag_log text format ["[PCA] Processing %1...", _category];
    
    // Pre-allocate arrays based on typical sizes
    private _classes = [];
    _classes resize 10000;
    private _classCount = 0;

    // Optimized class collection
    private _getAllClasses = {
        params ["_config", ["_depth", 0]];
        private _localClasses = [];
        _localClasses resize (count _config);
        private _localCount = 0;
        
        for "_i" from 0 to (count _config - 1) do {
            private _entry = _config select _i;
            if (isClass _entry) then {
                // Store class
                _localClasses set [_localCount, _entry];
                _localCount = _localCount + 1;
                
                // Process parents only if not already cached
                private _className = configName _entry;
                if (isNil {_parentCache getOrDefault [_className, nil]}) then {
                    private _parent = inheritsFrom _entry;
                    private _parentChain = [];
                    while {!isNull _parent} do {
                        _parentChain pushBack _parent;
                        _parent = inheritsFrom _parent;
                    };
                    _parentCache set [_className, _parentChain];
                    
                    // Add parents to local classes
                    {
                        _localClasses set [_localCount, _x];
                        _localCount = _localCount + 1;
                    } forEach _parentChain;
                };
                
                // Recurse into children
                _localClasses append ([_entry, _depth + 1] call _getAllClasses);
            };
        };
        
        _localClasses resize _localCount;
        _localClasses
    };

    private _configs = [(configFile >> _category)] call _getAllClasses;

    // Process classes in batches for better performance
    private _batchSize = 1000;
    private _batches = ceil(count _configs / _batchSize);
    
    for "_batch" from 0 to (_batches - 1) do {
        private _start = _batch * _batchSize;
        private _end = (_start + _batchSize) min (count _configs);
        
        for "_i" from _start to (_end - 1) do {
            private _entry = _configs select _i;
            private _className = configName _entry;
            
            if (_className != "") then {
                private _sourceList = configSourceModList _entry;
                private _source = if (count _sourceList > 0) then { _sourceList select 0 } else { "A3" };
                private _parentChain = _parentCache getOrDefault [_className, []];
                private _parent = if (count _parentChain > 0) then { _parentChain select 0 } else { configNull };
                private _parentName = if (!isNull _parent) then { configName _parent } else { "" };
                
                _classHierarchy set [_className, [_source, _parentName, _category]];
            };
        };
        
        if (_batch % 10 == 0) then {
            diag_log text format ["[PCA] Processed batch %1 of %2 for %3", _batch + 1, _batches, _category];
        };
    };
} forEach _categories;

// CSV generation with minimal overhead
private _safeStr = {
    params ["_str"];
    private _buffer = "";
    {
        switch (_x) do {
            case 44: { _buffer = _buffer + "\,"; };  // Escape commas
            case 34: { _buffer = _buffer + '""'; };  // Double quotes for CSV
            case 10: { _buffer = _buffer + " "; };   // Replace newlines with space
            case 13: { _buffer = _buffer + " "; };   // Replace carriage returns with space
            default {
                if (_x >= 32 && _x <= 126) then {
                    _buffer = _buffer + toString [_x];
                };
            };
        };
    } forEach toArray _str;
    _buffer
};

private _generateCsvLine = {
    params ["_className"];
    private _data = _classHierarchy get _className;
    if (isNil "_data") exitWith {
        format ['"%1","-","-","-"', [_className] call _safeStr]
    };

    private ["_source", "_parent", "_category"];
    _source = _data select 0;
    _parent = _data select 1;
    _category = _data select 2;

    // Ensure all fields are properly quoted and escaped
    format ['"%1","%2","%3","%4"',
        [_className] call _safeStr,
        [_source] call _safeStr,
        [_category] call _safeStr,
        [_parent] call _safeStr
    ]
};

// Process categories into separate chunks
{
    private _category = _x;
    private _categoryClasses = createHashMap;
    
    // Filter classes for this category
    {
        private _className = _x;
        private _data = _classHierarchy get _className;
        if (_data select 2 == _category) then {
            _categoryClasses set [_className, _data];
        };
    } forEach keys _classHierarchy;
    
    if (count _categoryClasses > 0) then {
        private _chunks = [];
        private _currentChunk = [];
        private _maxChunkSize = 1024 * 1024;
        private _processedClasses = 0;
        
        // Add CSV header to first chunk
        _currentChunk = ['"ClassName","Source","Category","Parent"'];
        
        {
            private _csvLine = [_x] call _generateCsvLine;
            private _currentSize = count (_currentChunk joinString toString [10]);
            
            if (_currentSize + count _csvLine + 1 > _maxChunkSize) then {
                _chunks pushBack (_currentChunk joinString toString [10]);
                _currentChunk = [_csvLine];
            } else {
                _currentChunk pushBack _csvLine;
            };
            
            _processedClasses = _processedClasses + 1;
        } forEach keys _categoryClasses;
        
        if (count _currentChunk > 0) then {
            _chunks pushBack (_currentChunk joinString toString [10]);
        };
        
        // Store chunks for this category
        {
            private _chunkNum = _forEachIndex + 1;
            private _chunkKey = format ["extractedCsv_%1_%2", _category, _chunkNum];
            profileNamespace setVariable [_chunkKey, _x];
            
            if (_forEachIndex == 0) then {
                profileNamespace setVariable [format ["extractedCsv_%1_count", _category], count _chunks];
                profileNamespace setVariable [format ["extractedCsv_%1_totalClasses", _category], count _categoryClasses];
            };
            
            saveProfileNamespace;
            diag_log text format ["[PCA] Saved %1 chunk %2 of %3", _category, _chunkNum, count _chunks];
        } forEach _chunks;
    };
} forEach _categories;

diag_log text format ["[PCA] Completed config extraction for %1 categories", count _categories];