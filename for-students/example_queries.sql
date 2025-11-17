-- Example SQL Queries for Washington Water Quality Database
-- Load this file in sqlite3 with: .read example_queries.sql
-- Or run specific queries by copying and pasting

-- ============================================================
-- SETUP: Uncomment these if you don't have .sqliterc
-- ============================================================
-- .mode column
-- .headers on
-- .timer on

-- ============================================================
-- 1. EXPLORE THE DATA
-- ============================================================

-- What tables exist?
.print "=== Available Tables ==="
.tables

-- What parameters are measured?
.print ""
.print "=== First 10 Water Quality Parameters ==="
SELECT code, short_name, long_name
FROM parameters
LIMIT 10;

-- How many total measurements?
.print ""
.print "=== Total Measurements ==="
SELECT COUNT(*) as total_measurements FROM results;

-- ============================================================
-- 2. FIND SPECIFIC PARAMETERS
-- ============================================================

-- Find turbidity codes
.print ""
.print "=== Turbidity Parameters ==="
SELECT code, long_name
FROM parameters
WHERE long_name LIKE '%turbidity%';

-- Find temperature codes
.print ""
.print "=== Temperature Parameters ==="
SELECT code, long_name
FROM parameters
WHERE long_name LIKE '%temperature%';

-- Find pH codes
.print ""
.print "=== pH Parameters ==="
SELECT code, long_name
FROM parameters
WHERE long_name LIKE '%pH%';

-- ============================================================
-- 3. COUNTY ANALYSIS
-- ============================================================

-- Which counties have the most data?
.print ""
.print "=== Top 10 Counties by Measurement Count ==="
SELECT
  county,
  COUNT(*) as measurements
FROM results
JOIN stations USING(station_id)
GROUP BY county
ORDER BY measurements DESC
LIMIT 10;

-- ============================================================
-- 4. TURBIDITY IN KING COUNTY
-- ============================================================

-- Get turbidity measurements for King County
.print ""
.print "=== King County Turbidity (First 20 measurements) ==="
SELECT
  start_date,
  result_value,
  station_name
FROM results
JOIN stations USING(station_id)
WHERE param_code = '00076'
  AND county = 'King'
LIMIT 20;

-- Average turbidity by county (excluding "<" values)
.print ""
.print "=== Average Turbidity by County ==="
SELECT
  county,
  ROUND(AVG(CAST(result_value AS REAL)), 2) as avg_turbidity,
  COUNT(*) as measurement_count
FROM results
JOIN stations USING(station_id)
WHERE param_code = '00076'
  AND result_value NOT LIKE '%<%'
  AND CAST(result_value AS REAL) > 0
GROUP BY county
HAVING measurement_count > 100
ORDER BY avg_turbidity DESC
LIMIT 10;

-- ============================================================
-- 5. TEMPERATURE TRENDS
-- ============================================================

-- Average water temperature by year
.print ""
.print "=== Average Water Temperature by Year ==="
SELECT
  SUBSTR(start_date, 1, 4) as year,
  ROUND(AVG(CAST(result_value AS REAL)), 2) as avg_temp_celsius,
  COUNT(*) as measurements
FROM results
WHERE param_code = '00010'  -- Temperature, water
  AND result_value NOT LIKE '%<%'
  AND CAST(result_value AS REAL) BETWEEN 0 AND 40
GROUP BY year
ORDER BY year
LIMIT 30;

-- ============================================================
-- 6. EXPORT EXAMPLES (uncomment to use)
-- ============================================================

-- Export King County turbidity to CSV:
-- .mode csv
-- .output king_county_turbidity.csv
-- SELECT
--   start_date,
--   result_value,
--   station_name,
--   latitude,
--   longitude
-- FROM results
-- JOIN stations USING(station_id)
-- WHERE param_code = '00076'
--   AND county = 'King'
-- LIMIT 1000;
-- .output stdout
-- .mode column
-- .print "✓ Exported to king_county_turbidity.csv"

-- ============================================================
-- 7. STATION INFORMATION
-- ============================================================

-- Find stations in a specific county
.print ""
.print "=== Monitoring Stations in King County ==="
SELECT
  station_id,
  station_name,
  latitude,
  longitude
FROM stations
WHERE county = 'King'
LIMIT 10;

.print ""
.print "=== Query Examples Complete ==="
.print "Modify these queries to explore the data!"
