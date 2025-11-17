#!/usr/bin/env python3
"""
Parse EPA STORET water quality data for any state and generate CSV files.

This generalized parser supports data from any state following the EPA STORET format:
- Inventory files: {STATE}_{County}_inv.txt
- County subdirectories: {STATE}_{County}/
  - Station files: {STATE}_{County}_sta_*.txt
  - Results files: {STATE}_{County}_res_*.txt

Usage:
    python3 parse_state_data.py data/Washington -s WA -n Washington
    python3 parse_state_data.py data/Oregon -s OR -n Oregon
    python3 parse_state_data.py data/California -s CA -n California
    python3 parse_state_data.py data/Illinois -s IL -n Illinois

Output:
    Creates CSV files ready for SQLite import:
    - output/parameters.csv
    - output/stations.csv
    - output/results.csv
    - output/schema.sql (SQLite-compatible)
"""

import os
import sys
import re
import csv
import argparse
from pathlib import Path
from collections import defaultdict


class StateDataParser:
    """Parse EPA STORET water quality monitoring data for any state."""

    def __init__(self, data_dir, state_abbr='WA', state_name='Washington'):
        """
        Initialize parser for a specific state.

        Args:
            data_dir: Directory containing state data files
            state_abbr: Two-letter state abbreviation (e.g., 'WA', 'OR', 'CA', 'IL')
            state_name: Full state name (e.g., 'Washington', 'Oregon')
        """
        self.data_dir = Path(data_dir)
        self.state_abbr = state_abbr.upper()
        self.state_name = state_name
        self.counties = []
        self.stations = []
        self.parameters = []
        self.results = []

        print(f"Initializing parser for {state_name} ({state_abbr})")
        print(f"Data directory: {self.data_dir}")

    def parse_tab_delimited_file(self, filepath):
        """Parse a tab-delimited file and return headers and data rows."""
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"  Warning: Could not read {filepath}: {e}")
            return [], []

        if len(lines) < 2:
            return [], []

        # Find the header line (usually line 1, with separator line at 2)
        headers = [h.strip() for h in lines[0].split('\t')]

        # Skip the separator line (dashes) and parse data
        data_rows = []
        for line in lines[2:]:  # Skip header and separator
            if line.strip():
                row = [field.strip() for field in line.split('\t')]
                data_rows.append(row)

        return headers, data_rows

    def extract_county_name(self, filename):
        """Extract county name from filename like WA_Adams_inv.txt or OR_Multnomah_inv.txt."""
        # Match pattern: {STATE}_{County}_inv.txt
        pattern = f'{self.state_abbr}_(.+?)_inv\\.txt'
        match = re.match(pattern, filename, re.IGNORECASE)
        if match:
            return match.group(1).replace('_', ' ')
        return None

    def parse_inventory_files(self):
        """Parse all county inventory files to get parameter information."""
        print(f"\nParsing inventory files ({self.state_abbr}_*_inv.txt)...")
        param_dict = {}

        # Look for files matching {STATE}_*_inv.txt
        pattern = f'{self.state_abbr}_*_inv.txt'
        inv_files = list(self.data_dir.glob(pattern))
        print(f"  Found {len(inv_files)} inventory files matching {pattern}")

        if not inv_files:
            print(f"  Warning: No inventory files found matching {pattern}")
            return

        for inv_file in inv_files:
            county_name = self.extract_county_name(inv_file.name)
            if not county_name:
                continue

            headers, rows = self.parse_tab_delimited_file(inv_file)

            if not headers:
                continue

            for row in rows:
                if len(row) >= 3:
                    code = row[0].strip()
                    short_name = row[1].strip() if len(row) > 1 else ''
                    long_name = row[2].strip() if len(row) > 2 else ''

                    # Skip if code is empty or looks like a header
                    if not code or code == 'Code' or code.startswith('---'):
                        continue

                    if code not in param_dict:
                        param_dict[code] = {
                            'code': code,
                            'short_name': short_name,
                            'long_name': long_name
                        }

        self.parameters = list(param_dict.values())
        print(f"  ✓ Found {len(self.parameters)} unique parameters")

    def parse_station_files(self):
        """Parse all station files."""
        print(f"\nParsing station files ({self.state_abbr}_*/{self.state_abbr}_*_sta_*.txt)...")
        station_dict = {}

        # Look for files matching {STATE}_*/{STATE}_*_sta_*.txt
        pattern = f'{self.state_abbr}_*/{self.state_abbr}_*_sta_*.txt'
        sta_files = list(self.data_dir.glob(pattern))
        print(f"  Found {len(sta_files)} station files matching {pattern}")

        if not sta_files:
            print(f"  Warning: No station files found matching {pattern}")
            return

        for sta_file in sta_files:
            headers, rows = self.parse_tab_delimited_file(sta_file)

            if not headers:
                continue

            # Create a mapping of header names to indices
            header_map = {h: i for i, h in enumerate(headers)}

            for row in rows:
                if len(row) < 2:
                    continue

                station_id = row[header_map.get('Station', 1)].strip() if 'Station' in header_map else row[1].strip()

                if not station_id or station_id in station_dict:
                    continue

                station_data = {
                    'agency': row[header_map.get('Agency', 0)].strip() if 'Agency' in header_map and len(row) > header_map['Agency'] else '',
                    'station_id': station_id,
                    'station_name': row[header_map.get('Station Name', 2)].strip() if 'Station Name' in header_map and len(row) > header_map['Station Name'] else '',
                    'agency_name': row[header_map.get('Agency Name', 3)].strip() if 'Agency Name' in header_map and len(row) > header_map['Agency Name'] else '',
                    'state': self.state_name,  # Use provided state name
                    'county': row[header_map.get('County Name', 5)].strip() if 'County Name' in header_map and len(row) > header_map['County Name'] else '',
                    'latitude': row[header_map.get('Latitude', 6)].strip() if 'Latitude' in header_map and len(row) > header_map['Latitude'] else '',
                    'longitude': row[header_map.get('Longitude', 7)].strip() if 'Longitude' in header_map and len(row) > header_map['Longitude'] else '',
                    'huc': row[header_map.get('HUC', 8)].strip() if 'HUC' in header_map and len(row) > header_map['HUC'] else '',
                    'station_type': row[header_map.get('Station Type', -4)].strip() if 'Station Type' in header_map and len(row) > header_map['Station Type'] else '',
                    'description': row[-1].strip() if len(row) > 0 else ''
                }

                station_dict[station_id] = station_data

        self.stations = list(station_dict.values())
        print(f"  ✓ Found {len(self.stations)} unique stations")

    def parse_result_files(self):
        """Parse all result files."""
        print(f"\nParsing result files ({self.state_abbr}_*/{self.state_abbr}_*_res_*.txt)...")
        result_count = 0

        # Look for files matching {STATE}_*/{STATE}_*_res_*.txt
        pattern = f'{self.state_abbr}_*/{self.state_abbr}_*_res_*.txt'
        res_files = list(self.data_dir.glob(pattern))
        print(f"  Found {len(res_files)} result files matching {pattern}")

        if not res_files:
            print(f"  Warning: No result files found matching {pattern}")
            return

        for res_file in res_files:
            headers, rows = self.parse_tab_delimited_file(res_file)

            if not headers:
                continue

            # Create a mapping of header names to indices
            header_map = {h: i for i, h in enumerate(headers)}

            for row in rows:
                if len(row) < 10:
                    continue

                result_data = {
                    'agency': row[header_map.get('Agency', 0)].strip() if 'Agency' in header_map and len(row) > header_map['Agency'] else '',
                    'station_id': row[header_map.get('Station', 1)].strip() if 'Station' in header_map and len(row) > header_map['Station'] else '',
                    'param_code': row[header_map.get('Param', 11)].strip() if 'Param' in header_map and len(row) > header_map['Param'] else '',
                    'start_date': row[header_map.get('Start Date', 12)].strip() if 'Start Date' in header_map and len(row) > header_map['Start Date'] else '',
                    'start_time': row[header_map.get('Start Time', 13)].strip() if 'Start Time' in header_map and len(row) > header_map['Start Time'] else '',
                    'result_value': row[header_map.get('Result Value', 8)].strip() if 'Result Value' in header_map and len(row) > header_map['Result Value'] else '',
                    'huc': row[header_map.get('HUC', 10)].strip() if 'HUC' in header_map and len(row) > header_map['HUC'] else '',
                    'sample_depth': row[header_map.get('Sample Depth', 16)].strip() if 'Sample Depth' in header_map and len(row) > header_map['Sample Depth'] else '',
                }

                self.results.append(result_data)
                result_count += 1

                if result_count % 100000 == 0:
                    print(f"  Processed {result_count:,} results...")

        print(f"  ✓ Found {result_count:,} total results")

    def write_csv_files(self, output_dir='output'):
        """Write parsed data to CSV files for SQLite import."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)

        print(f"\nWriting CSV files to {output_path}/...")

        # Write parameters table
        param_file = output_path / 'parameters.csv'
        with open(param_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['code', 'short_name', 'long_name'])
            writer.writeheader()
            writer.writerows(self.parameters)
        print(f"  ✓ Wrote {len(self.parameters):,} parameters to parameters.csv")

        # Write stations table
        station_file = output_path / 'stations.csv'
        with open(station_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['agency', 'station_id', 'station_name', 'agency_name',
                         'state', 'county', 'latitude', 'longitude', 'huc',
                         'station_type', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.stations)
        print(f"  ✓ Wrote {len(self.stations):,} stations to stations.csv")

        # Write results table
        result_file = output_path / 'results.csv'
        with open(result_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['agency', 'station_id', 'param_code', 'start_date',
                         'start_time', 'result_value', 'huc', 'sample_depth']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)
        print(f"  ✓ Wrote {len(self.results):,} results to results.csv")

    def write_sqlite_schema(self, output_dir='output'):
        """Write SQLite schema file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)

        schema_file = output_path / 'schema.sql'

        schema_sql = f"""-- SQLite Schema for {self.state_name} Water Quality Data
-- Generated by parse_state_data.py

-- Drop existing tables if they exist
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS parameters;

-- Parameters table
CREATE TABLE parameters (
    code TEXT PRIMARY KEY,
    short_name TEXT,
    long_name TEXT
);

-- Stations table
CREATE TABLE stations (
    agency TEXT,
    station_id TEXT PRIMARY KEY,
    station_name TEXT,
    agency_name TEXT,
    state TEXT,
    county TEXT,
    latitude REAL,
    longitude REAL,
    huc TEXT,
    station_type TEXT,
    description TEXT
);

-- Results table
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agency TEXT,
    station_id TEXT,
    param_code TEXT,
    start_date TEXT,
    start_time TEXT,
    result_value TEXT,
    huc TEXT,
    sample_depth TEXT,
    FOREIGN KEY (station_id) REFERENCES stations(station_id),
    FOREIGN KEY (param_code) REFERENCES parameters(code)
);

-- Create indexes for better query performance
CREATE INDEX idx_results_station ON results(station_id);
CREATE INDEX idx_results_param ON results(param_code);
CREATE INDEX idx_results_date ON results(start_date);
CREATE INDEX idx_stations_county ON stations(county);
"""

        with open(schema_file, 'w', encoding='utf-8') as f:
            f.write(schema_sql)

        print(f"  ✓ Wrote SQLite schema to schema.sql")

    def write_import_script(self, output_dir='output', db_name=None):
        """Write shell script to import CSV data into SQLite."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)

        if db_name is None:
            db_name = f"{self.state_name.lower()}_water.db"

        import_file = output_path / 'import_to_sqlite.sh'

        import_script = f"""#!/bin/bash
