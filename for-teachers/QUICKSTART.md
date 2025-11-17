# Quick Start for Teachers

## Create a Water Quality Package for Your State

### One Command:

```bash
./scripts/build_state_package.sh YourState ST 1.0
```

**Examples:**
```bash
./scripts/build_state_package.sh Oregon OR 1.0
./scripts/build_state_package.sh California CA 1.0
./scripts/build_state_package.sh Texas TX 1.0
```

**What happens:**
1. Downloads EPA STORET data
2. Parses and creates SQLite database
3. Compresses database for version control
4. Creates student package (zip file)

**Time:** 10-30 minutes

**Output:**
- `build/oregon_water.db.xz` - Compressed database (commit to git)
- `dist/oregon_water_data_v1.0.zip` - Student package (distribute)

---

## Test the Package

```bash
cd /tmp
unzip ~/path/to/dist/oregon_water_data_v1.0.zip
cd package
open index.html  # Or: xdg-open index.html on Linux
```

---

## Share with Students

### Option 1: Direct Distribution
Share the zip file via email, cloud storage, or LMS.

### Option 2: GitHub Releases (Automatic)
1. Commit the compressed database:
   ```bash
   git add build/oregon_water.db.xz
   git commit -m "Add Oregon database"
   git push
   ```
2. GitHub Actions automatically creates a release
3. Students download from: `https://github.com/yourname/water-sql/releases/latest`

---

## Available States

Browse available states at: https://gaftp.epa.gov/Storet/exports/

Common states:
- Washington, Oregon, California
- Texas, Illinois, Florida
- New York, Pennsylvania, Ohio
- And all other U.S. states!

---

## Need More Details?

See **`docs/FOR_TEACHERS.md`** for:
- Troubleshooting
- Customization
- GitHub Actions setup
- Technical details

---

## Already Have a Compressed Database?

If someone already created the `.db.xz` file, you can rebuild in < 1 minute:

```bash
./build.sh oregon 1.0
```

The database will auto-decompress and bundle into the student package.
