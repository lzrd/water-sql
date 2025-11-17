# CLAUDE.md

> **Note:** This file provides guidance to AI coding assistants (like Claude Code) when working with this repository.
> **For human contributors:** See [for-developers/CONTRIBUTING.md](for-developers/CONTRIBUTING.md) and [README.md](README.md)

## Project Overview

This project builds student-friendly educational packages containing EPA STORET water quality data. The system supports multiple states:
- **Washington State** (included): 3.1+ million measurements from 6,892 stations
- **Any other state**: Oregon, California, Illinois, etc. can be added using the same tools

Each package includes:
- A SQLite database (200-500 MB typical, portable, no server needed)
- Python analysis scripts with visualizations
- Comprehensive documentation (Markdown + HTML)

The build system transforms raw EPA STORET data files into complete, distribution-ready zip packages.

## Build Commands

### Main Build Process
```bash
# Build the complete student package
./build.sh [state] [version]
# Examples:
./build.sh washington 1.2.1    # Default: washington 1.2.1
./build.sh oregon 2.0

# Output: dist/washington_water_data_v1.2.1.zip (~79 MB)
```

The build script performs 9 steps:
1. Cleans `build/package/` directory
2. Copies `build/washington_water.db` to package (or decompresses from .xz if needed)
3. Skips SQL.js (removed in v1.3 - browser console too slow)
4. Copies student documentation from `for-students/`
5. Converts Markdown documentation to HTML
6. Copies Python scripts from `src/Python_Scripts/`
7. Generates sample visualizations
8. Creates MANIFEST.txt
9. Creates zip archive in `dist/`

### Development Workflow

```bash
# Parse raw EPA STORET data to CSV (any state)
# Washington (original parser - still works):
python3 src/parse_washington_data.py data/Washington -o build/output

# Any state (new generalized parser):
python3 src/parse_state_data.py data/Oregon -s OR -n Oregon -o build/output_oregon
python3 src/parse_state_data.py data/California -s CA -n California -o build/output_california

# Import CSV to SQLite (auto-generated script)
cd build/output_oregon
./import_to_sqlite.sh
cd ../..

# Export from PostgreSQL to SQLite (if database server is available - Washington only)
python3 src/export_to_sqlite.py

# Test the analysis scripts
cd build/package/Python_Scripts
pip install -r requirements.txt
python3 analyze_water_quality_sqlite.py

# Test database directly
sqlite3 build/washington_water.db "SELECT COUNT(*) FROM results;"  # Washington: 3,178,425
sqlite3 build/oregon_water.db "SELECT COUNT(*) FROM results;"      # Oregon: varies
```

### Testing a Package

```bash
# Extract and test in temporary location
mkdir -p /tmp/test && cd /tmp/test
unzip ~/path/to/dist/washington_water_data_v1.2.1.zip
cd package
open QUICKSTART.html  # Or xdg-open on Linux (Windows: start QUICKSTART.html)
cd Python_Scripts && python3 analyze_water_quality_sqlite.py
```

## Directory Structure

