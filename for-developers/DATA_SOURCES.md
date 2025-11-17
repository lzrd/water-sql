# EPA STORET Legacy Data Sources

This document explains how to obtain EPA STORET Legacy data for different states to use with this project.

## About STORET Legacy Data

**STORET** = STOrage and RETrieval

The **EPA STORET Legacy Data Center (LDC)** contains historical water quality data:
- **Time Range**: Early 20th century through end of 1998
- **Format**: Tab-delimited text files
- **Organization**: By state and county
- **Status**: Archived (no new data added after 1998)

The Legacy system has been replaced by the modern WQX (Water Quality Exchange) framework, but legacy data remains available for download.

## Primary Data Source: EPA FTP Site

### FTP Location

**Main FTP Site**: `https://gaftp.epa.gov/storet/exports/`

**Alternative (FTP protocol)**: `ftp://gaftp.epa.gov/storet/exports/`

This site contains compressed, self-extracting flat files organized by state.

### File Structure

Each state archive contains:
- `{STATE}_{County}_inv.txt` - Parameter inventory files
- `{STATE}_{County}/` - County subdirectories containing:
  - `{STATE}_{County}_sta_*.txt` - Station metadata files
  - `{STATE}_{County}_res_*.txt` - Results (measurements) files

Where `{STATE}` is the two-letter state abbreviation (WA, OR, CA, IL, etc.)

## Downloading Data

### Method 1: Command Line (Linux/macOS)

```bash
# Create directory for state data
mkdir -p data/Illinois

# Navigate to the directory
cd data/Illinois

# Connect to FTP and download Illinois data
ftp gaftp.epa.gov
# Login as: anonymous
# Password: your-email@example.com

cd storet/exports
# List available files
ls -la

# Download Illinois archive (filename may vary)
get illinois.zip
# or
get il.tar.gz
# or similar

quit

# Extract the archive
unzip illinois.zip
# or
tar -xzf il.tar.gz
```

### Method 2: FTP Client (Windows/macOS/Linux)

Use an FTP client like FileZilla:

1. **Host**: `gaftp.epa.gov`
2. **Username**: `anonymous`
3. **Password**: `your-email@example.com`
4. **Port**: 21 (default FTP)
5. **Navigate to**: `/storet/exports/`
6. **Download**: The appropriate state archive file

### Method 3: Web Browser

Open directly in a browser:
```
https://gaftp.epa.gov/storet/exports/
```

This HTTPS site allows browsing and downloading files directly - the easiest method!

## Available States

States with EPA STORET Legacy data include:

| State | Abbreviation | Likely Filename |
|-------|--------------|-----------------|
| Washington | WA | washington.zip or wa.tar.gz |
| Oregon | OR | oregon.zip or or.tar.gz |
| California | CA | california.zip or ca.tar.gz |
| Illinois | IL | illinois.zip or il.tar.gz |
| New York | NY | newyork.zip or ny.tar.gz |
| Texas | TX | texas.zip or tx.tar.gz |
| Florida | FL | florida.zip or fl.tar.gz |
| ... | ... | ... |

**Note**: Exact filenames may vary. Check the FTP directory listing for current file names.

## After Downloading

### 1. Extract the Archive

```bash
# If .zip format
unzip illinois.zip -d data/Illinois

# If .tar.gz format
tar -xzf illinois.tar.gz -C data/Illinois

# If self-extracting .exe (Windows)
# Double-click the file and choose extraction directory
```

### 2. Verify File Structure

```bash
ls -la data/Illinois/

# Should see files like:
# IL_Adams_inv.txt
# IL_Adams/
# IL_Cook_inv.txt
# IL_Cook/
# etc.
```

### 3. Check County Subdirectories

```bash
ls -la data/Illinois/IL_Cook/

# Should see files like:
# IL_Cook_sta_001.txt
# IL_Cook_sta_002.txt
# IL_Cook_res_001.txt
# IL_Cook_res_002.txt
# etc.
```

### 4. Parse the Data

```bash
python3 src/parse_state_data.py data/Illinois -s IL -n Illinois -o build/output_illinois
```

## Alternative: Contact EPA Directly

If FTP site is inaccessible or you need specific data:

### STORET Helpdesk
- **Email**: storet@epa.gov
- **Subject**: "Request for STORET Legacy Data - Illinois"
- **Request**: Tab-delimited flat files for Illinois, organized by county

### WQX Support
- **Email**: WQX@epa.gov
- **Phone**: 1-800-424-9067 (EPA Agency Contact Center)

### What to Request

