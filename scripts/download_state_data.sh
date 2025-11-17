#!/bin/bash
# Download EPA STORET data for a state
# Usage: ./scripts/download_state_data.sh <STATE_NAME>
# Example: ./scripts/download_state_data.sh Washington

set -e  # Exit on error

STATE_NAME="$1"

if [ -z "$STATE_NAME" ]; then
    echo "Usage: $0 <STATE_NAME>"
    echo "Example: $0 Washington"
    echo ""
    echo "Available states can be found at:"
    echo "https://gaftp.epa.gov/Storet/exports/"
    exit 1
fi

# Create data directory
mkdir -p data/storet

# Download the state data
EPA_URL="https://gaftp.epa.gov/Storet/exports/${STATE_NAME}.zip"
OUTPUT_FILE="data/storet/${STATE_NAME}.zip"

echo "========================================"
echo "Downloading EPA STORET data for ${STATE_NAME}"
echo "========================================"
echo "URL: ${EPA_URL}"
echo "Output: ${OUTPUT_FILE}"
echo ""

if [ -f "$OUTPUT_FILE" ]; then
    echo "⚠️  File already exists: ${OUTPUT_FILE}"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Download cancelled."
        exit 0
    fi
    rm "$OUTPUT_FILE"
fi

# Download with curl
curl -f -L -o "$OUTPUT_FILE" "$EPA_URL"

if [ $? -eq 0 ]; then
    SIZE=$(stat -c %s "$OUTPUT_FILE" 2>/dev/null || stat -f %z "$OUTPUT_FILE" 2>/dev/null || echo "unknown")
    SIZE_MB=$((SIZE / 1024 / 1024))
    echo ""
    echo "✓ Download complete!"
    echo "  File: ${OUTPUT_FILE}"
    echo "  Size: ${SIZE_MB} MB"
    echo ""
    echo "Next steps:"
    echo "  1. Extract the data: unzip ${OUTPUT_FILE} -d data/${STATE_NAME}"
    echo "  2. Build the package: ./scripts/build_state_package.sh ${STATE_NAME}"
else
    echo ""
    echo "✗ Download failed!"
    echo "  Check if '${STATE_NAME}' is a valid state name."
    echo "  Browse available states at: https://gaftp.epa.gov/Storet/exports/"
    exit 1
fi