```
water-sql/
├── README.md                      # Main entry point - directs to audience-specific docs
│
├── for-students/                  # Student documentation (copied to packages)
│   ├── README.md                  # Student starting point
│   ├── QUICKSTART.md              # 15-minute quick start guide
│   ├── INSTALL.md                 # Platform-specific setup guide
│   ├── INTERVIEW_PREP.md          # Interview practice questions
│   ├── SPATIAL_ANALYSIS.md        # Geographic analysis and mapping
│   ├── WATER_DATA.md              # SQL tutorial and database guide
│   ├── TIME_CODES.md              # Time code reference
│   ├── BROWSER_CONSOLE.md         # Browser console (legacy)
│   └── example_queries.sql        # Sample queries
│
├── for-teachers/                  # Teacher documentation
│   ├── README.md                  # Teacher starting point
│   ├── QUICKSTART.md              # One-page: create distribution
│   ├── DETAILED_GUIDE.md          # Complete guide with troubleshooting
│   ├── CURRICULUM_ALIGNMENT.md    # OSPI/NGSS/Common Core standards
│   ├── ADDING_STATES.md           # Technical: add new states
│   └── QUICK_REFERENCE.md         # Command reference cheat sheet
│
├── for-developers/                # Developer documentation
│   ├── README.md                  # Developer starting point
│   ├── CONTRIBUTING.md            # How to contribute
│   ├── ARCHITECTURE.md            # Technical design and schema
│   ├── AUTOMATION.md              # Build system and GitHub Actions
│   └── DATA_SOURCES.md            # EPA STORET format
│
├── src/                           # SOURCE FILES (edit these)
│   ├── templates/                 # Build-specific templates (index.html, sample.sqliterc)
│   ├── Python_Scripts/            # Analysis scripts for students
│   │   ├── analyze_water_quality_sqlite.py       # Main analysis script
│   │   ├── analyze_water_quality_annotated.py    # Educational version (600+ comment lines)
│   │   ├── analyze_water_quality_dual.py         # PostgreSQL/SQLite comparison
│   │   └── requirements.txt
│   ├── parse_state_data.py        # Universal state parser (any state)
│   ├── parse_washington_data.py   # LEGACY: Washington-specific parser
│   ├── export_to_sqlite.py        # Converts PostgreSQL → SQLite (Washington only)
│   └── convert_md_to_html.py      # Converts Markdown → HTML
│
├── scripts/                       # Automation scripts
│   ├── download_state_data.sh     # Download EPA STORET data
│   ├── build_state_package.sh     # Complete build pipeline
│   ├── compress_database.sh       # Compress SQLite with xz
│   └── decompress_database.sh     # Decompress for builds
│
├── data/storet/                   # Downloaded EPA data (not in git)
│   └── {State}.zip                # Raw STORET downloads
│
├── build/                         # Build artifacts
│   ├── output*/                   # Parser-generated CSV files (not in git)
│   ├── {state}_water.db           # SQLite database (not in git, too large)
│   ├── {state}_water.db.xz        # Compressed database (COMMIT TO GIT)
│   └── package/                   # Temporary staging during build (not in git)
│
├── dist/                          # Distribution packages (not in git)
│   └── *.zip                      # Final student packages
│
├── .github/workflows/             # GitHub Actions
│   └── release.yml                # Automatic release creation
│
└── build.sh                       # Main build automation script
```

## Database Schema

The SQLite database has three normalized tables:

```sql
-- Parameter definitions (1,587 parameters)
CREATE TABLE parameters (
    code TEXT PRIMARY KEY,          -- e.g., "00010", "00300"
    short_name TEXT,                -- e.g., "TEMP", "DO"
    long_name TEXT                  -- e.g., "Temperature, water"
);

-- Monitoring stations (6,892 stations)
CREATE TABLE stations (
    agency TEXT,
    station_id TEXT PRIMARY KEY,
    station_name TEXT,
    agency_name TEXT,
    state TEXT,
    county TEXT,
    latitude REAL,
    longitude REAL,
    huc TEXT,                       -- Hydrologic Unit Code
    station_type TEXT,
    description TEXT
);

-- Measurement results (3,178,425 measurements)
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agency TEXT,
    station_id TEXT,
    param_code TEXT,
    start_date TEXT,                -- ISO format: YYYY-MM-DD
    start_time TEXT,                -- Special codes: "2500"=noon, "0001"=unknown
    result_value TEXT,              -- Kept as TEXT (various formats/units)
    huc TEXT,
    sample_depth TEXT,
    FOREIGN KEY (station_id) REFERENCES stations(station_id),
    FOREIGN KEY (param_code) REFERENCES parameters(code)
);
```

**Indexes:**
- `idx_results_station` ON results(station_id)
- `idx_results_param` ON results(param_code)
- `idx_results_date` ON results(start_date)
- `idx_stations_county` ON stations(county)

## Architecture Notes

### Data Processing Pipeline

```
EPA STORET Data (online)
    ↓ download_state_data.sh
Raw ZIP file (~500 MB)
    ↓ parse_state_data.py
CSV files (normalized)
    ↓ import_to_sqlite.sh (auto-generated)
SQLite Database (200-400 MB)
    ↓ compress_database.sh
Compressed DB (~80 MB, .xz) ← COMMIT TO GIT
    ↓ build.sh or GitHub Actions
Student Package (~80 MB, .zip) ← DISTRIBUTE
```

**Key scripts:**
1. **Raw Data → CSV**: `parse_state_data.py` reads tab-delimited EPA STORET files and generates normalized CSV files
2. **CSV → SQLite**: Auto-generated `import_to_sqlite.sh` script imports CSVs
3. **SQLite → Compressed**: `compress_database.sh` compresses with xz (371 MB → 80 MB)
4. **Compressed → Package**: `build.sh` decompresses and bundles with scripts and documentation

### Why SQLite Instead of PostgreSQL?

The project originally used PostgreSQL but switched to SQLite for student distribution because:
- No server setup required (works immediately on Windows/macOS/Linux)
- Single 371 MB file is portable
- Performance is adequate for 3.1M rows with proper indexing
- Students can query with `sqlite3` CLI or Python