```
Hello,

I am requesting EPA STORET Legacy Data for Illinois in the original
tab-delimited flat file format, organized by county.

Specifically, I need:
- Parameter inventory files (IL_{County}_inv.txt)
- Station metadata files (IL_{County}_sta_*.txt)
- Results data files (IL_{County}_res_*.txt)

This data will be used for educational purposes to teach students
about water quality analysis and SQL databases.

Time range: All available legacy data (pre-1999)

Thank you,
[Your Name]
```

## Known Issues

### FTP Site Changes

The EPA FTP site has gone through several transitions:
- Old site: `ftp.epa.gov/storet/`
- Previous site: `newftp.epa.gov/storet/exports/`
- **Current site**: `gaftp.epa.gov/storet/exports/` (HTTPS and FTP)

**HTTPS access** (https://gaftp.epa.gov/) is now available and recommended as the easiest method.

If the site is down or moved, contact EPA for current data access methods.

### File Encoding

STORET Legacy files use **latin-1** (ISO-8859-1) encoding, not UTF-8.

Our parser handles this automatically:
```python
with open(filepath, 'r', encoding='latin-1') as f:
```

### Large File Sizes

State archives can be large:
- **Small states**: 10-50 MB compressed
- **Medium states**: 100-300 MB compressed
- **Large states**: 500 MB - 2 GB compressed

Ensure you have adequate disk space and bandwidth.

## Modern Data: Water Quality Portal

For data after 1998, use the **Water Quality Portal**:

**URL**: https://www.waterqualitydata.us/

### Differences from Legacy Data

| Feature | Legacy STORET | Modern WQP |
|---------|---------------|------------|
| Time Range | Pre-1999 | 1999-Present |
| Format | County-organized files | Query-based download |
| File Structure | Fixed (inv/sta/res) | Flexible (various profiles) |
| Compatibility | Direct (our parser) | May need adaptation |

### Using WQP Data

If you download from Water Quality Portal:
1. Select tab-separated format
2. Download may not be organized by county
3. May need to reorganize files to match expected structure
4. Or adapt parser to handle WQP format

## Testing Downloaded Data

Before running full parse, verify data integrity:

```bash
# Check file count
find data/Illinois -name "*.txt" | wc -l

# Check a few files are readable
head -20 data/Illinois/IL_Cook_inv.txt
head -20 data/Illinois/IL_Cook/IL_Cook_sta_001.txt

# Check file encoding
file -bi data/Illinois/IL_Cook_inv.txt
# Should show: charset=iso-8859-1 or charset=us-ascii

# Test with small parse
python3 src/parse_state_data.py data/Illinois -s IL -n Illinois -o /tmp/test_il
```

## Data Documentation

Each state archive should include documentation files:
- `README.txt` - General information
- `{STATE}__matrix.txt` - Data summary matrix (like Washington)
- Agency contact information

## Data Use and Citation

### Appropriate Use

EPA STORET Legacy data is public domain and freely available for:
- Educational purposes
- Research
- Environmental analysis
- Public information

### Recommended Citation

```
U.S. Environmental Protection Agency (EPA). [Year].
STORET Legacy Data for [State].
Retrieved from https://gaftp.epa.gov/storet/exports/
Accessed [Date].
```

Example:
```
U.S. Environmental Protection Agency (EPA). 2002.
STORET Legacy Data for Illinois.
Retrieved from https://gaftp.epa.gov/storet/exports/
Accessed November 15, 2025.
```

## Quick Reference

### Illinois Data Download

**Easiest Method - Web Browser**:
1. Open: https://gaftp.epa.gov/storet/exports/
2. Click on Illinois data file
3. Save to `data/Illinois/`

**Command Line**:
```bash
# Using wget
cd data/Illinois
wget -r -np -nH --cut-dirs=2 https://gaftp.epa.gov/storet/exports/illinois/
cd ../..

# Or using FTP
ftp gaftp.epa.gov
# User: anonymous
# Pass: your.email@example.com

cd storet/exports
ls il*
get illinois.zip
quit

# Extract
unzip illinois.zip -d data/Illinois

# Verify
ls -la data/Illinois/

# Parse
python3 src/parse_state_data.py data/Illinois -s IL -n Illinois -o build/output_illinois

# Import
cd build/output_illinois
./import_to_sqlite.sh
cd ../..

# Build package
./build.sh illinois 1.0
```

## Support

If you encounter issues:
1. Try web browser method: `https://gaftp.epa.gov/storet/exports/`
2. Check FTP site is accessible: `ping gaftp.epa.gov`
3. Try alternative FTP client
4. Contact EPA STORET helpdesk: storet@epa.gov
5. Check modern WQP as alternative: https://www.waterqualitydata.us/

---

**Last Updated**: 2025-11-15
**FTP Site Status**: Check with EPA if inaccessible
**Data Format**: Tab-delimited text (latin-1 encoding)
**Time Range**: Pre-1999 (Legacy), 1999+ (Modern WQP)
