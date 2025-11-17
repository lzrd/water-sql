# Browser SQL Console - User Guide

## Quick Start (30 Seconds!)

**No installation required!** Just open the HTML file:

### Windows
1. Navigate to extracted folder
2. **Double-click** `water_quality_browser.html`
3. Your default browser opens automatically

### macOS
1. Navigate to extracted folder in Finder
2. **Double-click** `water_quality_browser.html`
3. Safari/Chrome opens automatically

### Linux
1. Navigate to extracted folder
2. **Double-click** or run: `xdg-open water_quality_browser.html`
3. Your default browser opens

**That's it!** Wait 1-2 minutes for the database to load, then start querying!

---

## What You'll See

### Initial Load Screen
```
⏳ Loading database... This may take a minute (371 MB)
[========================================] 100%
```

**First time loading**: 1-2 minutes (downloads 371 MB database)
**Browser caches the database**, so subsequent loads are instant!

### Main Interface

Once loaded, you'll see:

```
┌─────────────────────────────────────────────────────────┐
│  🌊 Washington Water Quality Database                  │
│  Browser-Based SQL Console - No Installation Required! │
├─────────────────────────────────────────────────────────┤
│  ✅ Database loaded! Ready to query 3.1M+ measurements │
├──────────────────────┬──────────────────────────────────┤
│  Database Statistics │  SQL Query Editor                │
│  ─────────────────── │  ──────────────────              │
│  📊 3,178,425        │  Write SQL queries here:         │
│     Measurements     │  ┌────────────────────────────┐  │
│                      │  │ SELECT * FROM parameters   │  │
│  📍 6,892            │  │ LIMIT 10;                  │  │
│     Stations         │  └────────────────────────────┘  │
│                      │  [▶️ Execute Query] [🗑️ Clear]  │
│  🔬 1,587            │                                  │
│     Parameters       │  Results:                        │
│                      │  [Table with results appears]    │
│  💡 Example Queries  │                                  │
│  ───────────────     │                                  │
│  [View Parameters]   │                                  │
│  [King County]       │                                  │
│  [By County]         │                                  │
│  [Most Measured]     │                                  │
└──────────────────────┴──────────────────────────────────┘
```

---

## Using the Browser Console

### Method 1: Click Example Queries (Easiest!)

On the left side, click any example button:

**"View Parameters"** - See all water quality parameters
```sql
SELECT * FROM parameters LIMIT 10
```

**"King County Stations"** - Monitoring locations in King County
```sql
SELECT * FROM stations WHERE county = 'King' LIMIT 10
```

**"Stations by County"** - Count stations in each county
```sql
SELECT county, COUNT(*) as station_count
FROM stations
GROUP BY county
ORDER BY station_count DESC
LIMIT 10
```

**"Most Measured Parameters"** - What gets tested most?
```sql
SELECT p.short_name, COUNT(*) as measurements
FROM results r
JOIN parameters p ON r.param_code = p.code
GROUP BY p.code, p.short_name
ORDER BY measurements DESC
LIMIT 10
```

**"Measurements by Year"** - Historical trends
```sql
SELECT strftime('%Y', start_date) as year, COUNT(*) as count
FROM results
WHERE start_date IS NOT NULL
GROUP BY year
ORDER BY year
```

### Method 2: Write Your Own SQL

1. **Click in the SQL Editor** (right side, dark gray box)
2. **Type your SQL query**
3. **Click "▶️ Execute Query"**
4. **View results** in the table below

Example query:
```sql
SELECT
    s.county,
    COUNT(*) as measurement_count
FROM results r
JOIN stations s ON r.station_id = s.station_id
WHERE r.start_date >= '2000-01-01'
GROUP BY s.county
ORDER BY measurement_count DESC;
```

### Method 3: Export Results to CSV

1. **Run any query** to get results
2. **Click "📥 Export CSV"** button
3. **Save the file** to your computer
4. **Open in Excel, Google Sheets, or any spreadsheet program**

---

## Example Queries for Beginners

### See What's in the Database

**List all tables:**
```sql
SELECT name FROM sqlite_master WHERE type='table';
```

**Count everything:**
```sql
SELECT
    (SELECT COUNT(*) FROM results) as results,
    (SELECT COUNT(*) FROM stations) as stations,
    (SELECT COUNT(*) FROM parameters) as parameters;
```

### Explore Parameters

**Find parameters about temperature:**
```sql
SELECT code, short_name, long_name
FROM parameters
WHERE long_name LIKE '%TEMPERATURE%';
```

**Find parameters about pH:**
```sql
SELECT code, short_name, long_name
FROM parameters
WHERE long_name LIKE '%PH%';
```

### Explore Stations

**Stations with GPS coordinates:**
```sql
SELECT station_id, station_name, latitude, longitude, county
FROM stations
WHERE latitude IS NOT NULL
LIMIT 20;
```

