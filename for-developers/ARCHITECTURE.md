# Water Quality Data Project - Developer Documentation

## Quick Start

### You Just Reorganized - What's Next?

```bash
# 1. Verify the new structure
tree -L 2

# 2. Build a clean package (version 1.3 without browser console)
./build.sh washington 1.3

# 3. Test the package
cd /tmp
tar -xzf ~/Sysadmin/compose/db/dist/washington_water_data_v1.3.tar.gz
cd package/Python_Scripts
pip install -r requirements.txt
python3 analyze_water_quality_sqlite.py
```

## Project Structure

```
/home/stoltz/Sysadmin/compose/db/
├── src/                          # SOURCE (edit these)
│   ├── templates/                # Package templates
│   │   ├── README.md
│   │   ├── INSTALL.md
│   │   ├── water_quality_browser.html
│   │   └── Documentation/
│   │       ├── WATER_DATA.md
│   │       └── TIME_CODES.md
│   ├── Python_Scripts/           # Analysis scripts
│   │   ├── requirements.txt
│   │   ├── analyze_water_quality_sqlite.py
│   │   ├── analyze_water_quality_annotated.py
│   │   └── analyze_water_quality_dual.py
│   ├── parse_washington_data.py  # Data parser
│   ├── export_to_sqlite.py       # PostgreSQL → SQLite
│   └── convert_md_to_html.py     # MD → HTML converter
│
├── data/                         # RAW DATA
│   └── Washington/               # EPA STORET files
│
├── build/                        # BUILD ARTIFACTS
│   ├── output/                   # CSV files from parser
│   ├── washington_water.db       # SQLite database (371 MB)
│   └── package/                  # Staging area (temporary)
│
├── dist/                         # DISTRIBUTION
│   └── *.tar.gz                  # Student packages
│
├── docs/                         # DOCUMENTATION
│   ├── README.md (this file)
│   └── *.txt (historical notes)
│
├── build.sh                      # Build automation
└── reorganize.sh                 # Cleanup (already ran)
```

## Building Student Packages

### Basic Build

```bash
# Build version 1.3 for Washington State
./build.sh washington 1.3

# Output: dist/washington_water_data_v1.3.tar.gz (~79 MB)
```

### What build.sh Does

1. Cleans previous build artifacts
2. Copies SQLite database from `build/`
3. Downloads SQL.js library (for browser console if needed)
4. Copies template files from `src/templates/`
5. Converts Markdown to HTML
6. Copies Python scripts
7. Generates sample visualizations
8. Creates MANIFEST.txt
9. Creates tar.gz archive in `dist/`

## Adding a New State (e.g., Oregon)

### Step 1: Obtain Raw Data

Download EPA STORET data and organize:
```
data/Oregon/
├── OR_County1_inv.txt
├── OR_County1/
│   ├── OR_County1_sta_*.txt
│   └── OR_County1_res_*.txt
├── OR_County2_inv.txt
└── ... (repeat for each county)
```

### Step 2: Parse Raw Data to CSV

```bash
python3 src/parse_washington_data.py data/Oregon -o build/output_oregon

# Creates:
# build/output_oregon/parameters.csv
# build/output_oregon/stations.csv
# build/output_oregon/results.csv
# build/output_oregon/schema.sql
```

### Step 3: Create SQLite Database

```bash
cd build/output_oregon

# Create database and import schema
sqlite3 ../oregon_water.db < schema.sql

# Import CSV data
sqlite3 ../oregon_water.db <<'EOF'
.mode csv
.import --skip 1 parameters.csv parameters
.import --skip 1 stations.csv stations
.import --skip 1 results.csv results
EOF

# Create indexes
sqlite3 ../oregon_water.db <<'EOF'
CREATE INDEX idx_results_station ON results(station_id);
CREATE INDEX idx_results_param ON results(param_code);
CREATE INDEX idx_results_date ON results(start_date);
CREATE INDEX idx_stations_county ON stations(county);
EOF

cd ../..
```

### Step 4: Build Package

```bash
# Build version 1.0 for Oregon
./build.sh oregon 1.0

# Output: dist/oregon_water_data_v1.0.tar.gz
```

## Browser Console Decision

**Status**: ❌ Removed from recommended package (v1.3+)

**Why**: Loading time >2 minutes (user tested and declared "failing")

**Technical Reason**:
- Browser must load entire 371 MB database into memory
- No streaming/progressive loading possible
- Browser security prevents direct file access

**Alternative**: Python + SQLite
- 5-minute one-time setup
- Instant queries after setup
- Better educational value

## Editing Documentation

### Update Student Documentation

```bash
# 1. Edit markdown files
vim src/templates/README.md
vim src/templates/Documentation/WATER_DATA.md

# 2. Rebuild package (auto-converts MD to HTML)
./build.sh washington 1.3
```

### Files to Edit

- `src/templates/README.md` - Package README
- `src/templates/INSTALL.md` - Installation guide
- `src/templates/Documentation/WATER_DATA.md` - SQL tutorial
- `src/templates/Documentation/TIME_CODES.md` - Time codes

## Editing Python Scripts

```bash
# Edit scripts in src/
vim src/Python_Scripts/analyze_water_quality_sqlite.py

# Rebuild to include changes
./build.sh washington 1.3
```

## Parser Usage

