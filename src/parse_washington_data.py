#!/usr/bin/env python3
"""
Parse Washington State water quality data and generate PostgreSQL-compatible CSV files.

Data structure:
- Washington/ directory contains:
  - County inventory files: WA_{County}_inv.txt
  - County subdirectories: WA_{County}/
    - Station files: WA_{County}_sta_*.txt
    - Results files: WA_{County}_res_*.txt
  - Matrix file: Washington__matrix.txt

This script creates normalized CSV files for PostgreSQL import.
"""

import os
import sys
import re
import csv
from pathlib import Path
from collections import defaultdict


class WashingtonDataParser:
    """Parse Washington State water quality monitoring data."""

    def __init__(self, data_dir='Washington'):
        self.data_dir = Path(data_dir)
        self.counties = []
        self.stations = []
        self.parameters = []
        self.results = []

    def parse_tab_delimited_file(self, filepath):
        """Parse a tab-delimited file and return headers and data rows."""
        with open(filepath, 'r', encoding='latin-1') as f:
            lines = f.readlines()

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
        """Extract county name from filename like WA_Adams_inv.txt."""
        match = re.match(r'WA_(.+?)_inv\.txt', filename)
        if match:
            return match.group(1).replace('_', ' ')
        return None

    def parse_inventory_files(self):
        """Parse all county inventory files to get parameter information."""
        print("Parsing inventory files...")
        param_dict = {}

        for inv_file in self.data_dir.glob('WA_*_inv.txt'):
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
        print(f"  Found {len(self.parameters)} unique parameters")

    def parse_station_files(self):
        """Parse all station files."""
        print("Parsing station files...")
        station_dict = {}

        for sta_file in self.data_dir.glob('WA_*/WA_*_sta_*.txt'):
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
                    'state': row[header_map.get('State Name', 4)].strip() if 'State Name' in header_map and len(row) > header_map['State Name'] else 'Washington',
                    'county': row[header_map.get('County Name', 5)].strip() if 'County Name' in header_map and len(row) > header_map['County Name'] else '',
                    'latitude': row[header_map.get('Latitude', 6)].strip() if 'Latitude' in header_map and len(row) > header_map['Latitude'] else '',
                    'longitude': row[header_map.get('Longitude', 7)].strip() if 'Longitude' in header_map and len(row) > header_map['Longitude'] else '',
                    'huc': row[header_map.get('HUC', 8)].strip() if 'HUC' in header_map and len(row) > header_map['HUC'] else '',
                    'station_type': row[header_map.get('Station Type', -4)].strip() if 'Station Type' in header_map and len(row) > header_map['Station Type'] else '',
                    'description': row[-1].strip() if len(row) > 0 else ''
                }

                station_dict[station_id] = station_data

        self.stations = list(station_dict.values())
        print(f"  Found {len(self.stations)} unique stations")

    def parse_result_files(self):
        """Parse all result files."""
        print("Parsing result files...")
        result_count = 0

        for res_file in self.data_dir.glob('WA_*/WA_*_res_*.txt'):
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

                if result_count % 10000 == 0:
                    print(f"  Processed {result_count} results...")

        print(f"  Found {result_count} total results")

    def write_csv_files(self, output_dir='output'):
        """Write parsed data to CSV files for PostgreSQL import."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\nWriting CSV files...")

        # Write parameters table
        param_file = output_path / 'parameters.csv'
        with open(param_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['code', 'short_name', 'long_name'])
            writer.writeheader()
            writer.writerows(self.parameters)
        print(f"  Wrote {len(self.parameters)} parameters to {param_file}")

        # Write stations table
        station_file = output_path / 'stations.csv'
        with open(station_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['agency', 'station_id', 'station_name', 'agency_name',
                         'state', 'county', 'latitude', 'longitude', 'huc',
                         'station_type', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.stations)
        print(f"  Wrote {len(self.stations)} stations to {station_file}")

        # Write results table
        result_file = output_path / 'results.csv'
        with open(result_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['agency', 'station_id', 'param_code', 'start_date',
                         'start_time', 'result_value', 'huc', 'sample_depth']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)
        print(f"  Wrote {len(self.results)} results to {result_file}")

    def write_sql_schema(self, output_dir='output'):
        """Write PostgreSQL schema file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        schema_file = output_path / 'schema.sql'

        schema_sql = """-- PostgreSQL Schema for Washington State Water Quality Data
-- Generated by parse_washington_data.py

-- Drop existing tables if they exist
DROP TABLE IF EXISTS results CASCADE;
DROP TABLE IF EXISTS stations CASCADE;
DROP TABLE IF EXISTS parameters CASCADE;

-- Parameters table
CREATE TABLE parameters (
    code VARCHAR(10) PRIMARY KEY,
    short_name VARCHAR(50),
    long_name VARCHAR(255)
);

-- Stations table
CREATE TABLE stations (
    station_id VARCHAR(50) PRIMARY KEY,
    agency VARCHAR(50),
    station_name TEXT,
    agency_name VARCHAR(100),
    state VARCHAR(50),
    county VARCHAR(50),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    huc VARCHAR(20),
    station_type VARCHAR(100),
    description TEXT
);

-- Results table
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    agency VARCHAR(50),
    station_id VARCHAR(50) REFERENCES stations(station_id),
    param_code VARCHAR(10) REFERENCES parameters(code),
    start_date DATE,
    start_time TIME,
    result_value VARCHAR(50),
    huc VARCHAR(20),
    sample_depth VARCHAR(20)
);

-- Create indexes for better query performance
CREATE INDEX idx_results_station ON results(station_id);
CREATE INDEX idx_results_param ON results(param_code);
CREATE INDEX idx_results_date ON results(start_date);
CREATE INDEX idx_stations_county ON stations(county);

-- Import commands (run these after creating the schema)
-- \\COPY parameters FROM 'parameters.csv' WITH (FORMAT CSV, HEADER true);
-- \\COPY stations FROM 'stations.csv' WITH (FORMAT CSV, HEADER true);
-- \\COPY results FROM 'results.csv' WITH (FORMAT CSV, HEADER true);
"""

        with open(schema_file, 'w') as f:
            f.write(schema_sql)

        print(f"  Wrote SQL schema to {schema_file}")

    def write_import_script(self, output_dir='output'):
        """Write a shell script to import data into PostgreSQL."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        import_script = output_path / 'import_data.sh'

        script_content = """#!/bin/bash
