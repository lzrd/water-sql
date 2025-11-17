# Quick Start Guide - Water Quality Analysis

**Time needed:** 15-20 minutes
**Skill level:** Beginner (no prior experience needed)

---

## ⚡ Fast Track (3 Steps)

### Step 1: Setup (5 minutes)

1. Extract this package to your Desktop or Documents folder
2. Install VSCode (if you don't have it): https://code.visualstudio.com/
3. Open the extracted folder in VSCode:
   - Right-click the folder → "Open with Code"
   - Or: Launch VSCode → File → Open Folder

### Step 2: Install Python Packages (5 minutes)

1. Open a terminal in VSCode:
   - Press **Ctrl+`** (backtick key, usually above Tab)
   - Or: View menu → Terminal

2. Copy and paste this command:

**Windows (PowerShell):**
```powershell
pip install -r .\Python_Scripts\requirements.txt
```

**macOS/Linux:**
```bash
pip install -r Python_Scripts/requirements.txt
```

3. Wait for "Successfully installed..." message
   - **Note:** If you see a pip upgrade warning, you can safely ignore it!
   - The packages will still install correctly

**Troubleshooting:**
- If you see "pip was not found", you need to install Python first
- Visit: https://www.python.org/downloads/
- **Important for Windows:** Check "Add Python to PATH" during installation

### Step 3: Run the Analysis (10 minutes)

1. In the terminal, run this command:

**Windows (PowerShell):**
```powershell
python .\Python_Scripts\analyze_water_quality_sqlite.py
```

**Tip:** Type `python P` then press **TAB** - PowerShell will auto-complete the path for you!

**macOS/Linux:**
```bash
python3 Python_Scripts/analyze_water_quality_sqlite.py
```

2. **Be patient!** Wait 15-20 seconds while it loads the database
   - You'll see progress messages: "Opening database..." and "Verifying database structure..."
   - This is normal - it's reading 3.1 million measurements!

3. When it finishes, look for new PNG image files in your folder

**Troubleshooting:**
- **"python was not found"** on Windows? Try `py` instead of `python`
- **Script appears frozen?** Wait 20 seconds - it's working, just loading data
- **Still stuck?** See INSTALL.md for detailed platform-specific help

---

## 📊 What You'll See

The script analyzes **3.1 million** water quality measurements from Washington State and creates:

- **water_quality_analysis.png** - Temperature, dissolved oxygen, pH trends over time
- **county_comparison.png** - Statistics by county
- **temporal_coverage.png** - Data collection patterns

**How to view the results:**

1. Look in the VSCode file explorer (left sidebar)
2. Click on any *.png file to view it
3. Scroll up in the terminal to see printed statistics

---

## 🎯 What to Do Next

### Step 1: Examine the Visualizations (5-10 minutes)

**Open each PNG file and look carefully:**

1. **water_quality_analysis.png** - Three graphs showing trends over time:
   - What patterns do you see? (seasonal changes, long-term trends?)
   - Do values go up or down over the decades?
   - Are there any surprising spikes or drops?

2. **county_comparison.png** - Bar charts comparing counties:
   - Which counties have the most measurements?
   - Do some counties have higher/lower values than others?
   - Why might some counties be monitored more than others?

3. **temporal_coverage.png** - When data was collected:
   - Which time periods have the most data?
   - Are there gaps in the monitoring?
   - Has monitoring increased or decreased over time?

**Practice explaining out loud:** "I notice that..." or "This graph shows..."

### Step 2: Ask Questions About the Data (5 minutes)

Think like a data analyst preparing for an interview:

- **What questions could you answer** with this dataset?
  - Example: "Is water temperature increasing due to climate change?"
  - Example: "Which counties have the cleanest water?"

- **What additional data would help?**
  - Weather data? Population data? Industrial activity?

- **How could a utility use this information?**
  - Finding pollution sources? Planning monitoring stations? Public health?

**Write down 2-3 questions you're curious about!**

### Step 3: Explore the Database Structure (10-15 minutes)

**Open WATER_DATA.html in your browser** and read:

1. **The database diagram** (shows how tables relate)
   - Notice the 3 tables: parameters, stations, results
   - See how they connect using codes (param_code, station_id)
   - **Key insight:** Instead of storing "Temperature, water" 3 million times,
     we just store "00010" and look up the full name when needed!

2. **Understanding the "code" approach:**
   - **Why use codes?** Saves space, enforces consistency, faster queries
   - **Trade-off:** Less readable - need to join tables to understand data
   - **Real-world example:** Barcodes, ZIP codes, airport codes all work this way

3. **Time codes (the "hack" you should know about):**
   - Look at the TIME_CODES documentation
   - Notice: "2500" means noon (not 25:00 hours!)
   - "0001" means "unknown time" (not 12:01 AM!)
   - **This is a database hack:** Using invalid values to mean something special
   - **In modern programming:** We'd use NULL for unknown, or a separate column
   - **Why this matters:** You'll see this in old datasets - need to know how to handle it

### Step 4: Your First SQL Queries (Optional, 15-20 minutes)

**Ready to try querying the database directly?** Follow these step-by-step instructions:

#### Opening sqlite3 (First Time)

**1. Make sure you're in the right directory:**

In your VSCode terminal (Ctrl+` to open), you should see "package" in your path.
If not, navigate there:

