#!/bin/bash
# Decompress SQLite database before building
# Usage: ./scripts/decompress_database.sh <state>
# Example: ./scripts/decompress_database.sh washington

set -e

STATE="${1:-washington}"
COMPRESSED_FILE="build/${STATE}_water.db.xz"
DB_FILE="build/${STATE}_water.db"

if [ ! -f "$COMPRESSED_FILE" ]; then
    echo "Error: Compressed database not found: $COMPRESSED_FILE"
    echo "Looking for existing database..."

    if [ -f "$DB_FILE" ]; then
        echo "✓ Uncompressed database already exists: $DB_FILE"
        exit 0
    fi

    echo "✗ No database found (compressed or uncompressed)"
    echo "Run the parser first: ./scripts/build_state_package.sh $STATE"
    exit 1
fi

echo "========================================"
echo "Decompressing database"
echo "========================================"
echo "Input:  $COMPRESSED_FILE"
echo "Output: $DB_FILE"
echo ""

# Check if already decompressed
if [ -f "$DB_FILE" ]; then
    echo "⚠️  Database already exists: $DB_FILE"

    # Check if it's newer than compressed version
    if [ "$DB_FILE" -nt "$COMPRESSED_FILE" ]; then
        echo "✓ Existing database is newer than compressed version, using it."
        exit 0
    fi

    read -p "Overwrite with decompressed version? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Using existing database."
        exit 0
    fi
    rm "$DB_FILE"
fi

# Get compressed size
COMPRESSED_SIZE=$(stat -c %s "$COMPRESSED_FILE" 2>/dev/null || stat -f %z "$COMPRESSED_FILE" 2>/dev/null)
COMPRESSED_MB=$((COMPRESSED_SIZE / 1024 / 1024))

echo "Compressed size: ${COMPRESSED_MB} MB"
echo "Decompressing..."
echo ""

# Decompress
# -d: decompress
# -k: keep compressed file
# -f: force overwrite
xz -d -k -f "$COMPRESSED_FILE"

if [ $? -eq 0 ]; then
    DECOMPRESSED_SIZE=$(stat -c %s "$DB_FILE" 2>/dev/null || stat -f %z "$DB_FILE" 2>/dev/null)
    DECOMPRESSED_MB=$((DECOMPRESSED_SIZE / 1024 / 1024))

    echo "✓ Decompression complete!"
    echo "  Compressed:   ${COMPRESSED_MB} MB"
    echo "  Decompressed: ${DECOMPRESSED_MB} MB"
    echo ""
    echo "Database ready: $DB_FILE"
else
    echo "✗ Decompression failed!"
    exit 1
fi