### Browser Console Decision (v1.3+)

**Removed** from recommended package. The `water_quality_browser.html` file attempted to load the entire database in-browser using SQL.js but:
- Loading time >2 minutes (declared "failing" by users)
- Browser must load entire 371 MB database into memory
- No progressive loading possible due to browser security

**Alternative**: Python scripts load database in 1-2 seconds, query instantly

### Markdown to HTML Conversion

`convert_md_to_html.py` generates simple HTML versions of documentation with:
- GitHub-flavored markdown rendering
- Basic CSS styling
- Syntax highlighting for code blocks
- Relative link conversion

This allows students to read documentation in a web browser without markdown viewers.

## Important Conventions

### File Encoding
- Raw EPA STORET files use `latin-1` encoding
- Parser handles this with `encoding='latin-1'` in file operations

### Time Codes
- `start_time` column uses special codes, not HH:MM format
- See `for-students/TIME_CODES.md` for complete reference
- Common codes: `2500` (noon), `0001` (unknown time)

### Result Values
- Stored as TEXT (not numeric) because of varying units and formats
- Analysis scripts convert to numeric as needed with error handling
- Some values include qualifiers like "<0.5" or "ND" (not detected)

### Package Version Numbers
- v1.2.1: Current stable version with PostgreSQL/SQLite dual support
- v1.3: Planned version without browser console
- Edit default version in `build.sh` line 8: `VERSION="${2:-1.2.1}"`

## Common Development Tasks

### Adding or Modifying Student Documentation
1. Edit files in `for-students/` directory
2. Run `./build.sh` to copy to package and regenerate HTML versions
3. Test by extracting archive and opening HTML files

### Adding or Modifying Teacher Documentation
1. Edit files in `for-teachers/` directory
2. Documentation is separate from student packages
3. Commit changes directly

### Modifying Analysis Scripts
1. Edit scripts in `src/Python_Scripts/`
2. Test locally: `python3 src/Python_Scripts/analyze_water_quality_sqlite.py`
3. Run `./build.sh` to include in distribution package

### Adding a New State

**Quick version** (see `for-teachers/ADDING_STATES.md` for complete guide):

**One command does everything:**
```bash
./scripts/build_state_package.sh Oregon OR 1.0
```

This automatically:
1. Downloads EPA STORET data
2. Parses to CSV
3. Imports to SQLite
4. Compresses database (371 MB → 80 MB)
5. Creates student package

**Then commit compressed database:**
```bash
git add build/oregon_water.db.xz
git commit -m "Add Oregon water quality database"
```

See `for-developers/AUTOMATION.md` for details on the build system.

**Supported states**: Any state with EPA STORET format data (Washington, Oregon, California, Illinois, etc.)

**New tools**:
- `src/parse_state_data.py` - Universal parser that works with any state
- Auto-generated `import_to_sqlite.sh` - Handles CSV → SQLite import automatically

**Documentation**:
- Full guide: `for-teachers/ADDING_STATES.md`
- Quick reference: `for-teachers/QUICK_REFERENCE.md`

### Troubleshooting Build Failures

**"Database not found: build/washington_water.db"**
- Database must exist before building or compressed version must exist
- If `.db.xz` exists, build.sh will auto-decompress
- Otherwise run: `./scripts/build_state_package.sh StateName ST 1.0`

**"Student documentation not found in for-students/"**
- Verify repository structure with `ls -la for-students/`
- Check that files were copied correctly during reorganization

**Sample output generation fails**
- Non-critical warning (build continues)
- Requires matplotlib/pandas to be installed
- Missing dependencies or database connection issues

## Requirements

### Build System
- bash
- Python 3.7+
- zip, unzip
- sqlite3 command-line tool

### Python Analysis Scripts
```
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
psycopg2-binary>=2.9.0    # Only for PostgreSQL export
sqlalchemy>=1.4.0
```

### Data Parsing
- Python 3.7+ with standard library (csv, pathlib, collections)

## Key Design Decisions

1. **SQLite over PostgreSQL for distribution**: Eliminates server setup burden for students
2. **Both MD and HTML documentation**: Accommodates different preferences/environments
3. **Three analysis scripts**: Basic, annotated (educational), and dual (comparison) versions
4. **Normalized schema**: Three tables with foreign keys for data integrity
5. **Text-based result_value**: Preserves qualifiers and varying formats from source data
6. **Batch processing in export**: 10,000 rows at a time to manage memory during PostgreSQL→SQLite conversion