**Windows (PowerShell):**
```powershell
cd path\to\package  # Wherever you extracted the files
```

**macOS/Linux:**
```bash
cd path/to/package  # Wherever you extracted the files
```

**2. Open the database file:**

**Windows (PowerShell):**
```powershell
sqlite3 washington_water.db
```

**macOS/Linux:**
```bash
sqlite3 washington_water.db
```

**What you should see:**
```
SQLite version 3.x.x
Enter ".help" for usage hints.
sqlite>
```

The `sqlite>` prompt means you're inside the database and ready to run commands!

**⚠️ IMPORTANT:** If you see **"sqlite3 was not found"**:

**Windows - Two Options (Choose One):**

---

### ✅ **EASIEST OPTION - Just Copy One File (Recommended for Beginners)**

1. Download from https://www.sqlite.org/download.html
   - Look for **"sqlite-tools-win-x64-*.zip"** (about 2 MB)
   - Click to download the zip file

2. **Extract the zip file:**
   - Find the downloaded zip in your Downloads folder
   - Right-click → "Extract All..." → Extract

3. **Copy sqlite3.exe to your package folder:**
   - Open the extracted folder
   - Find the file named `sqlite3.exe`
   - Copy it (Ctrl+C)
   - Paste it into your `package` folder (where `washington_water.db` is)

4. **That's it! Now run it with:**
   ```powershell
   .\sqlite3 washington_water.db
   ```
   (The `.\` tells PowerShell to run the program in the current folder)

---

### ⚙️ **ADVANCED OPTION - Install to PATH (Works from Anywhere)**

Only do this if you want `sqlite3` available in all folders on your computer:

1. Download and extract (same as above)

2. **Move files to a permanent location:**
   - Create folder `C:\sqlite`
   - Copy all extracted files there

3. **Add to Windows PATH:**
   - Open Start Menu → Search for "environment variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables..." button (bottom right)
   - Under "User variables", find and select "Path"
   - Click "Edit..." → Click "New"
   - Type `C:\sqlite`
   - Click "OK" on all windows

4. **Restart VSCode completely**
   - Close VSCode
   - Open it again
   - Open terminal (Ctrl+`)
   - Try `sqlite3 --version` to verify

---

**macOS:** Install with `brew install sqlite3` (requires Homebrew)

**Linux:** Install with `sudo apt install sqlite3` (Ubuntu/Debian)

**Don't want to deal with installation?** Skip to "GUI Alternative" below for a visual interface

#### Your First Commands (Copy and Paste These!)

**3. Set up nice formatting (one-time setup):**

Copy these three commands one at a time, paste into the sqlite> prompt, and press Enter:

