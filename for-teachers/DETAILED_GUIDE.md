# For Teachers: Creating State Packages

Want to create a water quality analysis package for your state? It's automated!

## Quick Start (One Command)

```bash
./scripts/build_state_package.sh YourState ST 1.0
```

**Example:**
```bash
./scripts/build_state_package.sh Oregon OR 1.0
```

This single command will:
1. Download EPA STORET data for your state (~500 MB)
2. Extract and parse the data
3. Create a SQLite database
4. Compress the database for version control
5. Build the student package (zip file)

**Time:** 10-30 minutes depending on state size and internet speed

---

## What Gets Created

### For Version Control (check into git):
- `build/oregon_water.db.xz` - Compressed database (~50-100 MB)
  - This is what you commit to git
  - Will be auto-decompressed during builds

### For Students (distribute):
- `dist/oregon_water_data_v1.0.zip` - Student package (~80 MB)
  - Contains everything students need
  - Ready to distribute immediately

---

## Step-by-Step (If You Want Details)

### 1. Download STORET Data

```bash
./scripts/download_state_data.sh Oregon
```

**What this does:**
- Downloads from: `https://gaftp.epa.gov/Storet/exports/Oregon.zip`
- Saves to: `data/storet/Oregon.zip`

**Available states:** Browse https://gaftp.epa.gov/Storet/exports/

### 2. Build the Package

```bash
./scripts/build_state_package.sh Oregon OR 1.0
```

**What this does:**
- Extracts STORET zip files
- Parses tab-delimited data to CSV
- Imports CSV to SQLite database
- Compresses database for git
- Creates student package

**Output:**
- `build/oregon_water.db.xz` (compressed, ~80 MB) ← Commit this
- `dist/oregon_water_data_v1.0.zip` (student package, ~80 MB) ← Share this

### 3. Test the Package

```bash
cd /tmp
unzip ~/path/to/dist/oregon_water_data_v1.0.zip
cd package
open index.html  # Or: xdg-open index.html
```

### 4. Commit to Repository (Optional)

```bash
git add build/oregon_water.db.xz
git commit -m "Add Oregon water quality database"
git push
```

**Why commit?**
- Other teachers can rebuild the package
- GitHub Actions will create releases automatically
- Students can download from GitHub releases

---

## Rebuilding Later

Once the compressed database is committed, anyone can rebuild:

```bash
./build.sh oregon 1.0
```

**This is fast** (< 1 minute) because:
- No downloading needed
- No parsing needed
- Just decompresses and bundles

---

## GitHub Actions (Automatic Releases)

When you push a compressed database to `main` branch:

1. GitHub Actions automatically builds student packages
2. Creates a new release with all state packages
3. Students can download directly from GitHub releases

**No manual work needed after initial setup!**

---

## Troubleshooting

### "State not found" when downloading

Check the state name matches exactly (case-sensitive):
- ✅ `Washington` (correct)
- ❌ `washington` (wrong)

Browse available states: https://gaftp.epa.gov/Storet/exports/

### Database too large for git

Use the compressed version (`.db.xz`):
- Washington: 371 MB → 78 MB compressed
- Illinois: ~similar compression ratio

Git handles ~100 MB files fine. For larger states, consider:
- Git LFS (Large File Storage)
- Hosting database separately and providing download link

### Build fails during parsing

Check the data format:
- Some states may have different file structures
- Parser expects standard EPA STORET format
- See `src/parse_state_data.py` for details

---

## Customization

### Change package version

```bash
./build.sh oregon 2.0  # Creates v2.0 package
```

### Customize documentation

Edit files in `src/templates/`:
- `README.md` - Main overview
- `QUICKSTART.md` - Quick start guide
- `SPATIAL_ANALYSIS.md` - Mapping tutorial

Changes apply to all states automatically.

### Add state-specific notes

Create `src/templates/STATE_NOTES.md`:
```markdown
# Oregon-Specific Information

- Focus on Columbia River watershed
- Includes coastal estuaries
- Data from 1960-2020
```

Then reference it in the documentation.

---

## Distribution Options

### Option 1: GitHub Releases (Recommended)
- Automatic via GitHub Actions
- Free hosting
- Version control
- Students get latest version

### Option 2: Direct Download
- Share the zip file directly
- Email, cloud storage, LMS
- No git needed

### Option 3: USB Drive
- For classrooms without reliable internet
- Copy zip file to drives
- Students extract locally

---

## Support

Questions? See:
- [ADDING_STATES.md](ADDING_STATES.md) - Detailed technical guide
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - One-page cheat sheet
- [README.md](../README.md) - Project overview

Or check the scripts themselves - they're well-commented!
