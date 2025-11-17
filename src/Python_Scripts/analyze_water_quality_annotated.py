#!/usr/bin/env python3

"""
Water Quality Database Analysis and Visualization - ANNOTATED FOR LEARNING

⚠️ ADVANCED: This script uses PostgreSQL (requires database server)
⚠️ BEGINNERS: Use analyze_water_quality_sqlite.py instead (no server needed)

This script demonstrates how to:
1. Connect to a PostgreSQL database server from Python
2. Query data using SQL
3. Process data with pandas (a data analysis library)
4. Create visualizations with matplotlib and seaborn

Author: Claude Code
Purpose: Educational example for advanced students with PostgreSQL access
Database: Washington State Water Quality Monitoring Data (3.1M+ measurements)

Requirements:
    pip install psycopg2-binary pandas matplotlib seaborn sqlalchemy

    PLUS: Access to a PostgreSQL database server with the water quality data loaded

Usage:
    python3 analyze_water_quality_annotated.py

    NOTE: You must update DB_CONFIG below with your PostgreSQL server details

Learn more:
- PostgreSQL: https://www.postgresql.org/
- pandas: https://pandas.pydata.org/
- matplotlib: https://matplotlib.org/
- seaborn: https://seaborn.pydata.org/
"""

# ============================================================================
# SECTION 1: IMPORT LIBRARIES
# ============================================================================
# Libraries are pre-written code that add functionality to Python

import psycopg2                    # PostgreSQL database adapter for Python
from psycopg2 import sql          # Tools for building safe SQL queries
import pandas as pd                # Data analysis and manipulation library
import matplotlib.pyplot as plt    # Main plotting library
import seaborn as sns              # Statistical visualization (prettier plots)
from datetime import datetime      # For working with dates and times
import sys                         # System-specific parameters and functions
import warnings                    # Control warning messages
from sqlalchemy import create_engine  # Database connection toolkit

# Configure warning display
# Some libraries show warnings that aren't problems - we suppress them here
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')

# ============================================================================
# SECTION 2: CONFIGURATION
# ============================================================================
# This dictionary contains our database connection information

DB_CONFIG = {
    'host': 'localhost',             # Server address (use 'localhost' or your server IP)
    'port': 5432,                    # PostgreSQL default port
    'database': 'washington_water',  # Name of your database
    'user': 'your_username',         # Your PostgreSQL username
    'password': 'your_password'      # Your PostgreSQL password (if required)
    # NOTE: Update these values for your PostgreSQL server setup
}


# ============================================================================
# SECTION 3: SCHEMA VERIFICATION FUNCTION
# ============================================================================

