#!/bin/bash
# Complete build script for Water Quality Student Package
# Usage: ./build.sh [state] [version]

set -e  # Exit on error

STATE="${1:-washington}"
DEFAULT_VERSION=$(cat VERSION.txt)
VERSION="${2:-${DEFAULT_VERSION}}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Append Git short hash for PR builds
if [[ -n "$GITHUB_REF" && "$GITHUB_REF" == "refs/pull/"* ]]; then
    SHORT_SHA=$(echo "$GITHUB_SHA" | cut -c1-7)
    VERSION="${VERSION}-$$SHORT_SHA"
fi

echo "======================================================================="
echo "Building Water Quality Student Package"
echo "======================================================================="
echo "State: $STATE"
echo "Version: $VERSION"
echo "Build: $TIMESTAMP"
echo ""

# Step 1: Clean
echo "[1/9] Cleaning previous build..."
rm -rf build/package
mkdir -p build/package dist
echo "  ✓ Build directory cleaned"

# Step 2: Database
echo "[2/9] Preparing SQLite database..."

# Check if we need to decompress
if [ ! -f "build/${STATE}_water.db" ]; then
    if [ -f "build/${STATE}_water.db.xz" ]; then
        echo "  → Decompressing database..."
        ./scripts/decompress_database.sh "${STATE}"
    else
        echo "  ✗ ERROR: Database not found: build/${STATE}_water.db"
        echo "  → Run parser first or decompress: ./scripts/decompress_database.sh ${STATE}"
        exit 1
    fi
fi

cp "build/${STATE}_water.db" "build/package/${STATE}_water.db"
DB_SIZE=$(stat -c %s "build/package/${STATE}_water.db" | numfmt --to=iec-i --suffix=B)
echo "  ✓ Database: $DB_SIZE"

# Step 3: SQL.js (SKIPPED - browser console removed in v1.3)
echo "[3/9] Skipping SQL.js library (not needed without browser console)..."
echo "  ✓ Skipped"

# Step 4: Copy student documentation
echo "[4/9] Copying student documentation..."
if [ ! -f "for-students/README.md" ]; then
    echo "  ✗ ERROR: Student documentation not found in for-students/"
    echo "  → Check repository structure"
    exit 1
fi
cp for-students/README.md build/package/
cp for-students/INSTALL.md build/package/
cp for-students/QUICKSTART.md build/package/
cp for-students/INTERVIEW_PREP.md build/package/
cp for-students/SPATIAL_ANALYSIS.md build/package/
cp for-students/WATER_DATA.md build/package/
cp for-students/TIME_CODES.md build/package/
cp for-students/BROWSER_CONSOLE.md build/package/
cp for-students/example_queries.sql build/package/
# Copy index.html and sample.sqliterc from src/templates (build-specific files)
if [ -f "src/templates/index.html" ]; then
    cp src/templates/index.html build/package/
    sed -i "s|<!-- VERSION_PLACEHOLDER -->|${VERSION}|g" build/package/index.html
fi
if [ -f "src/templates/sample.sqliterc" ]; then
    cp src/templates/sample.sqliterc build/package/
fi
echo "  ✓ Student documentation copied"

# Step 5: Convert to HTML
echo "[5/9] Converting documentation to HTML..."
if [ ! -f "src/convert_md_to_html.py" ]; then
    echo "  ✗ WARNING: Converter not found, skipping HTML conversion"
else
    # Convert each markdown file in build/package/
    cd build/package
    python3 ../../src/convert_md_to_html.py README.md 2>/dev/null || echo "  ⚠ README.md conversion failed"
    python3 ../../src/convert_md_to_html.py INSTALL.md 2>/dev/null || echo "  ⚠ INSTALL.md conversion failed"
    python3 ../../src/convert_md_to_html.py QUICKSTART.md 2>/dev/null || echo "  ⚠ QUICKSTART.md conversion failed"
    python3 ../../src/convert_md_to_html.py INTERVIEW_PREP.md 2>/dev/null || echo "  ⚠ INTERVIEW_PREP.md conversion failed"
    python3 ../../src/convert_md_to_html.py SPATIAL_ANALYSIS.md 2>/dev/null || echo "  ⚠ SPATIAL_ANALYSIS.md conversion failed"
    python3 ../../src/convert_md_to_html.py WATER_DATA.md 2>/dev/null || echo "  ⚠ WATER_DATA.md conversion failed"
    python3 ../../src/convert_md_to_html.py TIME_CODES.md 2>/dev/null || echo "  ⚠ TIME_CODES.md conversion failed"
    python3 ../../src/convert_md_to_html.py BROWSER_CONSOLE.md 2>/dev/null || echo "  ⚠ BROWSER_CONSOLE.md conversion failed"
    cd ../..
    echo "  ✓ Documentation converted to HTML"