```
.mode column
```
```
.headers on
```
```
.timer on
```

**What these do:**
- `.mode column` - Makes output lined up in columns (easy to read)
- `.headers on` - Shows column names at the top
- `.timer on` - Shows how fast queries run (cool for 3M rows!)

#### Answer Real Questions with SQL

Now let's answer some actual questions about the data! We'll walk through each step carefully.

---

**4. EXAMPLE QUESTION: "I want to look at turbidity in King County. How do I access the numbers?"**

Let's answer this step by step. Follow along and copy each query.

**Step 1: What tables do we have?**

```sql
.tables
```

**What you see:** `parameters  results  stations`

**What this means:**
- `parameters` = what measurements exist (temperature, turbidity, pH, etc.)
- `results` = the actual measurement numbers
- `stations` = where measurements were taken

---

**Step 2: Find the turbidity code**

The database uses codes instead of full names. Let's find turbidity:

```sql
SELECT code, long_name FROM parameters WHERE long_name LIKE '%turbidity%';
```

**What you see:**
```
code   long_name
00076  Turbidity, water, unfiltered, monochrome near infra-red LED light, 780-900 nm, detection angle 90 +-2.5 degrees, formazin nephelometric units (FNU)
00077  Turbidity, water, unfiltered, monochrome near infra-red LED ...
```

**What this means:** Turbidity is code **"00076"**. Remember this code!

**💡 What is turbidity?**
- **Turbidity** measures how cloudy or murky the water is
- Caused by suspended particles like:
  - Sediment (dirt, sand, silt)
  - Algae and microscopic organisms
  - Organic matter (decaying plants)
  - Pollution runoff

**How is it measured?**
The full name says: "monochrome near infra-red LED light, 780-900 nm, detection angle 90 +-2.5 degrees"

This means:
1. Shine an infrared light beam through the water
2. Measure how much light scatters at a 90-degree angle
3. More particles = more scattering = higher turbidity reading

**Units: FNU (Formazin Nephelometric Units)**
- **Low turbidity (0-1 FNU):** Crystal clear water (drinking water quality)
- **Medium turbidity (1-10 FNU):** Slightly cloudy (typical for rivers)
- **High turbidity (10-100+ FNU):** Very cloudy (after storms, erosion)

**Why it matters:**
- High turbidity can harm fish (clogs gills, blocks sunlight for plants)
- Indicates water quality problems (erosion, pollution, algae blooms)
- Drinking water standards require turbidity < 1 FNU

**Want to learn more?** See: https://www.usgs.gov/special-topics/water-science-school/science/turbidity-and-water

**How the query works:**
- `SELECT code, long_name` = show me just these two columns
- `FROM parameters` = from the parameters table
- `WHERE long_name LIKE '%turbidity%'` = only rows where the name contains "turbidity"
  - The `%` means "anything before/after" (so it finds "Turbidity, water..." etc.)

---

**Step 3: See what turbidity data looks like**

Let's peek at a few turbidity measurements:

```sql
SELECT * FROM results WHERE param_code = '00076' LIMIT 5;
```

**What you see:** Lots of columns including `station_id`, `param_code`, `start_date`, `result_value`

**Problem:** We see station IDs like "532028" but not the county name. We need to connect (JOIN) to the stations table!

**How this query works:**
- `SELECT *` = show me all columns
- `FROM results` = from the results table
- `WHERE param_code = '00076'` = only turbidity measurements
- `LIMIT 5` = just show 5 rows (not all 3 million!)

---

**Step 4: Connect results to stations to see county names**

This is called a JOIN - we're combining two tables:

```sql
SELECT
  results.start_date,
  results.result_value,
  stations.county,
  stations.station_name
FROM results
JOIN stations ON results.station_id = stations.station_id
WHERE results.param_code = '00076'
LIMIT 10;
```

**What you see:** Now you can see dates, values, counties, and station names together!