def verify_schema(conn):
    """
    Verify that all expected tables and columns exist in the database.

    This is like checking that a filing cabinet has all the expected drawers
    and folders before you start looking for files.

    Args:
        conn: A psycopg2 database connection object

    Returns:
        bool: True if schema is valid, False if something is missing

    Learn more about database schemas:
    https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-schema/
    """
    print("=" * 60)
    print("SCHEMA VERIFICATION")
    print("=" * 60)

    # This dictionary defines what we EXPECT to find in the database
    # Each key is a table name, each value is a list of column names
    expected_schema = {
        'parameters': ['code', 'short_name', 'long_name'],
        'stations': ['agency', 'station_id', 'station_name', 'agency_name',
                     'state', 'county', 'latitude', 'longitude', 'huc',
                     'station_type', 'description'],
        'results': ['id', 'agency', 'station_id', 'param_code', 'start_date',
                    'start_time', 'result_value', 'huc', 'sample_depth']
    }

    # Create a cursor - this is like opening a communication channel to the database
    # Think of it as picking up the phone to talk to the database
    cursor = conn.cursor()

    # We'll track whether everything is OK
    schema_valid = True

    # Loop through each table we expect to find
    # .items() gives us both the key (table_name) and value (expected_columns)
    for table_name, expected_columns in expected_schema.items():
        print(f"\n{table_name.upper()} table:")

        # Check if table exists
        # This SQL query asks the database's information_schema (metadata about the database)
        # %s is a placeholder that will be safely replaced with table_name
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = %s
            );
        """, (table_name,))

        # fetchone() gets one row from the query result
        # [0] gets the first (and only) column from that row
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print(f"  ✗ Table does not exist!")
            schema_valid = False
            continue  # Skip to next table

        # Get actual columns from the database
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
              AND table_schema = 'public'
            ORDER BY ordinal_position;
        """, (table_name,))

        # fetchall() gets ALL rows from the query result
        # Returns a list of tuples: [('code', 'character varying'), ('short_name', 'character varying'), ...]
        actual_columns = cursor.fetchall()

        # Extract just the column names (first element of each tuple)
        # List comprehension: [expression for item in list]
        actual_column_names = [col[0] for col in actual_columns]

        # Verify columns match what we expect
        # set() creates a mathematical set - useful for finding differences
        missing = set(expected_columns) - set(actual_column_names)
        extra = set(actual_column_names) - set(expected_columns)

        # Report any problems
        if missing:
            print(f"  ✗ Missing columns: {missing}")
            schema_valid = False
        if extra:
            print(f"  ⚠ Extra columns: {extra}")

        if not missing and not extra:
            print(f"  ✓ All {len(actual_columns)} columns present")

        # Get row count - how much data is in this table?
        # sql.Identifier() safely quotes table name to prevent SQL injection
        cursor.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(
            sql.Identifier(table_name)
        ))
        count = cursor.fetchone()[0]

        # Format number with commas for readability: 3178425 → 3,178,425
        print(f"  ✓ Row count: {count:,}")

    # Check indexes (these make queries faster)
    print(f"\nINDEXES:")
    cursor.execute("""
        SELECT tablename, indexname
        FROM pg_indexes
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname;
    """)
    indexes = cursor.fetchall()
    for table, index in indexes:
        print(f"  ✓ {table}.{index}")

    # Close the cursor - we're done talking to the database for now
    cursor.close()

    # Print final verdict
    print("\n" + "=" * 60)
    if schema_valid:
        print("✓ Schema verification PASSED")
    else:
        print("✗ Schema verification FAILED")
    print("=" * 60 + "\n")

    return schema_valid


# ============================================================================
# SECTION 4: DATA QUERY FUNCTIONS
# ============================================================================

def get_top_parameters(conn, limit=5):
    """
    Find the most frequently measured water quality parameters.

    This function joins the results and parameters tables, counts measurements,
    and returns the top N most measured parameters.

    Args:
        conn: Database connection
        limit (int): How many top parameters to return (default 5)

    Returns:
        pandas.DataFrame: Table with columns [code, short_name, long_name, measurement_count]

    Learn more about SQL JOINs:
    https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-joins/
    """
    # This SQL query is more complex - let's break it down:
    #
    # SELECT - what columns do we want?
    #   p.code - parameter code from parameters table (p. is alias)
    #   p.short_name - short name from parameters table
    #   p.long_name - full name from parameters table
    #   COUNT(*) as measurement_count - count all matching rows, call it "measurement_count"
    #
    # FROM results r - start with results table, call it "r" for short
    # JOIN parameters p ON r.param_code = p.code - connect to parameters table where codes match
    #
    # GROUP BY - combine rows with same code/names into one row
    #   This is necessary when using COUNT() - we count within each group
    #
    # ORDER BY measurement_count DESC - sort by count, largest first (DESC = descending)
    # LIMIT %s - only return the top N rows (%s will be replaced with limit parameter)

    query = """
        SELECT p.code, p.short_name, p.long_name, COUNT(*) as measurement_count
        FROM results r
        JOIN parameters p ON r.param_code = p.code
        GROUP BY p.code, p.short_name, p.long_name
        ORDER BY measurement_count DESC
        LIMIT %s;
    """

    # pandas.read_sql_query() executes the SQL and returns results as a DataFrame
    # DataFrame is like a spreadsheet in Python - rows and columns of data
    # params=(limit,) passes the limit value to replace %s in the query
    # The comma in (limit,) makes it a tuple - SQL requires parameters as a sequence
    return pd.read_sql_query(query, conn, params=(limit,))


