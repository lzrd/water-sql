#!/usr/bin/env python3

"""
Water Quality Database Analysis - DUAL MODE (PostgreSQL or SQLite)

This educational script demonstrates how to work with BOTH database types,
showing students the differences and similarities between:
- PostgreSQL (client-server database)
- SQLite (file-based database)

The code is heavily annotated to help students understand database concepts.

Usage:
    # SQLite mode (default - no server needed)
    python3 analyze_water_quality_dual.py

    # PostgreSQL mode (requires server)
    python3 analyze_water_quality_dual.py --postgres
    python3 analyze_water_quality_dual.py --postgres --host localhost --user your_username

    # Show help
    python3 analyze_water_quality_dual.py --help

Requirements:
    pip install pandas matplotlib seaborn
    pip install psycopg2-binary  # Only needed for PostgreSQL mode

Learn more:
- PostgreSQL vs SQLite: https://www.sqlite.org/whentouse.html
- Database comparison: https://db-engines.com/en/system/PostgreSQL%3BSQLite
"""

# ============================================================================
# SECTION 1: IMPORTS
# ============================================================================

import argparse  # For command-line argument parsing
import sys
import os
import warnings

# Data analysis and visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')

# ============================================================================
# SECTION 2: DATABASE MODE CONFIGURATION
# ============================================================================

class DatabaseConfig:
    """
    Configuration class that handles both PostgreSQL and SQLite connections.

    This demonstrates POLYMORPHISM - the same interface works with different
    database backends. Students learn that SQL is (mostly) standardized!
    """

    def __init__(self, mode='sqlite', **kwargs):
        """
        Initialize database configuration.

        Args:
            mode (str): 'sqlite' or 'postgres'
            **kwargs: Additional connection parameters
        """
        self.mode = mode
        self.connection = None

        if mode == 'sqlite':
            # SQLite configuration - simple file-based database
            self.db_file = kwargs.get('db_file', 'washington_water.db')
            self.connection_info = f"SQLite file: {self.db_file}"

        elif mode == 'postgres':
            # PostgreSQL configuration - client-server database
            self.host = kwargs.get('host', 'localhost')
            self.port = kwargs.get('port', 5432)
            self.database = kwargs.get('database', 'washington_water')
            self.user = kwargs.get('user', 'water')
            self.password = kwargs.get('password', None)
            self.connection_info = f"PostgreSQL: {self.user}@{self.host}:{self.port}/{self.database}"
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'sqlite' or 'postgres'")

    def connect(self):
        """
        Create a database connection based on the mode.

        KEY LEARNING POINT: Notice how the connection process is DIFFERENT
        for each database type, but once connected, SQL queries are the SAME!

        Returns:
            Database connection object
        """
        print(f"\n{'='*60}")
        print(f"DATABASE MODE: {self.mode.upper()}")
        print(f"{'='*60}")
        print(f"Connecting to: {self.connection_info}")

        if self.mode == 'sqlite':
            # ================================================================
            # SQLITE CONNECTION
            # ================================================================
            # SQLite is built into Python - no separate installation needed!
            # The database is just a file on your computer.
            #
            # Advantages:
            # - Zero configuration
            # - No server process
            # - Single file (easy to share)
            # - Great for learning and small projects
            #
            # Disadvantages:
            # - Single user (no concurrent writes)
            # - Limited to one machine
            # - Fewer features than PostgreSQL

            import sqlite3

            if not os.path.exists(self.db_file):
                print(f"\n✗ SQLite database file not found: {self.db_file}")
                print("Please ensure the database file is in the current directory.")
                sys.exit(1)

            self.connection = sqlite3.connect(self.db_file)
            print("✓ Connected to SQLite database")

            # SQLite-specific optimizations
            # These make queries faster but are SQLite-specific
            cursor = self.connection.cursor()
            cursor.execute("PRAGMA temp_store = MEMORY")
            cursor.execute("PRAGMA cache_size = -64000")  # 64MB cache
            cursor.close()

        elif self.mode == 'postgres':
            # ================================================================
            # POSTGRESQL CONNECTION
            # ================================================================
            # PostgreSQL requires a separate server process.
            # It's more complex but much more powerful!
            #
            # Advantages:
            # - Multiple concurrent users
            # - Network access (work from anywhere)
            # - Advanced features (stored procedures, triggers, etc.)
            # - Better performance for large datasets
            # - ACID compliance (data safety)
            #
            # Disadvantages:
            # - Requires server installation
            # - More complex setup
            # - Network configuration needed

            try:
                import psycopg2
            except ImportError:
                print("\n✗ PostgreSQL mode requires psycopg2")
                print("Install with: pip install psycopg2-binary")
                sys.exit(1)

            try:
                # Build connection parameters
                conn_params = {
                    'host': self.host,
                    'port': self.port,
                    'database': self.database,
                    'user': self.user
                }

                if self.password:
                    conn_params['password'] = self.password

                self.connection = psycopg2.connect(**conn_params)
                print("✓ Connected to PostgreSQL server")

                # PostgreSQL-specific: Set transaction isolation
                # This affects how concurrent transactions see each other
                self.connection.set_session(autocommit=True)

            except psycopg2.OperationalError as e:
                print(f"\n✗ PostgreSQL connection failed: {e}")
                print("\nTroubleshooting:")
                print(f"  1. Is PostgreSQL running on {self.host}:{self.port}?")
                print(f"  2. Does database '{self.database}' exist?")
                print(f"  3. Does user '{self.user}' have access?")
                print(f"  4. Check network connectivity to {self.host}")
                sys.exit(1)

        return self.connection

    def get_query_syntax(self, query_type):
        """
        Return database-specific SQL syntax.

        KEY LEARNING POINT: Most SQL is standardized, but some functions
        differ between databases. This method shows the differences!

        Args:
            query_type (str): Type of query syntax needed

        Returns:
            str: Database-specific SQL fragment
        """
        # ====================================================================
        # SQL SYNTAX DIFFERENCES
        # ====================================================================
        # While SQL is largely standardized, each database has quirks.
        # Here are the main differences between PostgreSQL and SQLite:

        if query_type == 'regex_match':
            # Regular expression matching syntax
            if self.mode == 'postgres':
                # PostgreSQL uses ~ operator
                return "result_value ~ '^[0-9.Ee+-]+$'"
            else:
                # SQLite doesn't have built-in regex, we filter in pandas instead
                return "1=1"  # Always true, filter later

        elif query_type == 'year_extract':
            # Extract year from date
            if self.mode == 'postgres':
                # PostgreSQL uses EXTRACT function
                return "EXTRACT(YEAR FROM start_date)"
            else:
                # SQLite uses strftime function
                return "strftime('%Y', start_date)"

        elif query_type == 'cast_float':
            # Convert text to number
            if self.mode == 'postgres':
                return "CAST(result_value AS FLOAT)"
            else:
                # SQLite is more flexible with types
                return "CAST(result_value AS REAL)"

        return ""