**How this query works:**
- `SELECT results.start_date, results.result_value, ...` = get columns from both tables
- `FROM results` = start with the results table
- `JOIN stations ON results.station_id = stations.station_id` = match up rows where station_id is the same in both tables
- `WHERE results.param_code = '00076'` = only turbidity
- `LIMIT 10` = show 10 measurements

---

**Step 5: FINALLY - Get turbidity numbers for King County only!**

Add one more filter to show only King County:

```sql
SELECT
  start_date,
  result_value,
  station_name
FROM results
JOIN stations USING(station_id)
WHERE param_code = '00076'
  AND county = 'King'
LIMIT 20;
```

**What you see:** Turbidity measurements ONLY from King County stations!

**Example output:**
```
start_date   result_value  station_name
2015-06-15   2.3          Puget Sound at Seattle
2015-07-01   1.8          Lake Washington
```

**How this query works:**
- Same as Step 4, but we added `AND county = 'King'`
- `USING(station_id)` is shorthand for `ON results.station_id = stations.station_id`

**🎉 SUCCESS! You're looking at turbidity numbers from King County!**

---

**Want to see more? Try changing the query:**
- Change `'King'` to `'Pierce'` or `'Snohomish'` to see other counties
- Change `'00076'` to `'00010'` to see temperature instead
- Change `LIMIT 20` to `LIMIT 50` to see more rows

---

#### 💾 IMPORTANT: Save Long Queries to Files!

**Typing long queries directly is frustrating!** One typo and you have to start over. Here's a better way:

**Step 1: Create a query file**

Open a new file in VSCode (File → New File, or Ctrl+N):

```sql
-- my_turbidity_query.sql
-- Get King County turbidity measurements

SELECT
  start_date,
  result_value,
  station_name
FROM results
JOIN stations USING(station_id)
WHERE param_code = '00076'
  AND county = 'King'
LIMIT 20;
```

**Step 2: Save it** (File → Save As...) in your `package` folder as `my_turbidity_query.sql`

**Step 3: Run it from sqlite3**

```sql
.read my_turbidity_query.sql
```

**That's it!** The query runs and you can edit the file as many times as you want.

**Why this is better:**
- ✅ **No more typos** - VSCode has spell checking and syntax highlighting
- ✅ **Edit and re-run** - Fix mistakes without retyping everything
- ✅ **Save your work** - Keep queries for later use
- ✅ **Add comments** - Explain what each query does
- ✅ **Share with others** - Send .sql files to colleagues

**Example workflow:**
1. Write query in VSCode → Save as `my_query.sql`
2. In sqlite3: `.read my_query.sql`
3. See a typo? Edit the file in VSCode, save
4. In sqlite3: Press **Up Arrow** to get `.read my_query.sql` again, press Enter
5. Query runs with your fixes!

**💡 Pro tip:** Keep a folder of your favorite queries:
```
package/
  ├── my_queries/
  │   ├── king_county_turbidity.sql
  │   ├── temperature_trends.sql
  │   └── county_comparison.sql
  └── washington_water.db
```

Then run them with: `.read my_queries/king_county_turbidity.sql`

---

**6. "What's the average turbidity in King County?"**

```sql
SELECT
  AVG(CAST(result_value AS REAL)) as avg_turbidity,
  COUNT(*) as total_measurements
FROM results
JOIN stations USING(station_id)
WHERE param_code = '00076'
  AND county = 'King'
  AND result_value NOT LIKE '%<%';  -- Exclude "less than" values
```

**Note:** We use `CAST(result_value AS REAL)` because values are stored as text. We exclude values like "<0.5" to get clean averages.

**7. "Which station in King County has the highest turbidity reading?"**

```sql
SELECT
  station_name,
  MAX(CAST(result_value AS REAL)) as highest_turbidity,
  start_date
FROM results
JOIN stations USING(station_id)
WHERE param_code = '00076'
  AND county = 'King'
  AND result_value NOT LIKE '%<%';
```

**8. "How many measurements does each county have?"**

```sql
SELECT county, COUNT(*) as measurements
FROM results
JOIN stations USING(station_id)
GROUP BY county
ORDER BY measurements DESC
LIMIT 10;
```

