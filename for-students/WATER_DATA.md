# Washington State Water Quality Database - Beginner's Guide

## Table of Contents
1. [What is This Database?](#what-is-this-database)
2. [Understanding Databases](#understanding-databases)
3. [Database Structure](#database-structure)
4. [Example SQL Queries](#example-sql-queries)
5. [Using the Analysis Script](#using-the-analysis-script)
6. [Learning Resources](#learning-resources)

---

## What is This Database?

This database contains **3.1+ million water quality measurements** from across Washington State. Scientists and environmental agencies have been collecting this data for decades to monitor the health of rivers, lakes, streams, and groundwater.

### Quick Stats
- **3,178,425** individual water quality measurements
- **6,892** monitoring stations (locations where samples were taken)
- **1,587** different parameters (things being measured, like temperature, pH, etc.)
- **Data spans from 1960s to early 2000s**

### Why Does This Matter?

Water quality data helps us:
- Detect pollution before it becomes dangerous
- Track how water quality changes over time
- Identify which areas need environmental protection
- Make informed decisions about water resource management

---

## Understanding Databases

### What is a Database?

Think of a database as an organized filing cabinet for information. Instead of messy piles of paper, everything is stored in neat, structured **tables**.

### What is SQL?

**SQL** (Structured Query Language) is the language we use to ask questions of the database. It's like asking a librarian to find specific books, but for data.

### What is SQLite?

**SQLite** is the database software included with this package. It's:
- A single file database (washington_water.db) - no server needed!
- Built into Python - no separate installation required
- Fast and lightweight - perfect for learning and analysis
- Used in phones, browsers, and countless applications worldwide
- Free and open-source

**Why SQLite for students?**
- Works immediately on Windows, macOS, and Linux
- No server configuration or passwords
- Easy to share - just copy the .db file
- Professional-grade SQL support for learning

**Official Site**: https://www.sqlite.org/

---

## Database Structure

Our database has **three tables** that are connected to each other:

### Visual Relationship

```
┌─────────────────┐
│   parameters    │  ← Defines what's being measured
│─────────────────│
│ code            │  (Primary Key: uniquely identifies each parameter)
│ short_name      │
│ long_name       │
└─────────────────┘
         ↑
         │ (referenced by param_code)
         │
┌─────────────────┐      ┌─────────────────┐
│    stations     │      │     results     │  ← The actual measurements
│─────────────────│      │─────────────────│
│ agency          │  ←───│ station_id      │  (references stations)
│ station_id      │      │ param_code      │  (references parameters)
│ station_name    │      │ start_date      │
│ county          │      │ start_time      │
│ latitude        │      │ result_value    │
│ longitude       │      │ agency          │
│ (+ more...)     │      │ huc             │
└─────────────────┘      │ sample_depth    │
    (Primary Key)        └─────────────────┘
```

### Table 1: `parameters`

This table defines **what** is being measured.

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `code` | VARCHAR(10) | Unique code for the parameter (Primary Key) | `00010` |
| `short_name` | VARCHAR(50) | Abbreviated name | `WATER TEMP CENT` |
| `long_name` | VARCHAR(255) | Full descriptive name | `TEMPERATURE, WATER (DEGREES CENTIGRADE)` |

**Total Rows**: 1,587 different parameters

**Common Parameters**:
- `00010` - Water Temperature (most measured: 290,975 times)
- `00301` - Dissolved Oxygen (% saturation)
- `00095` - Specific Conductance
- `00300` - Dissolved Oxygen (mg/L)
- `00400` - pH level
- `00070` - Turbidity (water clarity)

### Table 2: `stations`

This table defines **where** samples were taken.

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `agency` | VARCHAR(50) | Organization that operates the station | `USEPA REGION 10` |
| `station_id` | VARCHAR(50) | Unique identifier (Primary Key) | `543017` |
| `station_name` | TEXT | Descriptive name | `PALOUSE RIVER AT HOOPER` |
| `agency_name` | VARCHAR(100) | Full agency name | `US Environmental Protection Agency` |
| `state` | VARCHAR(50) | Always "Washington" for this dataset | `Washington` |
| `county` | VARCHAR(50) | County name | `Adams` |
| `latitude` | DECIMAL(10,6) | GPS coordinate (North-South) | `46.758889` |
| `longitude` | DECIMAL(10,6) | GPS coordinate (East-West) | `-118.147222` |
| `huc` | VARCHAR(20) | Hydrologic Unit Code (watershed ID) | `17060108` |
| `station_type` | VARCHAR(100) | Type of water body | `/TYPA/AMBNT/STREAM` |
| `description` | TEXT | Additional notes | `none` or detailed description |

**Total Rows**: 6,892 monitoring stations

**Top Counties by Measurements**:
1. King County - Most urban monitoring
2. Spokane County - Eastern Washington
3. Pierce County - Tacoma area
(And many more - data covers all 39 WA counties)

### Table 3: `results`

This table contains the **actual measurements** - the heart of the database!

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `id` | SERIAL | Auto-generated unique ID | `1`, `2`, `3`... |
| `agency` | VARCHAR(50) | Who took the sample | `1119C050` |
| `station_id` | VARCHAR(50) | **References stations.station_id** | `543017` |
| `param_code` | VARCHAR(10) | **References parameters.code** | `00010` |
| `start_date` | DATE | When the sample was taken | `1969-03-10` |
| `start_time` | VARCHAR(10) | Time of sampling (see note below) | `1330` or `2500` |
| `result_value` | VARCHAR(50) | The measured value (often scientific notation) | `300000E-5` = 3.0 |
| `huc` | VARCHAR(20) | Watershed code | `17060108` |
| `sample_depth` | VARCHAR(20) | How deep the sample was taken | `210` (feet) or empty |

**Total Rows**: 3,178,425 measurements!

**Important Note about `start_time`**:
This field uses special codes! See [TIME_CODES.md](TIME_CODES.md) for details.
- Valid times: `1330` = 1:30 PM, `0800` = 8:00 AM
- Special codes: `2500` = "time not recorded" (13.8% of data!)
- `0001` = "unknown time" (7.1% of data)

### Understanding Foreign Keys and the "Code" Approach

**Why use codes instead of full names?**

Imagine if every one of the 3,178,425 measurement records stored the full text:
- ❌ `"TEMPERATURE, WATER (DEGREES CENTIGRADE)"` (44 characters × 3.1M = 136 MB just for this!)
- ✅ `"00010"` (5 characters × 3.1M = 15 MB)

**That's a 9x savings in storage!** And this was designed in the 1960s when storage was expensive.

**How it works:**

```
Result Record #1,234,567:
  param_code = "00010"  ←── This is the "foreign key"
                            It points to the parameters table

To find out what "00010" means:
  SELECT * FROM parameters WHERE code = '00010';

  Returns: "TEMPERATURE, WATER (DEGREES CENTIGRADE)"
```

**Foreign keys** are like cross-references in a book - they connect information across tables without duplicating it.

**Benefits of this approach:**
- **Space efficient:** Store codes once, reference them millions of times
- **Consistency:** Can't accidentally misspell "TEMPERATURE" differently in different records
- **Faster queries:** Comparing "00010" = "00010" is faster than comparing long strings
- **Easy updates:** Change the description in ONE place, affects all references

**Trade-offs:**
- **Less readable:** You see codes instead of descriptions
- **Requires JOINs:** Must combine tables to get human-readable results
- **Learning curve:** Need to understand table relationships

**Real-world examples of this pattern:**
- ZIP codes (instead of storing full city/state each time)
- Airport codes (SEA, JFK, ORD instead of full names)
- Product barcodes (UPC codes)
- Credit card types (VISA = 4, MasterCard = 5)

### Understanding the Time Code "Hack" ⚠️

**Notice something odd about `start_time`?**

This field contains some "illegal" values that can't actually be times:

- `2500` = This would be 25:00 (hour 25 doesn't exist!)
- `0001` = This means 00:01 (12:01 AM) OR "unknown time"

**This is a database hack from the 1960s-1970s:**

In old systems, programmers didn't have modern features like NULL values or separate indicator columns. So they used "magic numbers" - impossible values that carry special meaning:

```
start_time = "2500"  →  Actually means: "noon (but exact time not recorded)"
start_time = "0001"  →  Actually means: "we don't know the time"
```

**Why this is considered a "hack" (not best practice):**

1. **Overloading values:** One column stores both real times AND special codes
2. **Not type-safe:** Database thinks it's storing times, but some aren't
3. **Fragile:** New developer might not know "2500" is special
4. **Hard to query:** Need special WHERE clauses to filter out magic numbers

**How modern databases would do this:**

```sql
-- Modern approach:
start_time: TIME or NULL
time_precision: ENUM('exact', 'approximate', 'unknown')
time_quality_code: VARCHAR(10) -- separate column for special meanings
```

**Why you should know this:**

You'll encounter "magic numbers" in legacy datasets from government, healthcare, and old corporate systems. Examples:
- `-999` or `-9999` = "missing data"
- `99` in age field = "unknown age"
- `00000` in ZIP code = "military/overseas address"
- `9999-12-31` in dates = "ongoing/no end date"

**When working with old data:**
1. **Read the documentation** (like TIME_CODES.md) to learn magic values
2. **Filter them out** in queries if doing calculations
3. **Don't create new ones** in your own work - use NULL or enums instead
4. **Document them clearly** if you must use them

See [TIME_CODES.md](TIME_CODES.md) for the complete list of special time codes in this dataset.

---

## Example SQL Queries

### Connecting to the Database

**Opening the database from the command line:**

```bash
# Navigate to the package folder (where washington_water.db is located)
# Windows (PowerShell):
cd C:\Users\YourName\Documents\washington_water_quality

# macOS/Linux:
cd ~/Documents/washington_water_quality

# Open the database with sqlite3:
sqlite3 washington_water.db
```

Once connected, you'll see a prompt like: `sqlite>`

**💡 Pro tips for a better experience:**
- **Use up/down arrows** to recall previous commands (command history works!)
- **Press TAB** for auto-completion of table names (on some systems)
- **Type `.help`** to see all available dot-commands
- **Use `.mode column` and `.headers on`** for prettier output (recommended!)

**Can't stand the command line?**
- Install **DB Browser for SQLite** (free GUI): https://sqlitebrowser.org/
- Or use a **VSCode extension**: Search "SQLite" in VSCode extensions

### Working with sqlite3 - Essential Commands

Before running queries, here are essential **sqlite3 dot-commands** (they start with `.`):

**🎯 First time? Run these setup commands:**
```sql
-- Make output look nice (run these first!)
.mode column
.headers on
.timer on

-- Now you're ready to query!
```

**📋 Exploration commands:**
```sql
-- List all tables
.tables

-- Show table structure (columns and types)
.schema parameters
.schema stations
.schema results

-- Show ALL table structures
.schema

-- Execute SQL from a file
.read myquery.sql

-- Save query results to a file
.output results.txt
SELECT * FROM parameters LIMIT 10;
.output stdout  -- Stop writing to file, resume screen output

-- Export query results to CSV
.mode csv
.output parameters_export.csv
SELECT * FROM parameters;
.output stdout
.mode column  -- Switch back to column mode

-- See current settings
.show

-- Show query execution time
.timer on
SELECT COUNT(*) FROM results;
-- Now shows execution time after each query

-- Quit sqlite3
.quit
-- Or press Ctrl+D
```

**Useful sqlite3 Command-Line Options**:

```bash
# Run a single query and exit
sqlite3 washington_water.db "SELECT COUNT(*) FROM results;"

# Run a query from a file
sqlite3 washington_water.db < myquery.sql

# Output as CSV
sqlite3 -csv washington_water.db "SELECT * FROM parameters;" > params.csv

# Output as HTML table
sqlite3 -html washington_water.db "SELECT * FROM parameters LIMIT 5;" > table.html

# Columnar output with headers
sqlite3 -column -header washington_water.db "SELECT * FROM parameters LIMIT 5;"
```

**SQL Statement Formatting Tips**:

- SQL is **not** case-sensitive: `SELECT` = `select` = `SeLeCt`
- Convention: Write SQL keywords in UPPERCASE for readability
- Every SQL statement must end with a semicolon `;`
- You can split long queries across multiple lines - sqlite3 waits for the `;`
- Use `--` for single-line comments
- Use `/* multi-line comments */`
- String values use **single quotes**: `WHERE county = 'King'`
- Numbers don't need quotes: `WHERE count > 100`

---

## ⚠️ IMPORTANT: Always Use LIMIT When Exploring Data!

**This database has 3.1 MILLION rows!** Without `LIMIT`, a query like `SELECT * FROM results;` will try to show ALL 3+ million measurements and your screen will scroll forever.

**Best practices:**
```sql
-- ❌ DON'T DO THIS - will show 3 million rows!
SELECT * FROM results;

-- ✅ DO THIS - shows just 10 rows
SELECT * FROM results LIMIT 10;

-- ✅ Even better - add ORDER BY so you control which 10
SELECT * FROM results ORDER BY start_date DESC LIMIT 10;
```

**How LIMIT works:**
- `LIMIT 10` = show only the first 10 rows
- `LIMIT 100` = show only the first 100 rows
- Always use LIMIT when exploring, remove it only for `COUNT(*)` or when you know the result is small

**Pro tip:** Start with `LIMIT 5`, verify the query works, then increase if needed!

---

### Query 1: Count Everything

See how much data we have:

```sql
-- Count measurements
SELECT COUNT(*) FROM results;
-- Result: 3,178,425

-- Count stations
SELECT COUNT(*) FROM stations;
-- Result: 6,892

-- Count parameters
SELECT COUNT(*) FROM parameters;
-- Result: 1,587
```

**What this does**: `COUNT(*)` counts all rows in the table.

### Query 2: View Sample Data

Look at the first few rows:

```sql
-- See 5 parameters
SELECT * FROM parameters LIMIT 5;

-- See 5 stations
SELECT * FROM stations LIMIT 5;

-- See 5 results
SELECT * FROM results LIMIT 5;
```

**What this does**:
- `SELECT *` means "show me all columns"
- `LIMIT 5` means "only show 5 rows"

### Query 3: Find a Specific Parameter

```sql
-- Find information about pH
SELECT code, short_name, long_name
FROM parameters
WHERE code = '00400';
```

**Result**:
```
 code  | short_name |         long_name
-------+------------+---------------------------
 00400 | PH  SU     | PH (STANDARD UNITS)
```

**What this does**:
- `SELECT code, short_name, long_name` - only show these 3 columns
- `FROM parameters` - look in the parameters table
- `WHERE code = '00400'` - only show rows where code equals '00400'

### Query 4: Find Stations in a County

```sql
-- Find all monitoring stations in King County
SELECT station_id, station_name, latitude, longitude
FROM stations
WHERE county = 'King'
ORDER BY station_name
LIMIT 10;
```

**What this does**:
- `WHERE county = 'King'` - filter to only King County
- `ORDER BY station_name` - sort alphabetically by name
- `LIMIT 10` - show first 10 results

### Query 5: Join Tables Together

This is where it gets powerful! Combine information from multiple tables:

```sql
-- Show measurement details (combining all 3 tables)
SELECT
    r.start_date,
    s.station_name,
    s.county,
    p.short_name AS parameter,
    r.result_value
FROM results r
JOIN stations s ON r.station_id = s.station_id
JOIN parameters p ON r.param_code = p.code
WHERE s.county = 'Adams'
  AND p.code = '00010'  -- Water temperature
  AND r.start_date >= '2000-01-01'
ORDER BY r.start_date DESC
LIMIT 10;
```

**What this does**:
- `FROM results r` - start with results table (use 'r' as shorthand)
- `JOIN stations s ON r.station_id = s.station_id` - connect to stations table by matching IDs
- `JOIN parameters p ON r.param_code = p.code` - connect to parameters table
- Multiple `WHERE` conditions filter the data
- `ORDER BY r.start_date DESC` - newest dates first
- Shows station name, county, what was measured, and the value

### Query 6: Aggregate Data (Statistics)

Calculate statistics across many measurements:

```sql
-- Average pH by county (for readings since 2000)
SELECT
    s.county,
    COUNT(*) as measurement_count,
    ROUND(AVG(CAST(r.result_value AS FLOAT)), 2) as avg_ph,
    MIN(CAST(r.result_value AS FLOAT)) as min_ph,
    MAX(CAST(r.result_value AS FLOAT)) as max_ph
FROM results r
JOIN stations s ON r.station_id = s.station_id
WHERE r.param_code = '00400'  -- pH
  AND r.result_value ~ '^[0-9.Ee+-]+$'  -- Only numeric values
  AND r.start_date >= '2000-01-01'
GROUP BY s.county
HAVING COUNT(*) > 100  -- Only counties with at least 100 measurements
ORDER BY measurement_count DESC
LIMIT 10;
```

**What this does**:
- `COUNT(*)` - count how many measurements
- `AVG(...)` - calculate average
- `MIN(...)` and `MAX(...)` - find minimum and maximum values
- `CAST(... AS FLOAT)` - convert text to number for calculations
- `GROUP BY s.county` - group results by county (one row per county)
- `HAVING COUNT(*) > 100` - filter groups (like WHERE, but for aggregates)

**Result example**:
```
   county    | measurement_count | avg_ph | min_ph | max_ph
-------------+-------------------+--------+--------+--------
King         | 5234              | 7.23   | 4.5    | 9.1
Spokane      | 3421              | 7.45   | 5.2    | 8.9
```

### Query 7: Time-Based Analysis

See how measurements change over time:

```sql
-- Temperature measurements per year
SELECT
    EXTRACT(YEAR FROM start_date) as year,
    COUNT(*) as num_measurements,
    COUNT(DISTINCT station_id) as num_stations
FROM results
WHERE param_code = '00010'  -- Water temperature
  AND start_date IS NOT NULL
GROUP BY year
ORDER BY year;
```

**What this does**:
- `EXTRACT(YEAR FROM start_date)` - pull out just the year from the date
- `COUNT(DISTINCT station_id)` - count unique stations (not duplicates)
- `GROUP BY year` - one row per year
- Shows how monitoring activity changed over time

---

## Using the Analysis Script

The Python script `analyze_water_quality.py` automates complex queries and creates visualizations.

### What It Does

1. **Verifies the database schema** - checks that all tables and columns exist
2. **Finds the most measured parameters** - identifies the top 6
3. **Creates time-series plots** - shows how parameters changed over decades
4. **Creates county comparison charts** - geographic distribution of monitoring
5. **Creates temporal coverage plots** - monitoring activity over time

### Running the Script

```bash
# Make sure you have the required packages
pip install -r requirements.txt

# Run the analysis
python3 analyze_water_quality.py
```

### Output Files

The script generates three PNG image files:

1. **water_quality_analysis.png** - 6 subplots showing top parameters over time
2. **county_comparison.png** - Bar charts comparing counties
3. **temporal_coverage.png** - Monitoring activity by year

### Reading the Graphs

**Time Series Plots**:
- X-axis = time (dates)
- Y-axis = measured value
- Each point = monthly average
- Trends show how water quality changed over decades

**County Comparison**:
- Longer bars = more measurements or stations
- Shows which counties have the most comprehensive monitoring

**Temporal Coverage**:
- Shows when monitoring was most active
- Helps identify gaps in historical data

---

## Learning Resources

### SQL & Databases

**Beginner Tutorials**:
- [SQLite Tutorial](https://www.sqlitetutorial.net/) - Comprehensive SQLite guide
- [W3Schools SQL Tutorial](https://www.w3schools.com/sql/) - Interactive exercises
- [SQLBolt](https://sqlbolt.com/) - Learn by doing (interactive lessons)
- [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/) - Practical examples

**SQLite Official Documentation**:
- [SQLite Documentation](https://www.sqlite.org/docs.html) - Official reference
- [SQLite Command Line](https://www.sqlite.org/cli.html) - sqlite3 command guide

**Video Courses**:
- [Khan Academy - Intro to SQL](https://www.khanacademy.org/computing/computer-programming/sql) - Free, visual

**Note**: Most SQL tutorials work with any database (PostgreSQL, MySQL, SQLite). The syntax is 99% the same!

### Python Programming

**Beginner Resources**:
- [Python.org Official Tutorial](https://docs.python.org/3/tutorial/) - Start here if you remember some Python
- [Real Python](https://realpython.com/) - Excellent tutorials at all levels
- [Python for Everybody](https://www.py4e.com/) - Free book and videos
- [Automate the Boring Stuff](https://automatetheboringstuff.com/) - Practical Python projects

**Python Package Documentation** (used in our script):
- [pandas](https://pandas.pydata.org/docs/) - Data analysis library
- [matplotlib](https://matplotlib.org/stable/contents.html) - Plotting library
- [sqlite3](https://docs.python.org/3/library/sqlite3.html) - SQLite adapter (built into Python)
- [seaborn](https://seaborn.pydata.org/) - Statistical visualization (built on matplotlib)

**Interactive Learning**:
- [DataCamp](https://www.datacamp.com/) - Interactive Python/data science courses (some free)
- [Kaggle Learn](https://www.kaggle.com/learn) - Free mini-courses on Python, pandas, visualization

### Data Visualization

**Learning to Make Good Graphs**:
- [From Data to Viz](https://www.data-to-viz.com/) - Choose the right chart type
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html) - Official matplotlib guides
- [Python Graph Gallery](https://www.python-graph-gallery.com/) - Code examples for every chart type
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html) - Beautiful statistical plots

**Design Principles**:
- [Storytelling with Data](https://www.storytellingwithdata.com/blog) - Blog about effective visualization
- [Edward Tufte's Principles](https://www.edwardtufte.com/tufte/) - Classic data visualization theory

### Water Quality Data & Environmental Science

**Understanding Water Quality Parameters**:
- [USGS Water Quality Information](https://www.usgs.gov/mission-areas/water-resources/science/water-quality) - What parameters mean
- [EPA Water Quality Portal](https://www.waterqualitydata.us/) - National water data
- [Water Quality Parameters Explained](https://www.fondriest.com/environmental-measurements/parameters/) - Detailed explanations

**STORET/WQX System** (where this data comes from):
- [EPA STORET](https://www.epa.gov/waterdata/storage-and-retrieval-and-water-quality-exchange) - Data system overview
- [WQX Web](https://www.epa.gov/waterdata/water-quality-data-upload-wqx) - Modern water quality exchange
- [Water Quality Portal User Guide](https://www.waterqualitydata.us/portal_userguide/) - How to use national data

**Washington State Specific**:
- [WA Dept of Ecology Water Quality](https://ecology.wa.gov/Water-Shorelines/Water-quality) - State programs
- [WA Water Quality Atlas](https://fortress.wa.gov/ecy/eap/marinewq/mwdataset.asp) - Marine water quality
- [River and Stream Monitoring](https://ecology.wa.gov/Research-Data/Monitoring-assessment/River-stream-monitoring) - Current monitoring programs

### Database Design & Best Practices

**Understanding Relational Databases**:
- [Database Design for Mere Mortals](https://www.amazon.com/Database-Design-Mere-Mortals-Hands/dp/0321884493) - Book, very accessible
- [What is a Relational Database?](https://www.oracle.com/database/what-is-a-relational-database/) - Conceptual overview
- [Normalization Explained](https://www.essentialsql.com/get-ready-to-learn-sql-database-normalization-explained-in-simple-english/) - Why we use multiple tables

### Command Line & Tools

**If You're New to the Terminal**:
- [Command Line Crash Course](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line) - MDN tutorial
- [Linux Command Line Basics](https://ubuntu.com/tutorials/command-line-for-beginners) - Ubuntu tutorial
- [Bash Scripting Tutorial](https://linuxconfig.org/bash-scripting-tutorial-for-beginners) - Shell scripts

**Git & Version Control** (for tracking your own analysis code):
- [Git Handbook](https://guides.github.com/introduction/git-handbook/) - GitHub's intro
- [Learn Git Branching](https://learngitbranching.js.org/) - Interactive visual tutorial

---

## Quick Reference: Common SQL Commands

### Viewing Data
```sql
SELECT * FROM table_name;              -- See everything
SELECT column1, column2 FROM table;    -- See specific columns
SELECT * FROM table LIMIT 10;          -- See first 10 rows
```

### Filtering
```sql
WHERE column = 'value'                 -- Exact match
WHERE column LIKE '%text%'             -- Contains 'text'
WHERE column > 100                     -- Greater than
WHERE date >= '2000-01-01'             -- Date comparison
WHERE column IS NULL                   -- Missing values
WHERE column IS NOT NULL               -- Has a value
```

### Sorting
```sql
ORDER BY column ASC                    -- Ascending (A to Z, 0 to 9)
ORDER BY column DESC                   -- Descending (Z to A, 9 to 0)
ORDER BY column1, column2              -- Sort by multiple columns
```

### Aggregation
```sql
COUNT(*)                               -- Count rows
COUNT(DISTINCT column)                 -- Count unique values
AVG(column)                            -- Average
SUM(column)                            -- Total
MIN(column)                            -- Minimum
MAX(column)                            -- Maximum
GROUP BY column                        -- Group for aggregates
```

### Joining Tables
```sql
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.foreign_id
```

---

## Practice Exercises

### Exercise 1: Explore Parameters
**Goal**: Find parameters related to temperature

```sql
SELECT code, short_name, long_name
FROM parameters
WHERE long_name LIKE '%TEMPERATURE%'
ORDER BY short_name;
```

**Try This**: Modify the query to find parameters about 'OXYGEN' or 'NITROGEN'

### Exercise 2: County Statistics
**Goal**: Count how many stations are in each county

```sql
SELECT county, COUNT(*) as station_count
FROM stations
WHERE county IS NOT NULL
GROUP BY county
ORDER BY station_count DESC;
```

**Try This**: Find which agency operates the most stations

### Exercise 3: Recent Measurements
**Goal**: Find temperature measurements from the last 5 years in the database

```sql
SELECT
    start_date,
    result_value,
    station_id
FROM results
WHERE param_code = '00010'
  AND start_date >= '1995-01-01'
ORDER BY start_date DESC
LIMIT 20;
```

**Try This**: Change the parameter code to pH (00400) or conductivity (00095)

### Exercise 4: Your First Join
**Goal**: Show station names along with measurements

```sql
SELECT
    s.station_name,
    s.county,
    r.start_date,
    r.result_value
FROM results r
JOIN stations s ON r.station_id = s.station_id
WHERE r.param_code = '00010'
  AND s.county = 'King'
LIMIT 10;
```

**Try This**: Change to your favorite county, or add the parameter name by joining to parameters table

---

## Getting Help

### If SQL Queries Don't Work

1. **Read the error message** - SQLite gives helpful hints
2. **Check for typos** - SQL is case-insensitive but spelling matters
3. **Use semicolons** - Every SQL statement ends with `;`
4. **Quote text values** - Use single quotes: `WHERE county = 'King'`
5. **Don't quote numbers** - Use: `WHERE value > 100` not `'100'`

### If Python Script Fails

1. **Check you're in the right directory** - Navigate to the package folder containing `washington_water.db`
2. **Verify packages installed** - `pip install -r Python_Scripts/requirements.txt`
3. **Check database file exists** - Look for `washington_water.db` (371 MB file)
4. **Read the error traceback** - Last line usually tells you what went wrong

### If Graphs Look Weird

1. **Check your data** - Run the SQL query manually to see what data you're plotting
2. **Look for NULL values** - Empty data creates gaps in plots
3. **Check data types** - Make sure numbers are numbers, not text
4. **Adjust date ranges** - Some parameters only have data in certain years

---

## Next Steps

Once you're comfortable with the basics:

1. **Write your own queries** - Answer questions you're curious about
2. **Modify the Python script** - Add your own visualizations
3. **Export data to CSV** - Use SQL `COPY` or pandas `to_csv()`
4. **Combine with other datasets** - GIS data, demographic data, etc.
5. **Build a web dashboard** - Tools like Streamlit or Flask
6. **Perform statistical analysis** - Trend detection, correlation, forecasting

---

## Summary

You now have access to a rich environmental dataset with:
- **3.1+ million measurements** across decades
- **Geographic coverage** of all Washington State
- **Diverse parameters** measuring water quality
- **Tools to analyze and visualize** the data

The combination of SQL for querying and Python for analysis is extremely powerful and widely used in data science, environmental science, and many other fields.

Start with simple queries, experiment, and gradually build up to more complex analyses. Every expert started as a beginner!

**Happy exploring! 🌊📊**