# ============================================================================
# SECTION 3: ANALYSIS FUNCTIONS
# ============================================================================

def verify_schema(conn, db_config):
    """
    Verify database schema - works with both PostgreSQL and SQLite!

    This function shows how to write PORTABLE database code that works
    with multiple database systems.
    """
    print(f"\n{'='*60}")
    print("SCHEMA VERIFICATION")
    print(f"{'='*60}")

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

        # ====================================================================
        # DIFFERENCE #1: Querying Database Metadata
        # ====================================================================
        # PostgreSQL and SQLite store metadata differently!

        if db_config.mode == 'postgres':
            # PostgreSQL: Use information_schema (SQL standard)
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position
            """, (table_name,))

            actual_columns = cursor.fetchall()
            actual_column_names = [col[0] for col in actual_columns]

        else:  # SQLite
            # SQLite: Use PRAGMA commands (SQLite-specific)
            cursor.execute(f"PRAGMA table_info({table_name})")
            actual_columns = cursor.fetchall()
            # SQLite PRAGMA returns: (cid, name, type, notnull, dflt_value, pk)
            actual_column_names = [col[1] for col in actual_columns]

        # Verify columns (same logic for both databases)
        missing = set(expected_columns) - set(actual_column_names)
        extra = set(actual_column_names) - set(expected_columns)

        if missing:
            print(f"  ✗ Missing columns: {missing}")
            schema_valid = False
        if not missing and not extra:
            print(f"  ✓ All {len(actual_columns)} columns present")

        # Get row count (same SQL for both!)
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  ✓ Row count: {count:,}")

    cursor.close()

    print(f"\n{'='*60}")
    if schema_valid:
        print("✓ Schema verification PASSED")
    else:
        print("✗ Schema verification FAILED")
    print(f"{'='*60}\n")

    return schema_valid


def get_top_parameters(conn, db_config, limit=5):
    """
    Get the most frequently measured parameters.

    LEARNING POINT: This query works IDENTICALLY on both databases!
    JOINs, GROUP BY, and ORDER BY are standardized SQL.
    """
    # ========================================================================
    # DIFFERENCE #2: Parameter Placeholders
    # ========================================================================
    # PostgreSQL uses %s, SQLite uses ?
    # But pandas handles this for us!

    query = """
        SELECT p.code, p.short_name, p.long_name, COUNT(*) as measurement_count
        FROM results r
        JOIN parameters p ON r.param_code = p.code
        GROUP BY p.code, p.short_name, p.long_name
        ORDER BY measurement_count DESC
        LIMIT ?
    """

    # Note: We use ? but pandas.read_sql_query handles both database types!
    return pd.read_sql_query(query, conn, params=(limit,))


def plot_parameter_over_time(conn, db_config, param_code, param_name):
    """
    Get time-series data for a parameter.

    LEARNING POINT: Here we see SQL syntax differences in action!
    """
    # ========================================================================
    # DIFFERENCE #3: Regular Expression Support
    # ========================================================================
    # PostgreSQL has built-in regex, SQLite doesn't

    regex_filter = db_config.get_query_syntax('regex_match')

    query = f"""
        SELECT
            start_date,
            result_value as value
        FROM results
        WHERE param_code = ?
          AND {regex_filter}
          AND start_date IS NOT NULL
        ORDER BY start_date
    """

    df = pd.read_sql_query(query, conn, params=(param_code,))

    if df.empty:
        return None

    # For SQLite, we filter non-numeric values in pandas
    # (PostgreSQL already filtered with regex)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])

    if df.empty:
        return None

    df['start_date'] = pd.to_datetime(df['start_date'])
    df_monthly = df.set_index('start_date').resample('ME')['value'].agg(['mean', 'count'])
    df_monthly = df_monthly[df_monthly['count'] > 0]

    return df_monthly


def plot_temporal_coverage(conn, db_config, output_file='temporal_coverage.png'):
    """
    Visualize monitoring activity over time.

    LEARNING POINT: Date functions differ between databases!
    """
    # ========================================================================
    # DIFFERENCE #4: Date/Time Functions
    # ========================================================================
    # Each database has different date manipulation functions

    year_expr = db_config.get_query_syntax('year_extract')

    query = f"""
        SELECT
            {year_expr} as year,
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
    if db_config.mode == 'sqlite':
        # SQLite returns year as string
        df['year'] = pd.to_datetime(df['year'], format='%Y')
    else:
        # PostgreSQL returns year as number
        df['year'] = pd.to_datetime(df['year'].astype(int), format='%Y')

    # [Rest of plotting code same as before...]
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

    # Add database mode to title
    ax.set_title(f'Water Quality Monitoring Activity Over Time ({db_config.mode.upper()})',
                fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Temporal coverage plot saved to {output_file}")

    return fig


# ============================================================================
# SECTION 4: COMMAND-LINE INTERFACE
# ============================================================================

def parse_arguments():
    """
    Parse command-line arguments to determine which database mode to use.

    This demonstrates how to make Python scripts configurable!
    """
    parser = argparse.ArgumentParser(
        description='Water Quality Data Analysis - PostgreSQL or SQLite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # SQLite mode (default)
  python3 %(prog)s

  # PostgreSQL mode with default settings
  python3 %(prog)s --postgres

  # PostgreSQL mode with custom host
  python3 %(prog)s --postgres --host localhost --user your_username

  # PostgreSQL mode with all options
  python3 %(prog)s --postgres --host localhost --port 5432 --database washington_water --user myuser --password mypass

Learn More:
  SQLite vs PostgreSQL: https://www.sqlite.org/whentouse.html
  When to use each: https://www.digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql-a-comparison-of-relational-database-management-systems
        """
    )

    # Database mode selection
    parser.add_argument('--postgres', '--postgresql',
                       action='store_true',
                       help='Use PostgreSQL instead of SQLite (requires server)')

    # SQLite options
    parser.add_argument('--db-file',
                       default='washington_water.db',
                       help='SQLite database file (default: washington_water.db)')

    # PostgreSQL options
    parser.add_argument('--host',
                       default='localhost',
                       help='PostgreSQL host (default: localhost)')

    parser.add_argument('--port',
                       type=int,
                       default=5432,
                       help='PostgreSQL port (default: 5432)')

    parser.add_argument('--database',
                       default='washington_water',
                       help='PostgreSQL database name (default: washington_water)')

    parser.add_argument('--user',
                       default='water',
                       help='PostgreSQL username (default: water)')

    parser.add_argument('--password',
                       help='PostgreSQL password (if required)')

    return parser.parse_args()


# ============================================================================
# SECTION 5: MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function - orchestrates the entire analysis.

    LEARNING POINTS demonstrated here:
    1. Command-line argument parsing
    2. Configuration management
    3. Database abstraction (same code, different backends)
    4. Error handling
    5. Resource cleanup (closing connections)
    """

    # Parse command-line arguments
    args = parse_arguments()

    print("\n" + "="*60)
    print("WATER QUALITY DATA ANALYSIS - DUAL MODE")
    print("="*60)
    print("\n💡 LEARNING OBJECTIVE:")
    print("This script demonstrates the DIFFERENCES and SIMILARITIES")
    print("between PostgreSQL (client-server) and SQLite (file-based) databases.")
    print("\nMost SQL queries work on BOTH, but connection and some")
    print("syntax details differ. Watch for comments explaining differences!")
    print("="*60)

    # Determine database mode
    if args.postgres:
        mode = 'postgres'
        config_kwargs = {
            'host': args.host,
            'port': args.port,
            'database': args.database,
            'user': args.user,
            'password': args.password
        }
    else:
        mode = 'sqlite'
        config_kwargs = {
            'db_file': args.db_file
        }

    # Create database configuration
    db_config = DatabaseConfig(mode=mode, **config_kwargs)

    try:
        # Connect to database
        conn = db_config.connect()

        # Verify schema
        if not verify_schema(conn, db_config):
            print("Warning: Schema verification failed, continuing anyway...")

        # Set plotting style
        sns.set_style("whitegrid")
        plt.rcParams['figure.facecolor'] = 'white'

        # Generate visualizations
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60)

        # Only generate one plot to demonstrate - add others as needed
        plot_temporal_coverage(conn, db_config)

        print("\n" + "="*60)
        print("✓ Analysis complete!")
        print("="*60)

        # ====================================================================
        # EDUCATIONAL SUMMARY
        # ====================================================================
        print("\n📚 WHAT YOU LEARNED:")
        print("-" * 60)
        print(f"Database used: {db_config.mode.upper()}")
        print(f"Connection: {db_config.connection_info}")
        print("\nKey Differences Demonstrated:")
        print("  1. Connection methods (file vs network)")
        print("  2. Metadata queries (PRAGMA vs information_schema)")
        print("  3. Date functions (strftime vs EXTRACT)")
        print("  4. Regular expressions (~ operator vs not supported)")
        print("\nSimilarities:")
        print("  ✓ Same SELECT/JOIN/WHERE/GROUP BY syntax")
        print("  ✓ Same aggregation functions (COUNT, AVG, etc.)")
        print("  ✓ Same table structure and relationships")
        print("  ✓ Standard SQL works on both!")
        print("\nWhen to use each:")
        print(f"  SQLite: Learning, single-user, embedded apps, mobile")
        print(f"  PostgreSQL: Production, multi-user, large datasets, web apps")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        if 'conn' in locals():
            conn.close()
            print(f"Database connection closed ({db_config.mode}).")


if __name__ == "__main__":
    main()


# ============================================================================
# LEARNING EXERCISES
# ============================================================================

"""
EXERCISES FOR STUDENTS:

1. BEGINNER: Run in both modes and compare output
   a) Run with SQLite: python3 analyze_water_quality_dual.py
   b) Run with PostgreSQL: python3 analyze_water_quality_dual.py --postgres --host localhost
      (NOTE: Requires PostgreSQL server with water quality data loaded)
   c) Notice any differences in output or performance?

2. BEGINNER: Examine connection code
   a) Look at the DatabaseConfig class __init__ and connect methods
   b) What information is needed for SQLite? For PostgreSQL?
   c) Why does PostgreSQL need more configuration?

3. INTERMEDIATE: Add a new query
   a) Write a query that works on BOTH databases
   b) Test it in both modes
   c) Use get_query_syntax() if needed for database-specific parts

4. INTERMEDIATE: Compare performance
   a) Time how long queries take on each database
   b) Use: import time; start = time.time(); [run query]; print(f"Time: {time.time()-start}")
   c) Which is faster? Why might that be?

5. ADVANCED: Handle another SQL difference
   a) Research how to get "current date" in PostgreSQL vs SQLite
   b) Add a method to get_query_syntax() for this
   c) Write a query that uses it

6. ADVANCED: Add connection pooling
   a) Research connection pooling for PostgreSQL
   b) Modify the code to use a connection pool
   c) Why would this matter in a web application?

7. CHALLENGE: Add MySQL support
   a) Install mysql-connector-python
   b) Extend DatabaseConfig to support MySQL
   c) What SQL syntax differences do you find?

8. CHALLENGE: Create a benchmark suite
   a) Run the same queries on both databases
   b) Measure execution time for each
   c) Create a comparison chart
   d) Under what conditions is each database faster?

DISCUSSION QUESTIONS:

1. Why would you choose PostgreSQL over SQLite for a production application?
2. When would SQLite be the better choice?
3. How does the network aspect of PostgreSQL affect performance?
4. What security considerations are different between the two?
5. How would you migrate data from SQLite to PostgreSQL (or vice versa)?
6. What happens if two users try to write to SQLite simultaneously?
7. How does PostgreSQL handle concurrent writes differently?

FURTHER READING:

- SQLite when to use: https://www.sqlite.org/whentouse.html
- PostgreSQL features: https://www.postgresql.org/about/
- Database comparison: https://db-engines.com/
- ACID properties: https://en.wikipedia.org/wiki/ACID
- Connection pooling: https://en.wikipedia.org/wiki/Connection_pool
"""