# Import {self.state_name} water quality data into SQLite
# Generated by parse_state_data.py

set -e  # Exit on error

DB_FILE="../{db_name}"

echo "================================================================"
echo "Importing {self.state_name} Water Quality Data to SQLite"
echo "================================================================"

# Check if CSV files exist
if [ ! -f "parameters.csv" ] || [ ! -f "stations.csv" ] || [ ! -f "results.csv" ]; then
    echo "ERROR: CSV files not found. Run parse_state_data.py first."
    exit 1
fi

        # Check if database already exists
        if [ -f "$DB_FILE" ]; then
            echo "Database $DB_FILE already exists. Skipping import."
            exit 0
        fi

        # Create schemaecho ""
echo "[1/4] Creating database schema..."
sqlite3 "$DB_FILE" < schema.sql
echo "  ✓ Schema created"

# Import parameters
echo ""
echo "[2/4] Importing parameters..."
sqlite3 "$DB_FILE" <<'EOF'
.mode csv
.import --skip 1 parameters.csv parameters
EOF
COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM parameters;")
echo "  ✓ Imported $COUNT parameters"

# Import stations
echo ""
echo "[3/4] Importing stations..."
sqlite3 "$DB_FILE" <<'EOF'
.mode csv
.import --skip 1 stations.csv stations
EOF
COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM stations;")
echo "  ✓ Imported $COUNT stations"