fi

# Step 6: Python scripts
echo "[6/9] Copying Python scripts..."
if [ ! -d "src/Python_Scripts" ]; then
    echo "  ✗ ERROR: Python scripts not found in src/Python_Scripts/"
    exit 1
fi
cp -r src/Python_Scripts build/package/
echo "  ✓ Python scripts copied"

# Step 7: Sample output
echo "[7/9] Generating sample visualizations..."
cd build/package/Python_Scripts
if python3 analyze_water_quality_sqlite.py > /dev/null 2>&1; then
    mkdir -p ../Sample_Output
    mv ./*.png ../Sample_Output/ 2>/dev/null || true
    NUM_IMAGES=$(find ../Sample_Output/ -name "*.png" -type f 2>/dev/null | wc -l)
    echo "  ✓ Sample output generated ($NUM_IMAGES images)"
else
    echo "  ⚠ WARNING: Could not generate sample output (non-critical)"
fi
cd ../../..

# Step 8: MANIFEST
echo "[8/9] Creating MANIFEST..."
cat > build/package/MANIFEST.txt <<EOF
Water Quality Data - Student Package
====================================

Version: $VERSION
State: ${STATE^}
Built: $(date +"%Y-%m-%d %H:%M:%S")
Build ID: $TIMESTAMP

Package Contents:
-----------------

Root Level:
  - ${STATE}_water.db (SQLite database, 371 MB)
  - index.html (landing page - start here!)
  - README.md / README.html
  - QUICKSTART.md / QUICKSTART.html (15-minute quick start)
  - INSTALL.md / INSTALL.html (detailed setup)
  - INTERVIEW_PREP.md / INTERVIEW_PREP.html (interview practice)
  - sample.sqliterc (save as ~/.sqliterc for automatic formatting)
  - example_queries.sql (load with: .read example_queries.sql)
  - MANIFEST.txt (this file)

Documentation/:
  - WATER_DATA.md / WATER_DATA.html (SQL tutorial)
  - TIME_CODES.md / TIME_CODES.html (Time code reference)

Python_Scripts/:
  - requirements.txt
  - analyze_water_quality_sqlite.py (basic analysis)
  - analyze_water_quality_annotated.py (educational, 600+ lines of comments)
  - analyze_water_quality_dual.py (PostgreSQL or SQLite comparison)

Sample_Output/:
  - *.png (sample visualizations)

Quick Start:
-----------
1. Extract: unzip <filename>
2. Open QUICKSTART.html in your browser (15-minute guide)
3. Or: Open README.html for overview
4. Install Python packages: pip install -r Python_Scripts/requirements.txt
5. Run analysis: python3 Python_Scripts/analyze_water_quality_sqlite.py

For full documentation, open README.html in a web browser.

Note: Browser console removed in v1.3 due to slow loading (>2 minutes).
      Use Python scripts for fast, interactive analysis instead.
EOF
echo "  ✓ MANIFEST created"

# Step 9: Archive
echo "[9/9] Creating distribution archive..."
cd build
ARCHIVE_NAME="${STATE}_water_data_v${VERSION}.zip"
zip -q -r "$ARCHIVE_NAME" package/
mv "$ARCHIVE_NAME" ../dist/
cd ..

FINAL_SIZE=$(stat -c %s "dist/$ARCHIVE_NAME" | numfmt --to=iec-i --suffix=B)
FILE_COUNT=$(unzip -l "dist/$ARCHIVE_NAME" | tail -1 | awk '{print $2}')

echo "  ✓ Archive created"
echo ""
echo "======================================================================="
echo "✅ BUILD COMPLETE"
echo "======================================================================="
echo "Package: dist/$ARCHIVE_NAME"
echo "Size: $FINAL_SIZE"
echo "Files: $FILE_COUNT"
echo ""
echo "Distribution file ready!"
echo ""
