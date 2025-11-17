#!/usr/bin/env python3
"""
Export Washington State Water Quality Data from PostgreSQL to SQLite

This script creates a portable SQLite database file that students can use
without needing to set up a PostgreSQL server.

Usage:
    python3 export_to_sqlite.py

Output:
    washington_water.db - SQLite database file (~200-300MB)
"""

import psycopg2
import sqlite3
import sys

# PostgreSQL connection
PG_CONFIG = {
    'host': 'moneta.lan',
    'port': 5432,
    'database': 'washington_water',
    'user': 'water'
}

SQLITE_DB = 'washington_water.db'

def create_sqlite_schema(sqlite_conn):
    """Create tables in SQLite database."""
    cursor = sqlite_conn.cursor()

    print("Creating SQLite schema...")

    # Parameters table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parameters (
            code TEXT PRIMARY KEY,
            short_name TEXT,
            long_name TEXT
        )
    """)

    # Stations table (note: agency and station_id order matches CSV)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stations (
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
        )
    """)

    # Results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
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
        )
    """)

    # Create indexes
    print("Creating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_station ON results(station_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_param ON results(param_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_date ON results(start_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stations_county ON stations(county)")

    sqlite_conn.commit()
    print("✓ Schema created")


def copy_table(pg_conn, sqlite_conn, table_name, columns, insert_columns=None, batch_size=10000):
    """Copy data from PostgreSQL to SQLite."""
    pg_cursor = pg_conn.cursor()
    sqlite_cursor = sqlite_conn.cursor()

    # Get total count
    pg_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total = pg_cursor.fetchone()[0]
    print(f"\nCopying {table_name}: {total:,} rows")

    # Fetch and insert in batches
    pg_cursor.execute(f"SELECT {columns} FROM {table_name}")

    # Use insert_columns if provided (for tables with auto-increment)
    if insert_columns is None:
        insert_columns = ""
        placeholders = ','.join(['?' for _ in columns.split(',')])
    else:
        insert_columns = f"({insert_columns})"
        placeholders = ','.join(['?' for _ in insert_columns.split(',')])

    insert_sql = f"INSERT INTO {table_name} {insert_columns} VALUES ({placeholders})"

    copied = 0
    batch = []

    for row in pg_cursor:
        # Convert decimal.Decimal to float for SQLite compatibility
        converted_row = []
        for val in row:
            if val is not None and hasattr(val, '__float__'):
                try:
                    converted_row.append(float(val))
                except:
                    converted_row.append(val)
            else:
                converted_row.append(val)
        batch.append(tuple(converted_row))

        if len(batch) >= batch_size:
            sqlite_cursor.executemany(insert_sql, batch)
            sqlite_conn.commit()
            copied += len(batch)
            print(f"  Progress: {copied:,} / {total:,} ({100*copied//total}%)", end='\r')
            batch = []

    # Insert remaining rows
    if batch:
        sqlite_cursor.executemany(insert_sql, batch)
        sqlite_conn.commit()
        copied += len(batch)

    print(f"  ✓ Completed: {copied:,} rows" + " " * 20)


def main():
    print("=" * 60)
    print("PostgreSQL to SQLite Export")
    print("=" * 60)

    try:
        # Connect to PostgreSQL
        print(f"\nConnecting to PostgreSQL at {PG_CONFIG['host']}...")
        pg_conn = psycopg2.connect(**PG_CONFIG)
        print("✓ Connected to PostgreSQL")

        # Connect to SQLite (creates file if doesn't exist)
        print(f"\nCreating SQLite database: {SQLITE_DB}...")
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        print("✓ Connected to SQLite")

        # Create schema
        create_sqlite_schema(sqlite_conn)

        # Copy data
        print("\n" + "=" * 60)
        print("Copying data (this may take a few minutes)...")
        print("=" * 60)

        copy_table(pg_conn, sqlite_conn, 'parameters',
                  'code, short_name, long_name')

        copy_table(pg_conn, sqlite_conn, 'stations',
                  'agency, station_id, station_name, agency_name, state, county, latitude, longitude, huc, station_type, description')

        copy_table(pg_conn, sqlite_conn, 'results',
                  'agency, station_id, param_code, start_date, start_time, result_value, huc, sample_depth',
                  insert_columns='agency, station_id, param_code, start_date, start_time, result_value, huc, sample_depth',
                  batch_size=10000)

        # Close connections
        pg_conn.close()
        sqlite_conn.close()

        # Show file size
        import os
        size_mb = os.path.getsize(SQLITE_DB) / (1024 * 1024)

        print("\n" + "=" * 60)
        print("✓ Export complete!")
        print("=" * 60)
        print(f"\nSQLite database: {SQLITE_DB}")
        print(f"File size: {size_mb:.1f} MB")
        print("\nStudents can now use this file without a PostgreSQL server!")
        print("\nTo test the database:")
        print(f"  sqlite3 {SQLITE_DB}")
        print(f"  sqlite> SELECT COUNT(*) FROM results;")

    except psycopg2.Error as e:
        print(f"\n✗ PostgreSQL error: {e}")
        sys.exit(1)
    except sqlite3.Error as e:
        print(f"\n✗ SQLite error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
