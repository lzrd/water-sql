#!/bin/bash
# Compress SQLite database for version control
# Usage: ./scripts/compress_database.sh <state>
# Example: ./scripts/compress_database.sh washington

set -e

STATE="${1:-washington}"
DB_FILE="build/${STATE}_water.db"
COMPRESSED_FILE="build/${STATE}_water.db.xz"

if [ -f "$COMPRESSED_FILE" ]; then
    echo "Compressed database $COMPRESSED_FILE already exists. Skipping compression."
    exit 0
fi

if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database not found: $DB_FILE"
    echo "Run the parser first to create the database."
    exit 1
fi

echo "========================================"
echo "Compressing database for version control"
echo "========================================"
echo "Input:  $DB_FILE"
echo "Output: $COMPRESSED_FILE"
echo ""

# Get original size
ORIGINAL_SIZE=$(stat -c %s "$DB_FILE" 2>/dev/null || stat -f %z "$DB_FILE" 2>/dev/null)
ORIGINAL_MB=$((ORIGINAL_SIZE / 1024 / 1024))

echo "Original size: ${ORIGINAL_MB} MB"
echo "Compressing with xz (maximum compression)..."
echo ""

# Compress with maximum compression
# -9: maximum compression
# -e: extreme mode (slower but better compression)
# -k: keep original file
# -f: force overwrite
xz -9 -e -k -f "$DB_FILE"

if [ $? -eq 0 ]; then
    COMPRESSED_SIZE=$(stat -c %s "$COMPRESSED_FILE" 2>/dev/null || stat -f %z "$COMPRESSED_FILE" 2>/dev/null)
    COMPRESSED_MB=$((COMPRESSED_SIZE / 1024 / 1024))
    RATIO=$((100 - (COMPRESSED_SIZE * 100 / ORIGINAL_SIZE)))

    echo "✓ Compression complete!"
    echo "  Original:   ${ORIGINAL_MB} MB"
    echo "  Compressed: ${COMPRESSED_MB} MB"
    echo "  Saved:      ${RATIO}% reduction"
    echo ""
    echo "File ready to commit: $COMPRESSED_FILE"
    echo ""
    echo "To decompress later:"
    echo "  xz -d -k $COMPRESSED_FILE"
else
    echo "✗ Compression failed!"
    exit 1
fi