def plot_parameter_over_time(conn, param_code, param_name):
    """
    Extract time-series data for a specific water quality parameter.

    This function gets all measurements for one parameter and groups them
    by month to create a time series suitable for plotting.

    Args:
        conn: Database connection
        param_code (str): Parameter code (e.g., '00010' for temperature)
        param_name (str): Human-readable parameter name (for messages)

    Returns:
        pandas.DataFrame: Monthly aggregated data with columns [mean, count]
                         Index is datetime (month-end dates)
        None: If no valid data found

    Learn more about pandas time series:
    https://pandas.pydata.org/docs/user_guide/timeseries.html
    """
    # This query gets individual measurements
    query = """
        SELECT
            start_date,
            CAST(result_value AS FLOAT) as value
        FROM results
        WHERE param_code = %s
          AND result_value ~ '^[0-9.Ee+-]+$'  -- Regex: only numeric values
          AND start_date IS NOT NULL
        ORDER BY start_date;
    """
    # The regex '^[0-9.Ee+-]+$' matches scientific notation like "300000E-5"
    # ^ = start of string, $ = end of string
    # [0-9.Ee+-]+ = one or more of: digits, decimal point, E, e, +, -

    df = pd.read_sql_query(query, conn, params=(param_code,))

    if df.empty:
        print(f"No numeric data found for parameter {param_code}")
        return None

    # Convert 'start_date' column from strings to datetime objects
    # This allows pandas to understand them as dates for time-based operations
    df['start_date'] = pd.to_datetime(df['start_date'])

    # Group by month and calculate statistics
    # .set_index('start_date') - use dates as the index (row labels)
    # .resample('ME') - group by Month End (ME)
    # ['value'] - only process the 'value' column
    # .agg(['mean', 'count']) - calculate both mean and count for each month
    df_monthly = df.set_index('start_date').resample('ME')['value'].agg(['mean', 'count'])

    # Filter out months with no data (count = 0)
    df_monthly = df_monthly[df_monthly['count'] > 0]

    return df_monthly


# ============================================================================
# SECTION 5: PLOTTING FUNCTIONS
# ============================================================================

