# Water Quality Data Analysis - For Developers

Technical documentation for contributors to this educational data science project.

## Project Overview

This project builds student-friendly educational packages containing EPA STORET water quality data. The system supports multiple U.S. states and provides complete automation from data download to distribution.

## Quick Links

**Architecture and Design:**
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design, schema, data pipeline
- **[AUTOMATION.md](AUTOMATION.md)** - Build system and automation details
- **[DATA_SOURCES.md](DATA_SOURCES.md)** - EPA STORET format documentation

**Contributing:**
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to this project

## System Architecture

### Data Pipeline

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
    ↓ GitHub Actions or build.sh
Student Package (~80 MB, .zip) ← DISTRIBUTE
```

### Directory Structure

```
water-sql/
├── for-students/          # Student documentation (copied to packages)
├── for-teachers/          # Teacher guides and curriculum alignment
├── for-developers/        # Technical documentation (you are here)
├── src/
│   ├── parse_state_data.py          # Universal state parser
│   ├── export_to_sqlite.py          # PostgreSQL → SQLite (legacy)
│   ├── convert_md_to_html.py        # Markdown → HTML conversion
│   ├── templates/                   # Package templates (legacy location)
│   └── Python_Scripts/              # Student analysis scripts
├── scripts/
│   ├── download_state_data.sh       # Download EPA data
│   ├── build_state_package.sh       # Complete build pipeline
│   ├── compress_database.sh         # Compress with xz
│   └── decompress_database.sh       # Decompress for builds
├── build.sh                         # Main build script
├── data/storet/                     # Downloaded EPA data
└── build/                           # Build artifacts (.db, .db.xz)
```

### Database Schema

Three normalized tables:

```sql
-- Parameter definitions (1,500+ parameters)
CREATE TABLE parameters (
    code TEXT PRIMARY KEY,
    short_name TEXT,
    long_name TEXT
);

-- Monitoring stations (thousands per state)
CREATE TABLE stations (
    station_id TEXT PRIMARY KEY,
    station_name TEXT,
    agency TEXT,
    state TEXT,
    county TEXT,
    latitude REAL,
    longitude REAL,
    huc TEXT,
    station_type TEXT,
    description TEXT
);

-- Measurement results (millions per state)
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agency TEXT,
    station_id TEXT,
    param_code TEXT,
    start_date TEXT,           -- ISO: YYYY-MM-DD
    start_time TEXT,           -- Special codes: "2500"=noon, "0001"=unknown
    result_value TEXT,         -- Kept as TEXT (various formats/units)
    huc TEXT,
    sample_depth TEXT,
    FOREIGN KEY (station_id) REFERENCES stations(station_id),
    FOREIGN KEY (param_code) REFERENCES parameters(code)
);
```

**Indexes**: station_id, param_code, start_date, county

See **[ARCHITECTURE.md](ARCHITECTURE.md)** for complete schema details.

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/water-sql.git
cd water-sql

# Install Python dependencies
pip install -r requirements.txt

# Test parser on sample state
./scripts/build_state_package.sh Washington WA 1.0
```

### Build System Commands

```bash
# Download EPA data for a state
./scripts/download_state_data.sh Oregon

# Parse EPA data to CSV
python3 src/parse_state_data.py data/Oregon -s OR -n Oregon -o build/output_oregon

# Import CSV to SQLite (auto-generated script)
cd build/output_oregon
./import_to_sqlite.sh
cd ../..

# Compress database for version control
./scripts/compress_database.sh oregon

# Build student package
./build.sh oregon 1.0

# Complete pipeline (all of the above)
./scripts/build_state_package.sh Oregon OR 1.0
```

### Testing Changes

```bash
# Test database creation
python3 src/parse_state_data.py data/Washington -s WA -n Washington -o build/test_output

# Test analysis scripts
cd build/package/Python_Scripts
python3 analyze_water_quality_sqlite.py

# Test package build
./build.sh washington 1.3.3

# Extract and test package
cd /tmp && unzip ~/path/to/dist/washington_water_data_v1.3.3.zip
cd package && open index.html
```

### GitHub Actions

Workflow: `.github/workflows/release.yml`

**Triggered by:**
- Push to `main` branch
- Changes to `build/*.db.xz` files
- Changes to `src/**`
- Manual trigger

**Matrix Build:**
```yaml
matrix:
  state:
    - name: washington
      version: "1.3.3"
    - name: illinois
      version: "1.0"
```

See **[AUTOMATION.md](AUTOMATION.md)** for complete CI/CD details.

## Common Development Tasks

### Adding a New State

1. Download and process:
   ```bash
   ./scripts/build_state_package.sh Oregon OR 1.0
   ```

2. Test the package locally

3. Commit compressed database:
   ```bash
   git add build/oregon_water.db.xz
   git commit -m "Add Oregon water quality database"
   ```

4. Update GitHub Actions workflow:
   ```yaml
   - name: oregon
     version: "1.0"
   ```

5. Push to trigger automatic releases

See **for-teachers/ADDING_STATES.md** for complete guide.

### Modifying Documentation

Documentation is organized by audience:

```bash
for-students/       # Edit here, build.sh copies to packages
for-teachers/       # Teacher guides
for-developers/     # Technical docs (you are here)
```

After editing `for-students/` content:
```bash
./build.sh washington 1.3.3
# Test the package to verify changes
```

### Adding Features to Analysis Scripts

1. Edit `src/Python_Scripts/analyze_water_quality_sqlite.py`
2. Test locally:
   ```bash
   python3 src/Python_Scripts/analyze_water_quality_sqlite.py
   ```
3. Run build to include in distribution:
   ```bash
   ./build.sh washington 1.3.3
   ```

### Modifying the Parser

The parser (`src/parse_state_data.py`) handles EPA STORET format:

**Key functions:**
- `parse_inventory()`: Parse parameter definitions (`*_inv.txt`)
- `parse_stations()`: Parse station metadata (`*_sta_*.txt`)
- `parse_results()`: Parse measurement results (`*_res_*.txt`)

**Testing parser changes:**
```bash
python3 src/parse_state_data.py data/Washington -s WA -n Washington -o build/test_parse
cd build/test_parse
./import_to_sqlite.sh
sqlite3 washington_water.db "SELECT COUNT(*) FROM results;"
```

## Key Design Decisions

### 1. SQLite Over PostgreSQL for Distribution
- No server setup for students
- Single portable file
- Performance adequate for 3M+ rows with indexes

### 2. Compressed Databases in Git (.db.xz)
- 371 MB → ~80 MB (78% reduction)
- Fits in git without LFS
- Fast rebuilds (< 1 minute decompression)
- Deterministic builds

### 3. Audience-Specific Documentation
- `for-students/`: Student-facing tutorials
- `for-teachers/`: Curriculum alignment, lesson plans
- `for-developers/`: Technical architecture

### 4. Three Analysis Scripts
- `analyze_water_quality_sqlite.py`: Basic version
- `analyze_water_quality_annotated.py`: Educational (600+ comment lines)
- `analyze_water_quality_dual.py`: PostgreSQL/SQLite comparison

### 5. Normalized Schema
- Three tables with foreign keys
- `result_value` as TEXT (preserves qualifiers like "<0.5")
- Indexes on high-cardinality columns

### 6. Line Endings
- `.gitattributes` enforces LF for scripts/Python/markdown
- Binary files (.db, .xz, .zip) not normalized
- Cross-platform compatibility (Windows/macOS/Linux)

## Code Style and Conventions

### Python
- PEP 8 style guide
- Type hints preferred
- Docstrings for all functions
- Handle encoding explicitly (`latin-1` for EPA files)

### Bash
- Use `set -e` for early exit on errors
- Quote variables: `"$VAR"`
- Check prerequisites before running
- Provide helpful error messages

### SQL
- Uppercase keywords: `SELECT`, `FROM`, `WHERE`
- Lowercase table/column names
- Use table aliases for joins
- Comment complex queries

### Documentation
- Markdown for all docs
- GitHub-flavored markdown
- Code examples in fenced blocks with language tags
- Student-facing: conversational tone
- Developer-facing: technical precision

## Testing

### Manual Testing Checklist
- [ ] Parser creates correct CSV files
- [ ] SQLite import completes without errors
- [ ] Database has expected row counts
- [ ] Compression reduces file size significantly
- [ ] Package extracts correctly
- [ ] Documentation converts to HTML properly
- [ ] Analysis scripts run without errors
- [ ] Visualizations generate correctly

### Automated Testing
Currently minimal. Opportunities for contribution:
- Unit tests for parser functions
- Database schema validation
- Query correctness tests
- Documentation link checking

## Performance Considerations

### Parser Performance
- Tab-delimited format: fast with Python `csv` module
- Memory-efficient: streaming writes to CSV
- Typical parse time: 5-15 minutes for 500 MB STORET data

### Database Performance
- Indexes critical for query performance
- `ANALYZE` command after import updates statistics
- `result_value` as TEXT avoids type conversion overhead

### Build Performance
- Compression: 2-5 minutes (xz -9 -e)
- Decompression: 10-20 seconds
- Package bundling: < 30 seconds

## Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for:
- Code review process
- Pull request guidelines
- Commit message conventions
- Issue reporting

## Resources

### EPA STORET
- STORET exports: https://gaftp.epa.gov/Storet/exports/
- Water quality data: https://www.epa.gov/waterdata
- Parameter definitions: https://www.epa.gov/waterdata/water-quality-data-upload-definitions

### Technologies
- SQLite documentation: https://www.sqlite.org/docs.html
- pandas documentation: https://pandas.pydata.org/docs/
- matplotlib documentation: https://matplotlib.org/stable/contents.html

## Questions?

- Technical issues: Open an issue on GitHub
- Architecture questions: See **[ARCHITECTURE.md](ARCHITECTURE.md)**
- Build system: See **[AUTOMATION.md](AUTOMATION.md)**
- Data format: See **[DATA_SOURCES.md](DATA_SOURCES.md)**

---

**Ready to contribute?** → [CONTRIBUTING.md](CONTRIBUTING.md)