**Stations by county (sorted by most stations):**
```sql
SELECT county, COUNT(*) as num_stations
FROM stations
WHERE county IS NOT NULL
GROUP BY county
ORDER BY num_stations DESC;
```

### Explore Measurements

**Recent measurements (for one station):**
```sql
SELECT start_date, param_code, result_value
FROM results
WHERE station_id = '543017'
ORDER BY start_date DESC
LIMIT 100;
```

**Temperature readings in 2000:**
```sql
SELECT start_date, result_value, station_id
FROM results
WHERE param_code = '00010'
  AND start_date LIKE '2000%'
LIMIT 50;
```

### Join Tables Together

**Get parameter names with measurements:**
```sql
SELECT
    p.short_name,
    r.start_date,
    r.result_value
FROM results r
JOIN parameters p ON r.param_code = p.code
WHERE r.station_id = '543017'
LIMIT 20;
```

**Complete information (all 3 tables!):**
```sql
SELECT
    s.station_name,
    s.county,
    p.short_name as parameter,
    r.start_date,
    r.result_value
FROM results r
JOIN stations s ON r.station_id = s.station_id
JOIN parameters p ON r.param_code = p.code
WHERE s.county = 'King'
  AND p.code = '00010'
LIMIT 20;
```

---

## Advanced Features

### Aggregate Functions

**Average pH by county:**
```sql
SELECT
    s.county,
    COUNT(*) as measurements,
    AVG(CAST(r.result_value AS FLOAT)) as avg_value
FROM results r
JOIN stations s ON r.station_id = s.station_id
WHERE r.param_code = '00400'  -- pH
  AND r.result_value NOT IN ('2500', '0001', '9999')
GROUP BY s.county
HAVING COUNT(*) > 100
ORDER BY measurements DESC;
```

### Time-Based Queries

**Measurements per year:**
```sql
SELECT
    strftime('%Y', start_date) as year,
    COUNT(*) as measurements
FROM results
WHERE start_date IS NOT NULL
GROUP BY year
ORDER BY year;
```

**Measurements per month in 2000:**
```sql
SELECT
    strftime('%Y-%m', start_date) as month,
    COUNT(*) as measurements
FROM results
WHERE start_date BETWEEN '2000-01-01' AND '2000-12-31'
GROUP BY month
ORDER BY month;
```

### Complex Filtering

**Find stations with most diverse parameter measurements:**
```sql
SELECT
    s.station_id,
    s.station_name,
    s.county,
    COUNT(DISTINCT r.param_code) as different_parameters
FROM results r
JOIN stations s ON r.station_id = s.station_id
GROUP BY s.station_id, s.station_name, s.county
ORDER BY different_parameters DESC
LIMIT 20;
```

---

## Troubleshooting

### Problem: "Database file not found"

**Cause**: The HTML file can't find `washington_water.db`

**Solution**:
- Make sure `water_quality_browser.html` and `washington_water.db` are in the **same folder**
- Both files must be from the extracted archive

### Problem: Database loads forever (stuck)

**Cause**: Browser might have insufficient memory

**Solutions**:
1. Close other browser tabs (frees memory)
2. Use a different browser (Chrome works best)
3. Restart browser and try again
4. Check you have 1 GB free RAM

### Problem: "SQL Error" when running query

**Cause**: SQL syntax error

**Solutions**:
1. Check for typos in table/column names
2. Use SQLite syntax (not MySQL or PostgreSQL)
3. Try one of the example queries first
4. See error message for hints

### Problem: Results table shows "NULL"

**Cause**: Data is actually NULL in the database

**Solution**: This is normal! Use `WHERE column IS NOT NULL` to filter:
```sql
SELECT * FROM stations WHERE latitude IS NOT NULL;
```

### Problem: Query is slow

**Causes & Solutions**:

**Too many results**:
```sql
-- Add LIMIT
SELECT * FROM results LIMIT 1000;
```

**Missing WHERE clause on big table**:
```sql
-- Filter the data
SELECT * FROM results
WHERE start_date >= '2000-01-01'
LIMIT 100;
```

**Complex JOIN**:
```sql
-- Add indexes help, but already created in this database
-- Just add LIMIT to reduce results
```

### Problem: Can't see all results

**Cause**: Display limited to 1000 rows for performance

**Solution**:
- Use CSV export to get all results
- Or use `LIMIT` and `OFFSET` to page through:
```sql
SELECT * FROM results LIMIT 1000;           -- First 1000
SELECT * FROM results LIMIT 1000 OFFSET 1000;  -- Next 1000
```

---

## Tips & Best Practices

### Start Small
```sql
-- Good: Test with LIMIT first
SELECT * FROM results LIMIT 10;

-- Bad: No LIMIT on huge table (3M rows!)
SELECT * FROM results;
```