def plot_multiple_parameters(conn, output_file='water_quality_analysis.png'):
    """
    Create a multi-panel visualization of top water quality parameters.

    This function creates a 3x2 grid of plots (6 subplots total), each showing
    how one parameter changed over time.

    Args:
        conn: Database connection
        output_file (str): Where to save the PNG image

    Returns:
        matplotlib.figure.Figure: The created figure object

    Learn more about matplotlib subplots:
    https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
    """
    print("\nFetching top parameters...")
    top_params = get_top_parameters(conn, limit=6)

    print("\nTop 6 Most Measured Parameters:")
    # .to_string(index=False) prints the DataFrame nicely without row numbers
    print(top_params.to_string(index=False))
    print()

    # Create a figure with 6 subplots arranged in 3 rows, 2 columns
    # figsize=(16, 12) means 16 inches wide, 12 inches tall
    # Returns: fig (the whole figure) and axes (array of subplot objects)
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))

    # Add a title to the whole figure
    fig.suptitle('Washington State Water Quality Parameters Over Time',
                 fontsize=16, fontweight='bold')

    # .flatten() converts the 2D array of axes into a 1D list for easy iteration
    # Before: [[ax1, ax2], [ax3, ax4], [ax5, ax6]]
    # After: [ax1, ax2, ax3, ax4, ax5, ax6]
    axes = axes.flatten()

    # Loop through each parameter
    # enumerate(top_params.iterrows()) gives us:
    #   idx - the position (0, 1, 2, ...)
    #   (_, param) - a tuple of (index, row data) from the DataFrame
    #                we use _ for the index because we don't need it
    for idx, (_, param) in enumerate(top_params.iterrows()):
        if idx >= 6:  # Safety check
            break

        # Extract data from this row
        code = param['code']
        name = param['short_name'] or param['long_name']  # Use short_name, or long_name if short is missing
        count = param['measurement_count']

        print(f"Processing {code} - {name}...")

        # Get the time series data for this parameter
        df_monthly = plot_parameter_over_time(conn, code, name)

        if df_monthly is not None and not df_monthly.empty:
            # Get the corresponding subplot
            ax = axes[idx]

            # Plot the monthly mean values as a line
            # df_monthly.index contains the dates (x-axis)
            # df_monthly['mean'] contains the average values (y-axis)
            ax.plot(df_monthly.index, df_monthly['mean'],
                   linewidth=1.5,      # Line thickness
                   alpha=0.8,          # Transparency (0=invisible, 1=opaque)
                   color='steelblue')  # Color name

            # Add scatter points to show individual months
            ax.scatter(df_monthly.index, df_monthly['mean'],
                      s=10,               # Size of points
                      alpha=0.5,          # Half transparent
                      color='steelblue')

            # Set subplot title
            # \n creates a new line
            # :, formats the number with commas (e.g., 290,975)
            ax.set_title(f'{code}: {name}\n({count:,} measurements)',
                        fontsize=10, fontweight='bold')

            # Label the axes
            ax.set_xlabel('Date', fontsize=9)
            ax.set_ylabel('Value', fontsize=9)

            # Add a grid for easier reading
            ax.grid(True,              # Turn grid on
                   alpha=0.3,          # Make it faint
                   linestyle='--')     # Dashed lines

            # Make tick labels smaller
            ax.tick_params(axis='both', which='major', labelsize=8)

            # Rotate x-axis date labels so they don't overlap
            # ha='right' means horizontal alignment = right
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Adjust spacing between subplots to prevent overlap
    plt.tight_layout()

    # Save the figure to a file
    # dpi=300 means 300 dots per inch (high quality)
    # bbox_inches='tight' removes extra whitespace
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot saved to {output_file}")

    return fig