This shows which counties are monitored most heavily.

**9. "What was the water temperature trend over the years?"**

Let's look at average temperature by year:

```sql
SELECT
  SUBSTR(start_date, 1, 4) as year,
  AVG(CAST(result_value AS REAL)) as avg_temp
FROM results
WHERE param_code = '00010'  -- Temperature, water
  AND result_value NOT LIKE '%<%'
  AND CAST(result_value AS REAL) < 100  -- Remove outliers
GROUP BY year
ORDER BY year
LIMIT 20;
```

**What you're learning:** This shows average water temperature per year. Notice climate trends?

**10. Try your own question!**

Think of something you're curious about:
- "What's the pH level in my county?"
- "Which station has been collecting data the longest?"
- "How does dissolved oxygen vary by season?"

Use the queries above as templates and modify them!

**9. Export data to spreadsheets (CSV format)**

Want to analyze data in Excel, Google Sheets, or other spreadsheet software?

```sql
.mode csv
.output king_county_turbidity.csv
SELECT
  start_date,
  result_value,
  station_name
FROM results
JOIN stations USING(station_id)
WHERE param_code = '00076'
  AND county = 'King'
LIMIT 100;
.output stdout
.mode column
```

**What this does:**
1. `.mode csv` - Switch to CSV output format
2. `.output king_county_turbidity.csv` - Send output to a file
3. Run your query
4. `.output stdout` - Switch back to screen output
5. `.mode column` - Switch back to column format

**Now you can:**
- Open `king_county_turbidity.csv` in Excel or Google Sheets
- Create charts and graphs
- Do pivot tables and further analysis
- Share with others who prefer spreadsheets

**10. When you're done exploring:**

```
.quit
```

This exits sqlite3 and returns you to the normal terminal.

#### Save Your Settings (No More Retyping!)

Tired of typing `.mode column`, `.headers on`, `.timer on` every time? Save them!

**Create a config file that runs automatically:**

**Windows (PowerShell):**
```powershell
# Create .sqliterc in your home directory
echo ".mode column" > $HOME\.sqliterc
echo ".headers on" >> $HOME\.sqliterc
echo ".timer on" >> $HOME\.sqliterc
echo "-- SQLite settings loaded!" >> $HOME\.sqliterc
```

**macOS/Linux:**
```bash
# Create .sqliterc in your home directory
cat > ~/.sqliterc << 'EOF'
.mode column
.headers on
.timer on
-- SQLite settings loaded!
EOF
```

**Now every time you run sqlite3, these settings load automatically!**

You can also add your favorite queries as comments for quick reference:
```sql
-- Quick queries I use often:
-- SELECT * FROM parameters WHERE long_name LIKE '%turbidity%';
-- SELECT county, COUNT(*) FROM results JOIN stations USING(station_id) GROUP BY county;
```

**💡 Shortcut:** This package includes `sample.sqliterc` - just copy it!

**Windows:**
```powershell
copy sample.sqliterc $HOME\.sqliterc
```

**macOS/Linux:**
```bash
cp sample.sqliterc ~/.sqliterc
```

#### Using Spreadsheets to Query SQLite

**Excel and Google Sheets can connect directly to SQLite databases!**

**Option 1: Excel (Windows/Mac)**

1. **Install ODBC driver** (one time only):
   - Download from: http://www.ch-werner.de/sqliteodbc/
   - Install the SQLite ODBC driver

2. **Connect in Excel:**
   - Data → Get Data → From Other Sources → From ODBC
   - Choose "SQLite3 Datasource"
   - Browse to `washington_water.db`
   - Select tables to import

3. **Query with Power Query:**
   - Use Excel's Power Query editor
   - Write SQL queries directly
   - Results update when you refresh!

**Option 2: Google Sheets (via export)**

Google Sheets can't connect directly, but you can:

1. Export from sqlite3 to CSV (see step 9 above)
2. File → Import in Google Sheets
3. Now you have the data in Sheets!

