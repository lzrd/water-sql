#!/bin/bash
# Complete build process for a state package from scratch
# Usage: ./scripts/build_state_package.sh <state> [state_abbr] [version]
# Example: ./scripts/build_state_package.sh Washington WA 1.0
# Example: ./scripts/build_state_package.sh Illinois IL 1.0

set -e

STATE_NAME="${1}"
STATE_ABBR="${2:-$(echo $1 | cut -c1-2 | tr '[:lower:]' '[:upper:]')}"
VERSION="${3:-1.0}"

if [ -z "$STATE_NAME" ]; then
    echo "Usage: $0 <STATE_NAME> [STATE_ABBR] [VERSION]"
    echo ""
    echo "Examples:"
    echo "  $0 Washington WA 1.0"
    echo "  $0 Illinois IL 1.0"
    echo "  $0 Oregon OR 1.0"
    echo ""
    exit 1
fi

STATE_LOWER=$(echo "$STATE_NAME" | tr '[:upper:]' '[:lower:]')
STORET_ZIP="data/storet/${STATE_NAME}.zip"
EXTRACT_DIR="data/${STATE_NAME}"
OUTPUT_DIR="build/output_${STATE_LOWER}"
DB_FILE="build/${STATE_LOWER}_water.db"
COMPRESSED_DB="${DB_FILE}.xz"

echo "======================================================================="
echo "Building Complete Package for ${STATE_NAME}"
echo "======================================================================="
echo "State Name: ${STATE_NAME}"
echo "State Abbr: ${STATE_ABBR}"
echo "Version:    ${VERSION}"
echo "Output DB:  ${DB_FILE}"
echo ""

# Step 1: Check if STORET data exists, download if needed
if [ ! -f "$STORET_ZIP" ]; then
    echo "[1/6] Downloading STORET data..."
    ./scripts/download_state_data.sh "${STATE_NAME}"
else
    echo "[1/6] STORET data already downloaded"
    echo "  ✓ Found: ${STORET_ZIP}"
fi

# Step 2: Extract if needed
if [ ! -d "$EXTRACT_DIR" ]; then
    echo ""
    echo "[2/6] Extracting STORET data..."
    mkdir -p "$EXTRACT_DIR"
    unzip -q "$STORET_ZIP" -d "$EXTRACT_DIR"
    echo "  ✓ Extracted to: ${EXTRACT_DIR}"
else
    echo ""
    echo "[2/6] STORET data already extracted"
    echo "  ✓ Directory: ${EXTRACT_DIR}"
fi

# Step 3: Parse to CSV
echo ""
echo "[3/6] Parsing STORET data to CSV..."
python3 src/parse_state_data.py \
    "$EXTRACT_DIR" \
    -s "${STATE_ABBR}" \
    -n "${STATE_NAME}" \
    -o "$OUTPUT_DIR"

if [ $? -ne 0 ]; then
    echo "  ✗ Parser failed!"
    exit 1
fi
echo "  ✓ CSV files created in: ${OUTPUT_DIR}"

# Step 4: Import to SQLite
echo ""
echo "[4/6] Importing CSV to SQLite..."
cd "$OUTPUT_DIR"
./import_to_sqlite.sh
cd ../..

if [ ! -f "${OUTPUT_DIR}/${STATE_LOWER}_water.db" ]; then
    echo "  ✗ Database creation failed!"
    exit 1
fi

# Move database to build directory
mv "${OUTPUT_DIR}/${STATE_LOWER}_water.db" "$DB_FILE"
echo "  ✓ Database created: ${DB_FILE}"

# Get database stats
DB_SIZE_MB=$(stat -c %s "$DB_FILE" 2>/dev/null | awk '{print int($1/1024/1024)}' || stat -f %z "$DB_FILE" 2>/dev/null | awk '{print int($1/1024/1024)}')
STATION_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM stations;")
RESULT_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM results;")

echo "  Database stats:"
echo "    Size:     ${DB_SIZE_MB} MB"
echo "    Stations: ${STATION_COUNT}"
echo "    Results:  ${RESULT_COUNT}"

# Step 5: Compress database for version control
echo ""
echo "[5/6] Compressing database for git..."
./scripts/compress_database.sh "${STATE_LOWER}"

# Step 6: Build final package
echo ""
echo "[6/6] Building student package..."
./build.sh "${STATE_LOWER}" "${VERSION}"

echo ""
echo "======================================================================="
echo "✅ BUILD COMPLETE"
echo "======================================================================="
echo "Compressed DB (commit this): ${COMPRESSED_DB}"
echo "Student package:             dist/${STATE_LOWER}_water_data_v${VERSION}.zip"
echo ""
echo "Next steps:"
echo "  1. Test the package:"
echo "     cd /tmp && unzip ~/path/to/dist/${STATE_LOWER}_water_data_v${VERSION}.zip"
echo ""
echo "  2. Commit the compressed database:"
echo "     git add ${COMPRESSED_DB}"
echo "     git commit -m 'Add ${STATE_NAME} water quality database'"
echo ""
echo "  3. To rebuild later, just run:"
echo "     ./build.sh ${STATE_LOWER} ${VERSION}"
echo "     (The compressed database will be auto-decompressed)"
echo ""
