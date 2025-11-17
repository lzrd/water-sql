# Adding Water Quality Data for Other States

This guide explains how to add EPA STORET water quality data for Oregon, California, Illinois, or any other state to create educational packages similar to the Washington State package.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding the Data Format](#understanding-the-data-format)
3. [Step-by-Step Instructions](#step-by-step-instructions)
4. [State-Specific Examples](#state-specific-examples)
5. [Troubleshooting](#troubleshooting)
6. [For Instructors](#for-instructors)

---

## Quick Start

If you want to add a new state, here's the fastest path using the `Makefile`:

```bash
# 1. Clean any previous build artifacts
make clean

# 2. Prepare the state database (downloads, parses, imports, compresses)
#    Replace 'oregon' and 'OR' with your desired state name and code.
make prepare-state-db STATE_NAME=oregon STATE_CODE=OR

# 3. Build the student package
make build STATE_NAME=oregon

# 4. Test the generated package
make test-package STATE_NAME=oregon STATE_CODE=OR

# Done! Package is at: dist/oregon_water_data_v<VERSION>.zip
```

---

## Understanding the Data Format

### EPA STORET Data Structure

EPA STORET (STOrage and RETrieval) is a water quality database maintained by the Environmental Protection Agency. States submit data in a standardized tab-delimited text format.

### Required Files

For each state, you need files following this pattern:

```
data/Oregon/                          # State directory
├── OR_Multnomah_inv.txt             # Inventory (parameters) for Multnomah County
├── OR_Multnomah/                    # Multnomah County subdirectory
│   ├── OR_Multnomah_sta_001.txt     # Station metadata (file 1)
│   ├── OR_Multnomah_sta_002.txt     # Station metadata (file 2)
│   ├── OR_Multnomah_res_001.txt     # Results data (file 1)
│   └── OR_Multnomah_res_002.txt     # Results data (file 2)
├── OR_Clackamas_inv.txt             # Inventory for Clackamas County
├── OR_Clackamas/
│   ├── OR_Clackamas_sta_001.txt
│   └── OR_Clackamas_res_001.txt
└── ... (repeat for each county)
```

### File Naming Convention

**Pattern**: `{STATE}_{County}_{type}_{number}.txt`

- `STATE`: Two-letter abbreviation (WA, OR, CA, IL)
- `County`: County name (underscores for spaces, e.g., `San_Francisco`)
- `type`: File type:
  - `inv` - Inventory (parameter definitions)
  - `sta` - Station metadata
  - `res` - Results (measurements)
- `number`: Sequential file number (001, 002, etc.)

### File Format

All files are **tab-delimited text** with:
- Line 1: Column headers
- Line 2: Separator line (dashes)
- Line 3+: Data rows

**Encoding**: `latin-1` (not UTF-8)

---

## Step-by-Step Instructions

### Step 1: Obtain EPA STORET Legacy Data

#### Option A: EPA STORET Legacy FTP Site (Primary Method)

**This is the same source used for the Washington data.**

**Web Browser Method (Easiest)**:
1. Open in browser: `https://gaftp.epa.gov/storet/exports/`
2. Navigate to your state's folder or download state archive file
3. Save to `data/Illinois/` directory
4. Extract if archived

**FTP Command Line Method**:
```bash
# Connect to FTP site
ftp gaftp.epa.gov
# Username: anonymous
# Password: your-email@example.com

# Navigate to exports directory
cd storet/exports

# List available files
ls -la

# Download your state's archive (e.g., illinois.zip)
get illinois.zip

# Exit FTP
quit

# Extract the archive
unzip illinois.zip -d data/Illinois
```

**curl Method (Recommended for automated downloads)**:
```bash
cd data
STATE=Illinois
curl -O https://gaftp.epa.gov/Storet/exports/$STATE.zip
cd ..
```

**See `docs/DATA_SOURCES.md` for complete FTP instructions.**

#### Option B: Request from EPA Directly

If the FTP site is inaccessible:

**Email**: storet@epa.gov
**Subject**: "Request for STORET Legacy Data - [State Name]"
**Request**: "Tab-delimited flat files for [State], organized by county, in the legacy STORET format"

#### Option C: Request from State Environmental Agency

Many states maintain their own water quality databases:

- **Oregon**: Oregon DEQ (Department of Environmental Quality)
- **California**: California Water Quality Monitoring Council
- **Illinois**: Illinois EPA

Contact the agency and request:
- Historical water quality monitoring data
- EPA STORET format (preferred)
- County-level organization
- Time range: as much as available

### Step 2: Organize Data Files

Create a directory structure:

```bash
# Create state directory
mkdir -p data/Oregon

# Move/copy your downloaded files into this directory
# Ensure they follow the naming pattern: OR_County_inv.txt, etc.
```

**Verify your files**:
```bash
ls -la data/Oregon/
# Should show:
#   OR_Multnomah_inv.txt
#   OR_Multnomah/
#   OR_Clackamas_inv.txt
#   OR_Clackamas/
#   ... etc.
```

### Step 3: Parse the Data

Use the generalized state parser:

```bash
python3 src/parse_state_data.py data/Oregon \
    --state-abbr OR \
    --state-name Oregon \
    --output build/output_oregon
```

**What this does**:
1. Reads all `OR_*_inv.txt` files to extract parameter definitions
2. Reads all `OR_*/OR_*_sta_*.txt` files to extract station information
3. Reads all `OR_*/OR_*_res_*.txt` files to extract measurement results
4. Generates CSV files in `build/output_oregon/`:
   - `parameters.csv` - Parameter definitions
   - `stations.csv` - Monitoring station metadata
   - `results.csv` - Water quality measurements
   - `schema.sql` - SQLite database schema
   - `import_to_sqlite.sh` - Automated import script

**Expected output**:
```
======================================================================
EPA STORET Data Parser - Oregon
======================================================================

Parsing inventory files (OR_*_inv.txt)...
  ✓ Found 1,234 unique parameters

Parsing station files (OR_*/OR_*_sta_*.txt)...
  ✓ Found 4,567 unique stations

Parsing result files (OR_*/OR_*_res_*.txt)...
  Processed 100,000 results...
  Processed 200,000 results...
  ✓ Found 2,345,678 total results

Writing CSV files to build/output_oregon/...
  ✓ Wrote 1,234 parameters to parameters.csv
  ✓ Wrote 4,567 stations to stations.csv
  ✓ Wrote 2,345,678 results to results.csv
  ✓ Wrote SQLite schema to schema.sql
  ✓ Wrote import script to import_to_sqlite.sh

======================================================================
✓ Parsing complete!
======================================================================

Summary:
  Parameters: 1,234
  Stations:   4,567
  Results:    2,345,678

Next steps:
  cd build/output_oregon
  ./import_to_sqlite.sh
```

### Step 4: Create SQLite Database

```bash
cd build/output_oregon
./import_to_sqlite.sh
```

**What this does**:
1. Creates `build/oregon_water.db`
2. Imports schema (tables and indexes)
3. Imports parameters (fast)
4. Imports stations (fast)
5. Imports results (may take 5-10 minutes for millions of rows)

**Expected output**:
```
================================================================
Importing Oregon Water Quality Data to SQLite
================================================================

[1/4] Creating database schema...
  ✓ Schema created

[2/4] Importing parameters...
  ✓ Imported 1234 parameters

[3/4] Importing stations...
  ✓ Imported 4567 stations

[4/4] Importing results (this may take several minutes)...
  ✓ Imported 2345678 results

Verifying indexes...
  ✓ Indexes created

================================================================
✓ Import complete!
================================================================
Database: ../oregon_water.db
Size: 245M

To test:
  sqlite3 ../oregon_water.db
  sqlite> SELECT COUNT(*) FROM results;
  sqlite> SELECT COUNT(*) FROM stations;
  sqlite> .quit
```

### Step 5: Test the Database

```bash
cd ../..  # Return to project root

# Test basic queries
sqlite3 build/oregon_water.db "SELECT COUNT(*) FROM results;"
sqlite3 build/oregon_water.db "SELECT COUNT(*) FROM stations;"
sqlite3 build/oregon_water.db "SELECT DISTINCT county FROM stations ORDER BY county;"

# Test with Python analysis script
cd build
cp oregon_water.db package/oregon_water.db
cd package/Python_Scripts
python3 analyze_water_quality_sqlite.py
```

### Step 6: Build Student Package

Once the database is prepared, build the student package using the `make build` command:

```bash
# From the project root directory
make build STATE_NAME=oregon
```

**What this does**:
1. Copies the compressed database, documentation, and Python scripts into a temporary package directory.
2. Converts Markdown documentation to HTML.
3. Generates sample visualizations.
4. Creates a `MANIFEST.txt` file.
5. Archives the package into a `.zip` file in the `dist/` directory.

**Output**: `dist/oregon_water_data_v<VERSION>.zip` (replace `<VERSION>` with the current project version).

### Step 7: Test the Package

After building, it's crucial to test the generated package to ensure everything works as expected for students:

```bash
# From the project root directory
make test-package STATE_NAME=oregon STATE_CODE=OR
```

**What this does**:
1. Extracts the `.zip` package to a temporary location.
2. Installs Python dependencies required by the analysis scripts.
3. Runs the main Python analysis script (`analyze_water_quality_sqlite.py`) to verify its functionality and visualization generation.
4. Cleans up the temporary test directory.

**Expected output**: A success message if the script runs without errors, indicating the package is ready for distribution.

---

## State-Specific Examples

### Oregon

```bash
# Assuming data in data/Oregon/
python3 src/parse_state_data.py data/Oregon -s OR -n Oregon -o build/output_oregon
cd build/output_oregon
./import_to_sqlite.sh
cd ../..
./build.sh oregon 1.0
```

### California

```bash
# Assuming data in data/California/
python3 src/parse_state_data.py data/California -s CA -n California -o build/output_california
cd build/output_california
./import_to_sqlite.sh
cd ../..
./build.sh california 1.0
```

### Illinois

```bash
# Assuming data in data/Illinois/
python3 src/parse_state_data.py data/Illinois -s IL -n Illinois -o build/output_illinois
cd build/output_illinois
./import_to_sqlite.sh
cd ../..
./build.sh illinois 1.0
```

---

## Updating build.sh

The current `build.sh` expects the database to be named `build/washington_water.db` and copies it as `washington_water.db` in the package. To support multiple states:

### Option 1: Quick Edit (Manual)

For each state, manually edit line 32-33 in `build.sh`:

```bash
# Change this:
cp "build/${STATE}_water.db" build/package/washington_water.db

# To this (for Oregon):
cp "build/oregon_water.db" build/package/oregon_water.db
```

### Option 2: Enhanced build.sh (Recommended)

Replace lines 26-34 in `build.sh` with:

```bash
# Step 2: Database
echo "[2/9] Copying SQLite database..."
DB_SOURCE="build/${STATE}_water.db"
DB_TARGET="build/package/${STATE}_water.db"

if [ ! -f "$DB_SOURCE" ]; then
    echo "  ✗ ERROR: Database not found: $DB_SOURCE"
    echo "  → Run parser and import first:"
    echo "     python3 src/parse_state_data.py data/${STATE^} -s ${STATE:0:2} -n ${STATE^}"
    echo "     cd build/output_${STATE}"
    echo "     ./import_to_sqlite.sh"
    exit 1
fi

cp "$DB_SOURCE" "$DB_TARGET"
DB_SIZE=$(stat -c %s "$DB_TARGET" | numfmt --to=iec-i --suffix=B)
echo "  ✓ Database: $DB_SIZE"
```

This makes `build.sh` automatically use the correct database name based on the state parameter.

---

## Troubleshooting

### Problem: "No inventory files found"

**Symptoms**:
```
Parsing inventory files (OR_*_inv.txt)...
  Warning: No inventory files found matching OR_*_inv.txt
  ✓ Found 0 unique parameters
```

**Solutions**:
1. **Check file naming**: Files must match pattern `{STATE}_{County}_inv.txt`
   ```bash
   # Wrong: Oregon_Multnomah_inv.txt
   # Right: OR_Multnomah_inv.txt
   ```

2. **Check state abbreviation**: Use the `-s` flag correctly
   ```bash
   # Wrong: -s Oregon
   # Right: -s OR
   ```

3. **Check directory structure**:
   ```bash
   ls -la data/Oregon/
   # Should show files like: OR_Multnomah_inv.txt
   ```

### Problem: "No station files found"

**Symptoms**:
```
Parsing station files (OR_*/OR_*_sta_*.txt)...
  Warning: No station files found matching OR_*/OR_*_sta_*.txt
```

**Solutions**:
1. **Check subdirectories exist**:
   ```bash
   ls -la data/Oregon/
   # Should show directories like: OR_Multnomah/
   ```

2. **Check files in subdirectories**:
   ```bash
   ls -la data/Oregon/OR_Multnomah/
   # Should show: OR_Multnomah_sta_001.txt, OR_Multnomah_res_001.txt
   ```

### Problem: "Unable to open database file"

**Symptoms**:
```bash
Error: unable to open database "oregon_water.db": unable to open database file
```

**Solutions**:
1. **Check database was created**:
   ```bash
   ls -lh build/oregon_water.db
   ```

2. **Re-run import if database is missing**:
   ```bash
   cd build/output_oregon
   ./import_to_sqlite.sh
   ```

### Problem: Import is very slow

**Expected behavior**: Importing millions of rows takes time
- 1M rows: ~3-5 minutes
- 3M rows: ~8-12 minutes
- 5M+ rows: 15-20 minutes

**Tips**:
- Use an SSD (much faster than HDD)
- Close other applications to free RAM
- Don't interrupt the import process
- The progress messages update every 100,000 rows

### Problem: File encoding errors

**Symptoms**:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x92 in position 1234
```

**Solution**: EPA STORET files use `latin-1` encoding, which the parser handles automatically. If you still see this error:

```bash
# Verify file encoding
file -bi data/Oregon/OR_Multnomah_inv.txt
# Should show: charset=iso-8859-1 or charset=us-ascii
```

If files are in a different encoding, convert them:
```bash
iconv -f WINDOWS-1252 -t UTF-8 original.txt > converted.txt
```

### Problem: Different data format

**Symptoms**: Data doesn't match expected column structure

**Solution**: EPA STORET format can vary slightly. Check your actual column headers:

```bash
head -3 data/Oregon/OR_Multnomah_inv.txt
```

If headers don't match expectations, you may need to:
1. Map your columns to the expected format
2. Modify `parse_state_data.py` to handle your specific format
3. Convert data to match EPA STORET format

---

## For Instructors

### Data Sources for Common States

| State | Source | Contact |
|-------|--------|---------|
| **Oregon** | Oregon DEQ | waterqualitydata@deq.oregon.gov |
| **California** | CA Water Quality Portal | https://www.waterqualitydata.us/ |
| **Illinois** | Illinois EPA | epa.water@illinois.gov |
| **Washington** | Already included | - |

### Recommended States for Education

**Best for beginners**:
- Washington (already included)
- Oregon (similar size and structure)
- Vermont (smaller dataset, easier to explore)

**Best for advanced students**:
- California (very large dataset, diverse geography)
- Texas (large state, varied water types)
- Florida (coastal + freshwater systems)

### Customizing Documentation

After building a package for a new state, update the student-facing documentation:

```bash
# Edit template files
vim src/templates/README.md
# Change "Washington State" to "Oregon" throughout

vim src/templates/Documentation/WATER_DATA.md
# Update state-specific examples

# Rebuild package with updated docs
./build.sh oregon 1.0
```

### Multi-State Packages

You can create a combined package with data from multiple states:

1. Parse each state separately
2. Import each into its own database
3. Either:
   - Include multiple database files in package
   - Merge data into single database (advanced)

Example structure:
```
package/
├── washington_water.db
├── oregon_water.db
├── california_water.db
└── Python_Scripts/
    └── analyze_multi_state.py
```

### Quality Control Checklist

Before distributing a new state package:

- [ ] Database size is reasonable (< 500 MB preferred)
- [ ] All tables have data (parameters, stations, results)
- [ ] Sample queries return expected results
- [ ] Analysis scripts generate visualizations successfully
- [ ] README and INSTALL docs mention correct state name
- [ ] Package extracts cleanly
- [ ] Student can run scripts without errors
- [ ] File size of .tar.gz is reasonable for distribution

### Student Assignments

Ideas for comparative assignments with multi-state data:

1. **Geographic Comparison**: Compare water quality between states
2. **Time Series Analysis**: Identify long-term trends
3. **Parameter Focus**: Deep dive into specific pollutants (pH, dissolved oxygen, etc.)
4. **Station Density**: Analyze monitoring coverage by state
5. **Data Quality**: Identify gaps in monitoring data

---

## Advanced Topics

### Combining States into One Database

```bash
# Parse both states
python3 src/parse_state_data.py data/Oregon -s OR -n Oregon -o build/output_oregon
python3 src/parse_state_data.py data/California -s CA -n California -o build/output_ca

# Create combined database
sqlite3 build/western_states.db < build/output_oregon/schema.sql

# Import Oregon data
cd build/output_oregon
sqlite3 ../western_states.db <<EOF
.mode csv
.import --skip 1 parameters.csv parameters
.import --skip 1 stations.csv stations
.import --skip 1 results.csv results
EOF

# Import California data (appends to existing tables)
cd ../output_california
sqlite3 ../western_states.db <<EOF
.mode csv
.import --skip 1 parameters.csv parameters
.import --skip 1 stations.csv stations
.import --skip 1 results.csv results
EOF
```

### Filtering Large Datasets

For very large states, you may want to filter data:

```bash
# Option 1: Parse only specific counties
# Remove unwanted county directories before parsing
rm -rf data/California/CA_Los_Angeles/

# Option 2: Filter by date range (modify CSV after parsing)
# Filter results.csv to only include data after 2000
awk -F',' '$4 >= "2000-01-01" || NR==1' results.csv > results_filtered.csv
```

---

## Summary

**To add a new state**:

1. Get EPA STORET data files
2. Organize into `data/{State}/` directory
3. Run `parse_state_data.py` with correct state abbreviation
4. Run generated `import_to_sqlite.sh` script
5. Update `build.sh` (if needed)
6. Build package with `./build.sh {state} 1.0`
7. Test package before distribution

**Tools provided**:
- `src/parse_state_data.py` - Universal state data parser
- Auto-generated `import_to_sqlite.sh` - Database import automation
- `build.sh` - Package builder (may need state-specific edits)

**Time required**:
- Initial setup: 30-60 minutes
- Parsing: 5-15 minutes (depends on data size)
- Database import: 5-20 minutes (depends on data size)
- Testing: 15-30 minutes

**Total**: 1-2 hours for first new state, faster for subsequent states

---

**Questions?** Check the main project `docs/README.md` or `CLAUDE.md` for additional details.