**Option 3: LibreOffice Calc (Free, Works Great!)**

1. Open LibreOffice Calc
2. Sheet → Insert Sheet from file
3. Choose database type: "JDBC or ODBC"
4. Browse to washington_water.db
5. Write SQL queries in the database browser

**💡 Why use spreadsheets?**
- Familiar interface for non-programmers
- Easy pivot tables and charts
- Share results with colleagues
- No SQL knowledge needed (after initial query)

#### Quick Reference Card (for later)

Once you're comfortable, here are useful sqlite3 commands:

**Dot commands (start with `.`):**
```
.tables              -- List all tables
.schema results      -- Show how the results table is structured
.mode csv            -- Output as CSV (for Excel/Sheets)
.output file.csv     -- Save results to a file
.read myquery.sql    -- Run SQL commands from a file
.help                -- See all available commands
.quit                -- Exit sqlite3
```

**SQL queries (end with `;`):**
```sql
SELECT * FROM tablename LIMIT 10;           -- See first 10 rows
SELECT COUNT(*) FROM tablename;             -- Count total rows
SELECT DISTINCT column FROM table LIMIT 10; -- See unique values
```

**💡 Tips:**
- **Up/Down arrows** navigate through your command history
- **Tab key** doesn't autocomplete in sqlite3 (unlike your terminal)
- **Semicolon `;` is required** to end SQL queries
- **Dot commands don't need semicolons**
- **Always use LIMIT** when exploring (remember: 3.1 million rows!)
- **Save common queries** in .sql files and load with `.read myquery.sql`
- **Try the examples:** `.read example_queries.sql` (included in this package!)

#### GUI Alternative (If You Prefer Point-and-Click)

Don't like the command line? Try these visual database browsers:

- **DB Browser for SQLite** (recommended for beginners): https://sqlitebrowser.org/
  - Free, works on Windows/macOS/Linux
  - Drag and drop to open `washington_water.db`
  - Click "Browse Data" to explore tables
  - Click "Execute SQL" to run queries

- **VSCode Extension**: Search for "SQLite" in VSCode Extensions
  - Right-click `washington_water.db` in file explorer → "Open Database"

### Step 5: Prepare for Interview Questions (15 minutes)

**Open INTERVIEW_PREP.md** and practice:
- How would you explain what each column means?
- How would you check if a surprising value is correct?
- What would you want to investigate further?

---

## 📚 Additional Learning Resources

**For Interview Preparation:**
- **INTERVIEW_PREP.md** - Practice questions matching typical data analyst interviews
- **WATER_DATA.html** - Complete database tutorial with SQL examples

**For Deeper Learning:**
- **analyze_water_quality_annotated.py** - Heavily commented code showing how the analysis works
- **TIME_CODES.md** - Understanding the time code "hack" used in this dataset

**For SQL Practice:**
- Try the example queries in WATER_DATA.html
- Modify them to answer your own questions
- Challenge: Find the hottest water temperature recorded!

---

## 🆘 Common Issues

| Problem | Solution |
|---------|----------|
| "pip was not found" | Install Python from python.org - check "Add to PATH" |
| "python was not found" (Windows) | Try `py` instead of `python` |
| pip upgrade warning | Safe to ignore - packages still install fine |
| Script appears frozen | Normal! Wait 15-20 seconds for database to load |
| Can't find PNG files | Check VSCode file explorer on left, or use `ls` command |
| Requirements install fails | See INSTALL.md for detailed troubleshooting |

---

## 💡 Tips for Success

1. **Use tab completion** - Type a few letters and press TAB for auto-complete
2. **Keep VSCode full-screen** - You can read .md files with Ctrl+Shift+V (preview mode)
3. **Use the built-in terminal** - No need to open separate command prompt
4. **Take your time** - Database loading takes 15-20 seconds, this is normal
5. **Explore the visualizations** - They're designed to show real water quality trends

---

**Questions?** See [INSTALL.md](INSTALL.md) for detailed instructions or [README.md](README.md) for project overview.
