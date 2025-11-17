#!/usr/bin/env python3
"""
Water Quality Database Analysis and Visualization - SQLite Version

This script connects to a LOCAL SQLite database file (no server needed!)
and generates time-series visualizations of Washington State water quality data.

Requirements:
    pip install pandas matplotlib seaborn

Usage:
    # Windows (PowerShell):
    python .\Python_Scripts\analyze_water_quality_sqlite.py

    # macOS/Linux:
    python3 Python_Scripts/analyze_water_quality_sqlite.py

Database file:
    washington_water.db (must be in the package root directory)
    Run this script from the package root, not from Python_Scripts/
"""

import sys
import warnings
import os
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend for headless environments
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Suppress pandas warnings
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')

# Database configuration
SQLITE_DB = os.path.join('..', os.environ.get('SQLITE_DB_NAME', 'washington_water.db'))


def verify_schema(conn):
    """
    Verify that all expected tables and columns exist in the database.

    Args:
        conn: A sqlite3 database connection object

    Returns:
        bool: True if schema is valid, False otherwise
    """
    print("=" * 60)
    print("SCHEMA VERIFICATION")
    print("=" * 60)

    expected_schema = {
        'parameters': ['code', 'short_name', 'long_name'],
        'stations': ['agency', 'station_id', 'station_name', 'agency_name',
                     'state', 'county', 'latitude', 'longitude', 'huc',
                     'station_type', 'description'],
        'results': ['id', 'agency', 'station_id', 'param_code', 'start_date',
                    'start_time', 'result_value', 'huc', 'sample_depth']
    }

    cursor = conn.cursor()
    schema_valid = True

    for table_name, expected_columns in expected_schema.items():
        print(f"\n{table_name.upper()} table:")

        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """, (table_name,))

        table_exists = cursor.fetchone() is not None

        if not table_exists:
            print(f"  ✗ Table does not exist!")
            schema_valid = False
            continue

        # Get actual columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        actual_columns = cursor.fetchall()
        actual_column_names = [col[1] for col in actual_columns]  # Column name is at index 1

        # Verify columns
        missing = set(expected_columns) - set(actual_column_names)
        extra = set(actual_column_names) - set(expected_columns)

        if missing:
            print(f"  ✗ Missing columns: {missing}")
            schema_valid = False
        if extra:
            print(f"  ⚠ Extra columns: {extra}")

        if not missing and not extra:
            print(f"  ✓ All {len(actual_columns)} columns present")

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  ✓ Row count: {count:,}")

    # Check indexes
    print(f"\nINDEXES:")
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='index' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    indexes = cursor.fetchall()
    for (index,) in indexes:
        print(f"  ✓ {index}")

    cursor.close()

    print("\n" + "=" * 60)
    if schema_valid:
        print("✓ Schema verification PASSED")
    else:
        print("✗ Schema verification FAILED")
    print("=" * 60 + "\n")

    return schema_valid


def get_top_parameters(conn, limit=5):
    """
    Find the most frequently measured water quality parameters.

    Args:
        conn: Database connection
        limit (int): How many top parameters to return

    Returns:
        pandas.DataFrame: Table with columns [code, short_name, long_name, measurement_count]
    """
    query = """
        SELECT p.code, p.short_name, p.long_name, COUNT(*) as measurement_count
        FROM results r
        JOIN parameters p ON r.param_code = p.code
        GROUP BY p.code, p.short_name, p.long_name
        ORDER BY measurement_count DESC
        LIMIT ?
    """
    return pd.read_sql_query(query, conn, params=(limit,))


def plot_parameter_over_time(conn, param_code, param_name):
    """
    Extract time-series data for a specific water quality parameter.

    Args:
        conn: Database connection
        param_code (str): Parameter code
        param_name (str): Human-readable parameter name

    Returns:
        pandas.DataFrame: Monthly aggregated data
    """
    # SQLite uses different regex syntax than PostgreSQL
    # We'll filter non-numeric values in pandas instead
    query = """
        SELECT
            start_date,
            result_value as value
        FROM results
        WHERE param_code = ?
          AND start_date IS NOT NULL
        ORDER BY start_date
    """

    df = pd.read_sql_query(query, conn, params=(param_code,))

    if df.empty:
        print(f"No data found for parameter {param_code}")
        return None

    # Convert result_value to numeric, coercing errors to NaN
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    # Drop rows where value couldn't be converted
    df = df.dropna(subset=['value'])

    if df.empty:
        print(f"No numeric data found for parameter {param_code}")
        return None

    df['start_date'] = pd.to_datetime(df['start_date'])

    # Group by month
    df_monthly = df.set_index('start_date').resample('ME')['value'].agg(['mean', 'count'])
    df_monthly = df_monthly[df_monthly['count'] > 0]

    return df_monthly


def plot_multiple_parameters(conn, output_file='water_quality_analysis.png'):
    """Create a multi-panel visualization of top water quality parameters."""
    print("\nFetching top parameters...")
    top_params = get_top_parameters(conn, limit=6)

    print("\nTop 6 Most Measured Parameters:")
    print(top_params.to_string(index=False))
    print()

    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    fig.suptitle('Washington State Water Quality Parameters Over Time',
                 fontsize=16, fontweight='bold')
    axes = axes.flatten()

    for idx, (_, param) in enumerate(top_params.iterrows()):
        if idx >= 6:
            break

        code = param['code']
        name = param['short_name'] or param['long_name']
        count = param['measurement_count']

        print(f"Processing {code} - {name}...")

        df_monthly = plot_parameter_over_time(conn, code, name)

        if df_monthly is not None and not df_monthly.empty:
            ax = axes[idx]

            ax.plot(df_monthly.index, df_monthly['mean'],
                   linewidth=1.5, alpha=0.8, color='steelblue')

            ax.scatter(df_monthly.index, df_monthly['mean'],
                      s=10, alpha=0.5, color='steelblue')

            ax.set_title(f'{code}: {name}\n({count:,} measurements)',
                        fontsize=10, fontweight='bold')
            ax.set_xlabel('Date', fontsize=9)
            ax.set_ylabel('Value', fontsize=9)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.tick_params(axis='both', which='major', labelsize=8)

            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot saved to {output_file}")

    return fig


def plot_county_comparison(conn, output_file='county_comparison.png'):
    """Compare water quality measurements across counties."""
    query = """
        SELECT
            s.county,
            COUNT(DISTINCT r.station_id) as station_count,
            COUNT(*) as measurement_count
        FROM results r
        JOIN stations s ON r.station_id = s.station_id
        WHERE s.county IS NOT NULL AND s.county != ''
        GROUP BY s.county
        ORDER BY measurement_count DESC
        LIMIT 15
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("No county data found")
        return None

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Water Quality Monitoring by County',
                 fontsize=16, fontweight='bold')

    ax1.barh(df['county'], df['measurement_count'], color='steelblue')
    ax1.set_xlabel('Number of Measurements', fontsize=12)
    ax1.set_ylabel('County', fontsize=12)
    ax1.set_title('Total Measurements by County', fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3, linestyle='--')

    for i, v in enumerate(df['measurement_count']):
        ax1.text(v, i, f' {v:,}', va='center', fontsize=8)

    ax2.barh(df['county'], df['station_count'], color='coral')
    ax2.set_xlabel('Number of Monitoring Stations', fontsize=12)
    ax2.set_ylabel('County', fontsize=12)
    ax2.set_title('Monitoring Stations by County', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3, linestyle='--')

    for i, v in enumerate(df['station_count']):
        ax2.text(v, i, f' {v}', va='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ County comparison plot saved to {output_file}")

    return fig


def plot_temporal_coverage(conn, output_file='temporal_coverage.png'):
    """Visualize temporal coverage of measurements."""
    # SQLite uses different date functions
    query = """
        SELECT
            strftime('%Y', start_date) as year,
            COUNT(*) as measurement_count,
            COUNT(DISTINCT station_id) as station_count,
            COUNT(DISTINCT param_code) as parameter_count
        FROM results
        WHERE start_date IS NOT NULL
        GROUP BY year
        ORDER BY year
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("No temporal data found")
        return None

    # Convert year to datetime
    df['year'] = pd.to_datetime(df['year'], format='%Y')

    fig, ax = plt.subplots(figsize=(14, 6))
    ax2 = ax.twinx()

    ax.bar(df['year'], df['measurement_count'],
           width=250, alpha=0.6, color='steelblue', label='Measurements')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Measurements', fontsize=12, color='steelblue')
    ax.tick_params(axis='y', labelcolor='steelblue')

    ax2.plot(df['year'], df['station_count'],
            color='coral', marker='o', linewidth=2, label='Stations')
    ax2.plot(df['year'], df['parameter_count'],
            color='green', marker='s', linewidth=2, label='Parameters')
    ax2.set_ylabel('Count (Stations/Parameters)', fontsize=12, color='coral')
    ax2.tick_params(axis='y', labelcolor='coral')

    ax.legend(loc='upper left', fontsize=10)
    ax2.legend(loc='upper right', fontsize=10)

    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_title('Water Quality Monitoring Activity Over Time',
                fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Temporal coverage plot saved to {output_file}")

    return fig


def main():
    """Main execution function."""
    print("\nWashington State Water Quality Database Analysis (SQLite)")
    print(f"Looking for database file: {SQLITE_DB}...")

    # Check if database file exists
    if not os.path.exists(SQLITE_DB):
        print(f"\n✗ Database file not found: {SQLITE_DB}")
        print("\nPlease ensure the database file is in the same directory as this script.")
        print("Expected file: washington_water.db")
        sys.exit(1)

    try:
        # Connect to SQLite database
        print("⏳ Opening database file (this may take 10-15 seconds)...")
        sys.stdout.flush()  # Force immediate output on Windows
        conn = sqlite3.connect(SQLITE_DB)
        print("✓ Connected to database")

        # Verify schema
        print("⏳ Verifying database structure (counting 3.1M measurements)...")
        sys.stdout.flush()
        if not verify_schema(conn):
            print("Warning: Schema verification failed, but continuing with analysis...\n")
        else:
            print("✓ Database ready - starting analysis\n")

        # Set plotting style
        sns.set_style("whitegrid")
        plt.rcParams['figure.facecolor'] = 'white'

        # Generate visualizations
        print("\n" + "=" * 60)
        print("GENERATING VISUALIZATIONS")
        print("=" * 60 + "\n")

        plot_multiple_parameters(conn, 'water_quality_analysis.png')
        plot_county_comparison(conn, 'county_comparison.png')
        plot_temporal_coverage(conn, 'temporal_coverage.png')

        print("\n" + "=" * 60)
        print("✓ ANALYSIS COMPLETE!")
        print("=" * 60)

        # List created PNG files
        print("\n📊 OUTPUT FILES CREATED:")
        import glob
        png_files = glob.glob("*.png")
        if png_files:
            for f in sorted(png_files):
                print(f"   • {f}")
        else:
            print("   • water_quality_analysis.png")
            print("   • county_comparison.png")
            print("   • temporal_coverage.png")

        print("\n👉 NEXT STEPS:")
        print("   1. View the PNG files (click them in VSCode file explorer)")
        print("   2. Scroll up to review statistics printed above")
        print("   3. Read WATER_DATA.html to learn more about the data")
        print("   4. Try writing your own SQL queries!")

        print("\n💡 FOR INTERVIEW PREP:")
        print("   • What patterns do you see in the visualizations?")
        print("   • Which measurements are highest/lowest?")
        print("   • What questions could you answer with this data?")
        print("   • How might a utility use this information?")
        print("\n")

    except sqlite3.Error as e:
        print(f"\n✗ Database error: {e}")
        print("\nThe database file may be corrupted or incompatible.")
        sys.exit(1)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