### Use WHERE to Filter
```sql
-- Good: Filter before counting
SELECT COUNT(*) FROM results
WHERE start_date >= '2000-01-01';

-- Okay: Counts everything (takes longer)
SELECT COUNT(*) FROM results;
```

### Check Column Names First
```sql
-- See what columns are available
PRAGMA table_info(stations);
```

### Format for Readability
```sql
-- Easier to read
SELECT
    county,
    COUNT(*) as count
FROM stations
WHERE county IS NOT NULL
GROUP BY county;

-- Works but harder to read
SELECT county, COUNT(*) as count FROM stations WHERE county IS NOT NULL GROUP BY county;
```

---

## Keyboard Shortcuts

None built-in, but your browser has:

- **Ctrl+F** (Cmd+F on Mac) - Search in results table
- **Ctrl+A** - Select all text in SQL editor
- **Ctrl+C** - Copy selected text
- **Ctrl+V** - Paste into SQL editor

---

## Privacy & Security

### Your Data is Safe

✅ **Everything runs in your browser** - No data sent to any server
✅ **Works offline** - No internet connection needed after initial load
✅ **Read-only database** - You can't accidentally delete data
✅ **No tracking** - No analytics, cookies, or data collection

### Technical Details

- Database stored in browser memory (RAM)
- Queries executed by WebAssembly SQLite engine
- Results rendered in browser DOM
- CSV export uses client-side Blob API
- No external API calls except SQL.js library (CDN)

---

## Comparison: Browser vs Python vs Command Line

| Feature | Browser Console | Python Scripts | Command Line |
|---------|----------------|----------------|--------------|
| **Installation** | None! | Python + packages | sqlite3 |
| **Works on Chromebook** | ✅ Yes | ❌ No | ❌ No |
| **Visualizations** | ❌ No (SQL only) | ✅ Yes (graphs) | ❌ No |
| **Ease of Use** | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐ Medium | ⭐⭐ Hard |
| **SQL Learning** | ✅ Perfect | ✅ Yes | ✅ Yes |
| **Export CSV** | ✅ Yes | ✅ Yes | ⭐ Manual |
| **Offline** | ✅ Yes* | ✅ Yes | ✅ Yes |
| **Speed** | Fast | Fast | Fastest |
| **Best For** | Beginners, Quick queries | Data analysis | Advanced users |

*After initial database load

---

## Next Steps

1. ✅ Try the example queries
2. 📝 Modify them to learn SQL
3. 📚 Read [WATER_DATA.html](Documentation/WATER_DATA.html) for SQL tutorial
4. 🐍 Progress to Python scripts for visualizations
5. 💻 Try dual-mode script to compare PostgreSQL vs SQLite

---

## Additional Resources

**SQL Learning**:
- [SQLite Tutorial](https://www.sqlitetutorial.net/) - SQLite-specific syntax
- [SQL Teaching](https://www.sqlteaching.com/) - Interactive lessons
- [W3Schools SQL](https://www.w3schools.com/sql/) - Reference and examples

**SQLite Functions**:
- [Date/Time Functions](https://www.sqlite.org/lang_datefunc.html) - `strftime()`, etc.
- [Aggregate Functions](https://www.sqlite.org/lang_aggfunc.html) - `COUNT()`, `AVG()`, etc.
- [Core Functions](https://www.sqlite.org/lang_corefunc.html) - `CAST()`, `SUBSTR()`, etc.

**This Database**:
- [Database Guide](Documentation/WATER_DATA.html) - Complete tutorial
- [Time Codes](Documentation/TIME_CODES.html) - Understanding time values
- [README](README.html) - Package overview

---

## Frequently Asked Questions

**Q: Do I need internet to use this?**
A: Only for the initial load (to download SQL.js library and database). After that, works 100% offline.

**Q: Can I break the database?**
A: No! It's read-only. Even if you write `DELETE` or `DROP` queries, they'll fail safely.

**Q: How much disk space does this use?**
A: Zero! Database runs in RAM. When you close the browser, it's gone. (Files on disk stay safe)

**Q: Can I save my queries?**
A: Not built-in. Copy-paste them to a text file if you want to save them.

**Q: Why does it say "Showing first 1000 of X rows"?**
A: Performance! Rendering millions of rows would freeze the browser. Use CSV export for full results.

**Q: Can I use this for other SQLite databases?**
A: Yes! Replace `washington_water.db` with your database file. The HTML file works with any SQLite database.

**Q: Does this work on my phone/tablet?**
A: Technically yes, but the 371 MB download is large. Better on desktop/laptop with WiFi.

**Q: Can my instructor host this online?**
A: Yes! Upload both files to any web server. Students access via URL.

---

## Credits

- **Data**: EPA STORET Water Quality Database (Public Domain)
- **Technology**: [sql.js](https://github.com/sql-js/sql.js/) - SQLite compiled to WebAssembly
- **Design**: Custom HTML/CSS/JavaScript
- **Created for**: Educational purposes

---

**Happy querying! 🌊📊**