# Import Washington State water quality data into PostgreSQL
# Usage: ./import_data.sh [database_name] [username]

DB_NAME="${1:-washington_water}"
DB_USER="${2:-$USER}"

echo "Importing data into database: $DB_NAME"
echo "Using PostgreSQL user: $DB_USER"
echo ""

# Create database if it doesn't exist
echo "Creating database (if it doesn't exist)..."
createdb -U "$DB_USER" "$DB_NAME" 2>/dev/null || echo "Database already exists"

# Create schema
echo "Creating schema..."
psql -U "$DB_USER" -d "$DB_NAME" -f schema.sql

# Import data
echo "Importing parameters..."
psql -U "$DB_USER" -d "$DB_NAME" -c "\\COPY parameters FROM 'parameters.csv' WITH (FORMAT CSV, HEADER true);"

echo "Importing stations..."
psql -U "$DB_USER" -d "$DB_NAME" -c "\\COPY stations FROM 'stations.csv' WITH (FORMAT CSV, HEADER true);"

echo "Importing results (this may take a while)..."
psql -U "$DB_USER" -d "$DB_NAME" -c "\\COPY results FROM 'results.csv' WITH (FORMAT CSV, HEADER true);"

echo ""
echo "Import complete!"
echo ""
echo "To connect to the database:"
echo "  psql -U $DB_USER -d $DB_NAME"
"""

        with open(import_script, 'w') as f:
            f.write(script_content)

        # Make script executable
        os.chmod(import_script, 0o755)

        print(f"  Wrote import script to {import_script}")

    def parse_all(self):
        """Parse all data files."""
        self.parse_inventory_files()
        self.parse_station_files()
        self.parse_result_files()

    def generate_output(self, output_dir='output'):
        """Generate all output files."""
        self.write_csv_files(output_dir)
        self.write_sql_schema(output_dir)
        self.write_import_script(output_dir)


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Parse Washington State water quality data for PostgreSQL import'
    )
    parser.add_argument(
        'data_dir',
        nargs='?',
        default='Washington',
        help='Directory containing Washington data files (default: Washington)'
    )
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='Output directory for CSV and SQL files (default: output)'
    )

    args = parser.parse_args()

    # Check if data directory exists
    if not Path(args.data_dir).exists():
        print(f"Error: Data directory '{args.data_dir}' not found")
        sys.exit(1)

    print("="*60)
    print("Washington State Water Quality Data Parser")
    print("="*60)
    print(f"Data directory: {args.data_dir}")
    print(f"Output directory: {args.output}")
    print("")

    # Parse data
    parser = WashingtonDataParser(args.data_dir)
    parser.parse_all()

    # Generate output files
    print("")
    parser.generate_output(args.output)

    print("")
    print("="*60)
    print("Parsing complete!")
    print("="*60)
    print("")
    print("To import data into PostgreSQL:")
    print(f"  cd {args.output}")
    print("  ./import_data.sh [database_name] [username]")
    print("")


if __name__ == '__main__':
    main()