The parser (`src/parse_washington_data.py`) processes EPA STORET tab-delimited files:

```bash
# Basic usage
python3 src/parse_washington_data.py data/Washington -o build/output

# Help
python3 src/parse_washington_data.py --help
```

**Input**: Tab-delimited text files
- `*_inv.txt` - Parameter definitions
- `*_sta_*.txt` - Station metadata
- `*_res_*.txt` - Measurement results

**Output**: PostgreSQL-compatible CSV files
- `parameters.csv`
- `stations.csv`
- `results.csv`
- `schema.sql`
- `import_data.sh`

## PostgreSQL to SQLite Export

If you have data in PostgreSQL and want to export to SQLite:

```bash
python3 src/export_to_sqlite.py \
    --host moneta.lan \
    --dbname washington_water \
    --user water \
    --output build/washington_water.db
```

## Common Tasks

### Rebuild Package After Changes

```bash
# Make changes to source files
vim src/templates/README.md

# Rebuild
./build.sh washington 1.3
```

### Test Package

```bash
# Extract to temp location
mkdir -p /tmp/test
tar -xzf dist/washington_water_data_v1.3.tar.gz -C /tmp/test

# Test documentation
cd /tmp/test/package
open README.html  # or xdg-open

# Test Python scripts
cd Python_Scripts
pip install -r requirements.txt
python3 analyze_water_quality_sqlite.py

# Test database
cd ..
sqlite3 washington_water.db "SELECT COUNT(*) FROM results;"
```

### Update Version Number

```bash
# Edit build.sh and change default version
vim build.sh  # Change VERSION="${2:-1.4}"

# Or specify on command line
./build.sh washington 1.4
```

## Package Contents (v1.3)

**Root**:
- `washington_water.db` (371 MB SQLite)
- `README.md` / `README.html`
- `INSTALL.md` / `INSTALL.html`
- `MANIFEST.txt`

**Documentation/**:
- `WATER_DATA.md` / `WATER_DATA.html` (SQL tutorial)
- `TIME_CODES.md` / `TIME_CODES.html`

**Python_Scripts/**:
- `requirements.txt`
- `analyze_water_quality_sqlite.py`
- `analyze_water_quality_annotated.py`
- `analyze_water_quality_dual.py`

**Sample_Output/**:
- `*.png` (example visualizations)

**NOT Included** (removed in v1.3):
- ❌ `water_quality_browser.html` (too slow)
- ❌ `lib/` directory (SQL.js not needed)
- ❌ `BROWSER_CONSOLE.md`

## Database Schema

Three tables with foreign key relationships:

```sql
-- Parameter definitions
CREATE TABLE parameters (
    code VARCHAR(10) PRIMARY KEY,
    short_name VARCHAR(100),
    long_name TEXT
);

-- Monitoring stations
CREATE TABLE stations (
    agency VARCHAR(50),
    station_id VARCHAR(50) PRIMARY KEY,
    station_name TEXT,
    county VARCHAR(50),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    huc VARCHAR(20)
);

-- Measurement results
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agency VARCHAR(50),
    station_id VARCHAR(50) REFERENCES stations(station_id),
    param_code VARCHAR(10) REFERENCES parameters(code),
    start_date DATE,
    start_time VARCHAR(10),  -- Special codes: 2500, 0001, etc.
    result_value VARCHAR(50),
    huc VARCHAR(20),
    sample_depth VARCHAR(20)
);
```

**Indexes**:
- `idx_results_station` ON results(station_id)
- `idx_results_param` ON results(param_code)
- `idx_results_date` ON results(start_date)
- `idx_stations_county` ON stations(county)

## Troubleshooting

### build.sh fails: "Database not found"

```bash
# Check if database exists
ls -lh build/washington_water.db

# If missing, export from PostgreSQL
python3 src/export_to_sqlite.py \
    --host moneta.lan \
    --dbname washington_water \
    --user water \
    --output build/washington_water.db
```

### build.sh fails: "Templates not found"

```bash
# Verify templates exist
ls -la src/templates/

# If missing, source files may not be in src/
# Check if they're still in washington_water_data/
ls -la washington_water_data/
```

### Generated HTML looks wrong

```bash
# Check converter
ls -la src/convert_md_to_html.py

# Test manually
python3 src/convert_md_to_html.py
```

## Maintenance

### Weekly
- None (project is stable)

### When EPA Releases New Data
1. Download to `data/[State]/`
2. Parse: `python3 src/parse_washington_data.py`
3. Create SQLite: (see "Adding a New State")
4. Rebuild: `./build.sh`

### When Students Report Issues
1. Update docs in `src/templates/`
2. Update scripts in `src/Python_Scripts/`
3. Rebuild: `./build.sh washington [version]`
4. Test thoroughly
5. Distribute

## Distribution

### File
`dist/washington_water_data_v1.3.tar.gz` (~79 MB)

### Methods
- USB drives (most reliable)
- Cloud storage (Google Drive, Dropbox)
- Course management system
- Network share
- Web server download

### Student Instructions
1. Extract archive
2. Open `README.html` in browser
3. Follow installation for their OS
4. Run Python scripts

---

**Last Updated**: 2025-11-15
**Current Version**: 1.3 (without browser console)
**Scripts**: build.sh, reorganize.sh (both pass shellcheck ✓)
