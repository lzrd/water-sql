# Quick Reference: Adding States

One-page cheat sheet for adding water quality data from new states.

## Prerequisites

- EPA STORET data files for your state
- Python 3.7+
- sqlite3 command-line tool
- 500 MB - 2 GB free disk space

## Four-Step Process

### 1. Parse Data → CSV

```bash
python3 src/parse_state_data.py data/{State} -s {XX} -n {StateName} -o build/output_{state}
```

**Examples**:
```bash
python3 src/parse_state_data.py data/Oregon -s OR -n Oregon -o build/output_oregon
python3 src/parse_state_data.py data/California -s CA -n California -o build/output_california
python3 src/parse_state_data.py data/Illinois -s IL -n Illinois -o build/output_illinois
```

### 2. Import CSV → SQLite

```bash
cd build/output_{state}
./import_to_sqlite.sh
cd ../..
```

### 3. Test Database

```bash
sqlite3 build/{state}_water.db "SELECT COUNT(*) FROM results;"
sqlite3 build/{state}_water.db "SELECT DISTINCT county FROM stations;"
```

### 4. Build Package

```bash
./build.sh {state} 1.0
```

Output: `dist/{state}_water_data_v1.0.tar.gz`

---

## File Organization Requirements

Your data directory must follow this structure:

```
data/Oregon/
├── OR_County1_inv.txt          # Parameter inventory
├── OR_County1/                 # County subdirectory
│   ├── OR_County1_sta_001.txt  # Station files
│   └── OR_County1_res_001.txt  # Results files
├── OR_County2_inv.txt
├── OR_County2/
│   ├── OR_County2_sta_001.txt
│   └── OR_County2_res_001.txt
└── ...
```

**Naming pattern**: `{STATE}_{County}_{type}_{number}.txt`

---

## State Abbreviations

| State | Abbr | State | Abbr |
|-------|------|-------|------|
| Washington | WA | Oregon | OR |
| California | CA | Illinois | IL |
| New York | NY | Texas | TX |
| Florida | FL | Ohio | OH |

---

## Common Commands

**Check data structure**:
```bash
ls -la data/Oregon/
ls -la data/Oregon/OR_Multnomah/
```

**View file format**:
```bash
head -5 data/Oregon/OR_Multnomah_inv.txt
```

**Check database size**:
```bash
ls -lh build/oregon_water.db
```

**Test database**:
```bash
sqlite3 build/oregon_water.db
sqlite> .schema
sqlite> SELECT COUNT(*) FROM results;
sqlite> .quit
```

**Extract package for testing**:
```bash
mkdir /tmp/test && cd /tmp/test
tar -xzf ~/path/to/dist/oregon_water_data_v1.0.tar.gz
cd package/Python_Scripts
python3 analyze_water_quality_sqlite.py
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No inventory files found" | Check file naming: `OR_County_inv.txt` not `Oregon_County_inv.txt` |
| "No station files found" | Check subdirectories exist: `data/Oregon/OR_County/` |
| "Database not found" | Run `./import_to_sqlite.sh` in `build/output_{state}/` |
| Import is slow | Normal for millions of rows (5-20 min). Use SSD if possible |
| Encoding errors | Files should be `latin-1` encoded (parser handles this) |

---

## Time Estimates

- **Parsing**: 5-15 minutes
- **Import**: 5-20 minutes
- **Testing**: 15-30 minutes
- **Total**: 1-2 hours for first state

---

## Output Files

**After parsing** (`build/output_{state}/`):
- `parameters.csv` - Parameter definitions
- `stations.csv` - Station metadata
- `results.csv` - Measurement data
- `schema.sql` - Database schema
- `import_to_sqlite.sh` - Import script

**After import** (`build/`):
- `{state}_water.db` - SQLite database (200-500 MB typical)

**After build** (`dist/`):
- `{state}_water_data_v1.0.tar.gz` - Student package (80-150 MB typical)

---

## Parser Options

```bash
python3 src/parse_state_data.py --help

# Required:
  data_dir              # Directory with data files

# Optional:
  -s, --state-abbr      # Two-letter abbreviation (default: WA)
  -n, --state-name      # Full state name (default: Washington)
  -o, --output          # Output directory (default: output)
```

---

## Data Sources

### EPA STORET Legacy Site (Primary)

**Web Browser (Easiest)**: https://gaftp.epa.gov/storet/exports/

**FTP**:
```bash
ftp gaftp.epa.gov
# User: anonymous
# Pass: your-email@example.com
# Directory: /storet/exports/
```

**Detailed instructions**: See `docs/DATA_SOURCES.md`

### Alternatives
- **EPA Water Quality Portal**: https://www.waterqualitydata.us/ (modern data, 1999+)
- **State Environmental Agencies**: Contact your state's DEQ/EPA office
- **EPA STORET Helpdesk**: storet@epa.gov (request data files)

---

## Quality Checklist

Before distributing a package:

- [ ] Database < 500 MB (preferred)
- [ ] All three tables have data
- [ ] Sample queries work
- [ ] Analysis scripts generate plots
- [ ] Package extracts cleanly
- [ ] Documentation mentions correct state

---

See `docs/ADDING_STATES.md` for detailed instructions and troubleshooting.
