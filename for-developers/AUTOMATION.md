# Automation System Summary

## What's Been Built

### Complete Automation for Multi-State Packages

Teachers can now create water quality packages for **any U.S. state** with a single command, and GitHub automatically creates releases for students.

---

## For Teachers: Creating a New State Package

### One Command Does Everything:

```bash
./scripts/build_state_package.sh Oregon OR 1.0
```

**What happens automatically:**
1. ✅ Downloads EPA STORET data (~500 MB)
2. ✅ Extracts and parses data
3. ✅ Creates SQLite database
4. ✅ Compresses database for git (371 MB → 80 MB)
5. ✅ Builds student package (zip file, ~80 MB)

**Time:** 10-30 minutes (mostly download time)

---

## For Students: Getting Packages

### Option 1: GitHub Releases (Automatic)

When a teacher pushes a compressed database to `main`:
1. GitHub Actions builds the package
2. Creates a new release
3. Students download zip file
4. No teacher intervention needed!

### Option 2: Direct Distribution

Teacher shares the generated zip file via:
- Email
- Cloud storage (Google Drive, Dropbox)
- Learning management system
- USB drives (for classrooms)

---

## How It Works

### File Flow:

```
EPA STORET Data (online)
    ↓ download_state_data.sh
Raw ZIP file (~500 MB)
    ↓ build_state_package.sh
SQLite Database (371 MB)
    ↓ compress_database.sh
Compressed DB (80 MB) ← CHECK INTO GIT
    ↓ GitHub Actions
Student Package (80 MB) ← DISTRIBUTE TO STUDENTS
```

### Storage Strategy:

**In Git Repository:**
- ✅ `build/washington_water.db.xz` (80 MB compressed)
- ✅ `build/illinois_water.db.xz` (similar size)
- ❌ NOT raw STORET zips (can re-download)
- ❌ NOT uncompressed databases (generated from .xz)

**Why this works:**
- Compressed databases fit in git without LFS
- Fast git operations
- Anyone can rebuild in < 1 minute
- Deterministic builds (everyone uses same data)

---

## Scripts Reference

### `scripts/download_state_data.sh <STATE>`
Downloads EPA STORET data for a state.

```bash
./scripts/download_state_data.sh Washington
```

**Output:** `data/storet/Washington.zip`

---

### `scripts/build_state_package.sh <STATE> <ABBR> <VERSION>`
Complete build process from scratch.

```bash
./scripts/build_state_package.sh Illinois IL 1.0
```

**Does:**
- Downloads data (if needed)
- Parses to CSV
- Imports to SQLite
- Compresses database
- Creates student package

**Output:**
- `build/illinois_water.db.xz` (commit this)
- `dist/illinois_water_data_v1.0.zip` (distribute this)

---

### `scripts/compress_database.sh <STATE>`
Compress an existing database.

```bash
./scripts/compress_database.sh washington
```

**Compression:** ~70-80% reduction (371 MB → 80 MB)

---

### `scripts/decompress_database.sh <STATE>`
Decompress for building (happens automatically).

```bash
./scripts/decompress_database.sh washington
```

**Called by:** `build.sh` automatically

---

## Build System

### Quick Build (Database Already Compressed):

```bash
./build.sh washington 1.3.3
```

**What happens:**
1. Checks for `washington_water.db`
2. If not found, decompresses `washington_water.db.xz`
3. Bundles into student package
4. Creates `dist/washington_water_data_v1.3.3.zip`

**Time:** < 1 minute (just decompression + bundling)

---

## GitHub Actions

### Workflow: `.github/workflows/release.yml`

**Triggered by:**
- Push to `main` branch
- Changes to `build/*.db.xz` files
- Changes to `src/**` (source code)
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

**Steps:**
1. Checkout code
2. Install Python dependencies
3. Decompress databases
4. Build packages (parallel for each state)
5. Upload artifacts
6. Create GitHub Release with all packages

**Result:** Students get URLs like:
```
https://github.com/yourname/water-sql/releases/latest/download/washington_water_data_v1.3.3.zip
https://github.com/yourname/water-sql/releases/latest/download/illinois_water_data_v1.0.zip
```

---

## Adding a New State

### Step 1: Build Locally

```bash
./scripts/build_state_package.sh Oregon OR 1.0
```

**Test the package:**
```bash
cd /tmp
unzip ~/path/to/dist/oregon_water_data_v1.0.zip
cd package
open index.html
```

### Step 2: Commit Compressed Database

```bash
git add build/oregon_water.db.xz
git commit -m "Add Oregon water quality database"
```

### Step 3: Update GitHub Action

Edit `.github/workflows/release.yml`:

```yaml
matrix:
  state:
    - name: washington
      version: "1.3.3"
    - name: illinois
      version: "1.0"
    - name: oregon        # Add this
      version: "1.0"      # Add this
```

### Step 4: Push

```bash
git push
```

**GitHub automatically:**
- Builds Oregon package
- Includes it in next release
- Students can download immediately

---

## Benefits

### For Teachers:
- ✅ One command creates complete package
- ✅ No manual parsing or database work
- ✅ Automated releases via GitHub
- ✅ Consistent structure across all states
- ✅ Can customize documentation once (applies to all states)

### For Students:
- ✅ Download and run immediately
- ✅ No installation complexity
- ✅ Same interface for all states
- ✅ Professional-looking packages
- ✅ Always get latest version from GitHub releases

### For Repository:
- ✅ Compressed databases fit in git
- ✅ Fast builds (< 1 minute from compressed DB)
- ✅ Deterministic (everyone builds from same data)
- ✅ No external dependencies during build
- ✅ Scales to many states

---

## Technical Details

### Compression Details:

**Algorithm:** xz with maximum compression (`-9 -e`)

**Typical results:**
- Washington: 371 MB → 78 MB (79% reduction)
- Compression time: 2-5 minutes
- Decompression time: 10-20 seconds

**Why xz?**
- Better compression than gzip (~30% better)
- Standard on Linux/macOS
- Available on Windows (via Git Bash, WSL)
- Widely supported

### Line Ending Handling:

**`.gitattributes` ensures:**
- Shell scripts: Always LF (required for bash)
- Python scripts: LF (works everywhere)
- Markdown: LF (git standard)
- Binary files: No normalization

**Result:**
- Scripts work on Linux/macOS/WSL/Git Bash
- Python works on all platforms
- No platform-specific issues

---

## Future Enhancements

### Easy to Add:
- More states (just run the script)
- Different versions (change version number)
- Custom documentation per state
- Regional variations

### Possible Additions:
- Automatic data updates (fetch latest from EPA)
- Multi-state comparison packages
- Regional packages (Pacific Northwest, Great Lakes, etc.)
- Subset packages (just temperature, just turbidity, etc.)

---

## Documentation

- **FOR_TEACHERS.md**: Detailed guide for creating packages
- **ADDING_STATES.md**: Technical details on data format
- **QUICK_REFERENCE.md**: One-page cheat sheet
- **README.md**: Project overview
- **This file**: Automation system overview

---

## Quick Reference

```bash
# Create new state package
./scripts/build_state_package.sh StateName ST 1.0

# Rebuild from compressed database
./build.sh statename 1.0

# Just download data
./scripts/download_state_data.sh StateName

# Just compress database
./scripts/compress_database.sh statename

# Test locally
make serve
# Then visit http://localhost:8000/
```

---

**Questions?** See [docs/FOR_TEACHERS.md](docs/FOR_TEACHERS.md) or check the scripts - they're well-commented!