# Import results (this may take a while)
echo ""
echo "[4/4] Importing results (this may take several minutes)..."
sqlite3 "$DB_FILE" <<'EOF'
.mode csv
CREATE TEMPORARY TABLE temp_results (
    agency TEXT,
    station_id TEXT,
    param_code TEXT,
    start_date TEXT,
    start_time TEXT,
    result_value TEXT,
    huc TEXT,
    sample_depth TEXT
);
.import --skip 1 results.csv temp_results
INSERT INTO results (agency, station_id, param_code, start_date, start_time, result_value, huc, sample_depth)
SELECT agency, station_id, param_code, start_date, start_time, result_value, huc, sample_depth FROM temp_results;
DROP TABLE temp_results;
EOF
COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM results;")
echo "  ✓ Imported $COUNT results"

# Verify indexes
echo ""
echo "Verifying indexes..."
sqlite3 "$DB_FILE" ".indexes" | grep -c "idx_" || echo "0"
echo "  ✓ Indexes created"

# Show database size
DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
echo ""
echo "================================================================"
echo "✓ Import complete!"
echo "================================================================"
echo "Database: $DB_FILE"
echo "Size: $DB_SIZE"
echo ""
echo "To test:"
echo "  sqlite3 $DB_FILE"
echo "  sqlite> SELECT COUNT(*) FROM results;"
echo "  sqlite> SELECT COUNT(*) FROM stations;"
echo "  sqlite> .quit"
echo ""
"""

        with open(import_file, 'w', encoding='utf-8') as f:
            f.write(import_script)

        # Make script executable
        import_file.chmod(0o755)

        print(f"  ✓ Wrote import script to import_to_sqlite.sh")

    def run(self, output_dir='output'):
        """Run the complete parsing process."""
        output_path = Path(output_dir)
        param_file = output_path / 'parameters.csv'
        station_file = output_path / 'stations.csv'
        result_file = output_path / 'results.csv'

        if param_file.exists() and station_file.exists() and result_file.exists():
            print(f"Output CSV files already exist in {output_dir}. Skipping parsing.")
            # Still write schema and import script, as they might be needed even if CSVs exist
            self.write_sqlite_schema(output_dir)
            self.write_import_script(output_dir)
            return

        print("=" * 70)
        print(f"EPA STORET Data Parser - {self.state_name}")
        print("=" * 70)

        self.parse_inventory_files()
        self.parse_station_files()
        self.parse_result_files()

        self.write_csv_files(output_dir)
        self.write_sqlite_schema(output_dir)
        self.write_import_script(output_dir)

        print("\n" + "=" * 70)
        print("✓ Parsing complete!")
        print("=" * 70)
        print(f"\nSummary:")
        print(f"  Parameters: {len(self.parameters):,}")
        print(f"  Stations:   {len(self.stations):,}")
        print(f"  Results:    {len(self.results):,}")
        print(f"\nNext steps:")
        print(f"  cd {output_dir}")
        print(f"  ./import_to_sqlite.sh")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Parse EPA STORET water quality data for any state',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Washington State
  python3 parse_state_data.py data/Washington -s WA -n Washington

  # Oregon
  python3 parse_state_data.py data/Oregon -s OR -n Oregon

  # California
  python3 parse_state_data.py data/California -s CA -n California

  # Illinois
  python3 parse_state_data.py data/Illinois -s IL -n Illinois

Output:
  Creates CSV files and import script in the output directory.
  Run the generated import_to_sqlite.sh script to create the database.
        """
    )

    parser.add_argument('data_dir',
                       help='Directory containing state data files')
    parser.add_argument('-s', '--state-abbr',
                       default='WA',
                       help='Two-letter state abbreviation (default: WA)')
    parser.add_argument('-n', '--state-name',
                       default='Washington',
                       help='Full state name (default: Washington)')
    parser.add_argument('-o', '--output',
                       default='output',
                       help='Output directory for CSV and SQL files (default: output)')

    args = parser.parse_args()

    # Validate data directory exists
    base_data_dir = Path(args.data_dir)
    actual_data_dir = base_data_dir / args.state_name.capitalize()

    if not actual_data_dir.exists():
        print(f"ERROR: Data directory not found: {actual_data_dir}")
        sys.exit(1)

    # Run parser
    state_parser = StateDataParser(actual_data_dir, args.state_abbr, args.state_name)
    state_parser.run(args.output)


if __name__ == '__main__':
    main()