def plot_county_comparison(conn, output_file='county_comparison.png'):
    """
    Compare water quality measurements across counties.

    Creates two side-by-side bar charts showing which counties have
    the most measurements and the most monitoring stations.

    Args:
        conn: Database connection
        output_file (str): Where to save the PNG image

    Returns:
        matplotlib.figure.Figure: The created figure object

    Learn more about bar charts:
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/barh.html
    """
    # This query joins results and stations tables to count by county
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
        LIMIT 15;
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("No county data found")
        return None

    # Create figure with 2 subplots side by side (1 row, 2 columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    fig.suptitle('Water Quality Monitoring by County',
                 fontsize=16, fontweight='bold')

    # First plot: Horizontal bar chart of measurements
    # .barh() creates horizontal bars (barh = bar horizontal)
    ax1.barh(df['county'], df['measurement_count'], color='steelblue')
    ax1.set_xlabel('Number of Measurements', fontsize=12)
    ax1.set_ylabel('County', fontsize=12)
    ax1.set_title('Total Measurements by County', fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3, linestyle='--')  # Only horizontal grid lines

    # Add value labels at the end of each bar
    # enumerate() gives us position (i) and value (v)
    for i, v in enumerate(df['measurement_count']):
        # ax1.text(x, y, text_string, alignment)
        # v is the x position (end of the bar)
        # i is the y position (which bar)
        # f' {v:,}' formats the number with comma separator and a leading space
        ax1.text(v, i, f' {v:,}', va='center', fontsize=8)

    # Second plot: Stations by county
    ax2.barh(df['county'], df['station_count'], color='coral')
    ax2.set_xlabel('Number of Monitoring Stations', fontsize=12)
    ax2.set_ylabel('County', fontsize=12)
    ax2.set_title('Monitoring Stations by County', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3, linestyle='--')

    # Add value labels
    for i, v in enumerate(df['station_count']):
        ax2.text(v, i, f' {v}', va='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ County comparison plot saved to {output_file}")

    return fig


def plot_temporal_coverage(conn, output_file='temporal_coverage.png'):
    """
    Visualize temporal coverage of measurements over the years.

    Creates a combination plot showing:
    - Bar chart: Total measurements per year
    - Line plots: Number of active stations and parameters per year

    This helps identify when monitoring was most active.

    Args:
        conn: Database connection
        output_file (str): Where to save the PNG image

    Returns:
        matplotlib.figure.Figure: The created figure object

    Learn more about dual-axis plots:
    https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
    """
    # DATE_TRUNC('year', start_date) rounds dates down to January 1st of that year
    # This groups all measurements from each year together
    query = """
        SELECT
            DATE_TRUNC('year', start_date) as year,
            COUNT(*) as measurement_count,
            COUNT(DISTINCT station_id) as station_count,
            COUNT(DISTINCT param_code) as parameter_count
        FROM results
        WHERE start_date IS NOT NULL
        GROUP BY year
        ORDER BY year;
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("No temporal data found")
        return None

    # Convert year column to datetime for better plotting
    df['year'] = pd.to_datetime(df['year'])

    # Create one subplot
    fig, ax = plt.subplots(figsize=(14, 6))

    # Create a second y-axis that shares the same x-axis
    # This allows us to plot two different scales on one chart
    ax2 = ax.twinx()

    # Plot measurements as bars on the first y-axis
    # width=250 is in days (roughly the width of each bar)
    ax.bar(df['year'], df['measurement_count'],
           width=250,          # Bar width in days
           alpha=0.6,          # Semi-transparent
           color='steelblue',
           label='Measurements')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Measurements', fontsize=12, color='steelblue')
    ax.tick_params(axis='y', labelcolor='steelblue')  # Color the tick labels to match

    # Plot stations and parameters as lines on the second y-axis
    ax2.plot(df['year'], df['station_count'],
            color='coral',
            marker='o',         # Circle markers at each point
            linewidth=2,
            label='Stations')

    ax2.plot(df['year'], df['parameter_count'],
            color='green',
            marker='s',         # Square markers
            linewidth=2,
            label='Parameters')

    ax2.set_ylabel('Count (Stations/Parameters)', fontsize=12, color='coral')
    ax2.tick_params(axis='y', labelcolor='coral')

    # Add legends (one for each axis)
    ax.legend(loc='upper left', fontsize=10)
    ax2.legend(loc='upper right', fontsize=10)

    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_title('Water Quality Monitoring Activity Over Time',
                fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Temporal coverage plot saved to {output_file}")

    return fig


# ============================================================================
# SECTION 6: MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function - orchestrates the entire analysis.

    This function:
    1. Connects to the database
    2. Verifies the schema
    3. Generates all visualizations
    4. Handles errors gracefully
    5. Closes the connection

    This is a common pattern in Python - put the main logic in a function
    that gets called when the script runs.
    """
    print("\nWashington State Water Quality Database Analysis")
    print(f"Connecting to {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}...")

    try:
        # Try to connect to the database
        # **DB_CONFIG unpacks the dictionary into keyword arguments
        # Equivalent to: psycopg2.connect(host='localhost', port=5432, ...)
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Database connection successful\n")

        # Verify schema
        if not verify_schema(conn):
            print("Warning: Schema verification failed, but continuing with analysis...\n")

        # Set plotting style
        # Seaborn provides several preset styles that make plots look nicer
        sns.set_style("whitegrid")
        plt.rcParams['figure.facecolor'] = 'white'  # White background for figures

        # Generate visualizations
        print("\n" + "=" * 60)
        print("GENERATING VISUALIZATIONS")
        print("=" * 60 + "\n")

        plot_multiple_parameters(conn, 'water_quality_analysis.png')
        plot_county_comparison(conn, 'county_comparison.png')
        plot_temporal_coverage(conn, 'temporal_coverage.png')

        print("\n" + "=" * 60)
        print("✓ Analysis complete! Check the PNG files for visualizations.")
        print("=" * 60 + "\n")

    except psycopg2.OperationalError as e:
        # This exception is raised if we can't connect to the database
        print(f"\n✗ Database connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Verify PostgreSQL is running on your server")
        print("  2. Check host, database name, username, and password in DB_CONFIG above")
        print("  3. Ensure network connectivity to your database server")
        print("  4. Verify firewall allows connection to port 5432")
        sys.exit(1)  # Exit with error code 1

    except Exception as e:
        # Catch any other unexpected errors
        print(f"\n✗ Error: {e}")

        # Print the full error traceback for debugging
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        # This block ALWAYS runs, even if there was an error
        # It ensures we clean up the database connection
        if 'conn' in locals():  # Check if conn was successfully created
            conn.close()
            print("Database connection closed.")


# ============================================================================
# SECTION 7: SCRIPT ENTRY POINT
# ============================================================================

# This is a Python idiom that checks if this file is being run directly
# (as opposed to being imported as a module by another script)
#
# __name__ is a special variable:
# - When you run "python3 script.py", __name__ == "__main__"
# - When you do "import script" from another file, __name__ == "script"
#
# This pattern allows the file to be both:
# 1. A runnable script (calls main() when executed)
# 2. An importable module (defines functions but doesn't run automatically)

if __name__ == "__main__":
    main()


# ============================================================================
# LEARNING EXERCISES
# ============================================================================

"""
EXERCISES FOR STUDENTS:

1. BEGINNER: Modify the number of parameters plotted
   - Change line 233: limit=6 to limit=3
   - Run the script and see how the output changes

2. BEGINNER: Change the output filenames
   - Change the output_file parameters in main()
   - Save plots with different names or in a subdirectory

3. INTERMEDIATE: Add a new simple plot
   - Create a function to plot measurement counts by year as a simple bar chart
   - Call it from main() to generate a fourth visualization
   - Hint: Use the query from plot_temporal_coverage() but simpler

4. INTERMEDIATE: Filter by date range
   - Modify plot_parameter_over_time() to only get data after 1990
   - Add "AND start_date >= '1990-01-01'" to the WHERE clause

5. ADVANCED: Add a new visualization type
   - Create a scatter plot of latitude vs longitude with county colors
   - This would show the geographic distribution of monitoring stations
   - Hint: Use ax.scatter() with station latitude/longitude data

6. ADVANCED: Make the script interactive
   - Use input() to ask the user which parameter code to plot
   - Allow the user to choose the date range
   - Generate a custom plot based on user input

7. CHALLENGE: Add statistical analysis
   - Calculate trend lines (linear regression) for each parameter
   - Add the trend line to the time series plots
   - Print the slope to see if values are increasing or decreasing
   - Hint: Look up scipy.stats.linregress or numpy.polyfit

8. CHALLENGE: Export data to CSV
   - After generating plots, also save the underlying data to CSV files
   - Use pandas .to_csv() method
   - Create one CSV per parameter with monthly aggregated values

DEBUGGING TIPS:

- If you get an error, read it carefully - Python tells you the line number!
- Use print() statements to see what variables contain
- Comment out code with # to disable parts while testing
- Test small changes one at a time
- Use the Python interactive shell to experiment: python3 -i script.py

EXTENDING THE SCRIPT:

Ideas for further development:
- Add command-line arguments to choose which plots to generate
- Create an HTML report with embedded images
- Connect to different databases by changing DB_CONFIG
- Add statistical tests (t-tests, ANOVA) to compare counties
- Build a web dashboard with Flask or Streamlit
- Perform anomaly detection to find unusual measurements
- Correlate water quality with weather or demographic data

Remember: Every expert was once a beginner. Start simple, experiment,
and gradually build complexity. The best way to learn is by doing!
"""
