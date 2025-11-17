# Spatial Analysis - Finding Patterns in Water Quality

**Time needed:** 45-60 minutes
**Prerequisites:** Complete QUICKSTART.md first

---

## Overview

Water quality doesn't happen in isolation - it's affected by geography! In this exercise, you'll:

1. **Find nearby stations** using distance calculations
2. **Visualize water quality on a map** to spot patterns
3. **Investigate real questions** like:
   - Where does turbidity come from? (erosion, construction, urban runoff?)
   - How does temperature vary near the coast vs. inland?
   - Does water quality change from upstream to downstream?
   - Are pollution sources clustered around certain areas?

---

## Part 1: Distance Queries with SQL

### The Problem

You want to find all monitoring stations within a certain distance of a location. For example:
- "Show me all stations within 10 miles of Seattle"
- "Find turbidity measurements near Mount Rainier"
- "Which stations are within 5 miles of a suspected pollution source?"

### The Haversine Formula

**The Challenge:** Earth approximates a sphere (it's actually an oblate spheroid), not a flat map!
You can't use simple Pythagorean theorem (√(x² + y²)) because latitude/longitude lines curve.

**The Solution:** The Haversine formula calculates distance between two points on a sphere.

**How it works (simplified):**
1. Convert latitude/longitude from degrees to radians
2. Calculate the angular distance between two points
3. Multiply by Earth's radius (3,959 miles or 6,371 km)
4. Result: Distance "as the crow flies"

**Why this matters:**
- Accurate for distances up to ~100 miles
- Works anywhere on Earth
- Standard method for GPS and mapping applications

**Want to understand the math?**
- Full explanation: https://en.wikipedia.org/wiki/Haversine_formula
- Interactive demo: https://www.movable-type.co.uk/scripts/latlong.html
- Video explanation: Search YouTube for "Haversine formula explained"

### Example: Find Stations Near Seattle

**Seattle coordinates:** 47.6062° N, 122.3321° W

```sql
-- Find all stations within 10 miles of downtown Seattle
SELECT
  station_name,
  county,
  latitude,
  longitude,
  -- Haversine formula for distance in miles
  (3959 * acos(
    cos(radians(47.6062)) * cos(radians(latitude))
    * cos(radians(longitude) - radians(-122.3321))
    + sin(radians(47.6062)) * sin(radians(latitude))
  )) AS distance_miles
FROM stations
WHERE distance_miles < 10
ORDER BY distance_miles;
```

**Breaking down the formula:**

```sql
-- Earth's radius in miles (use 6371 for kilometers)
3959 *

-- acos = inverse cosine (gives angle between points)
acos(
  -- Cosine of latitude differences, accounting for longitude convergence
  cos(radians(47.6062)) * cos(radians(latitude))
  * cos(radians(longitude) - radians(-122.3321))

  -- Plus sine of latitude differences
  + sin(radians(47.6062)) * sin(radians(latitude))
)
```

**Try it yourself:**

1. Open sqlite3: `sqlite3 washington_water.db`
2. Set up formatting: `.mode column` and `.headers on`
3. Run the query above

**What you'll see:** Stations sorted by distance from Seattle, showing which ones are closest.

### Save It as a Reusable Query File

Create a file you can edit and rerun with different locations:

**distance_from_point.sql:**
```sql
-- Find stations within X miles of a given point
-- INSTRUCTIONS:
--   1. Edit the three values below
--   2. Save the file
--   3. Run: .read distance_from_point.sql

-- EDIT THESE VALUES (then save the file):
.parameter set :lat1 47.6062      -- Latitude of your point
.parameter set :lon1 -122.3321    -- Longitude of your point
.parameter set :max_distance 10   -- Maximum distance in miles

-- Run the query (don't edit below this line):
SELECT
  station_name,
  county,
  latitude,
  longitude,
  ROUND((3959 * acos(
    cos(radians(:lat1)) * cos(radians(latitude))
    * cos(radians(longitude) - radians(:lon1))
    + sin(radians(:lat1)) * sin(radians(latitude))
  )), 2) AS distance_miles
FROM stations
WHERE distance_miles < :max_distance
ORDER BY distance_miles;
```

**How to use it:**

1. **Edit the file** in VSCode - change `:lat1`, `:lon1`, and `:max_distance` to your values
2. **Save the file** (Ctrl+S)
3. **Run in sqlite3:** `.read distance_from_point.sql`
4. **Want different coordinates?** Edit the file again and re-run!

**Example coordinates to try:**
- **Seattle:** lat1=47.6062, lon1=-122.3321
- **Spokane:** lat1=47.6588, lon1=-117.4260
- **Mount Rainier:** lat1=46.8523, lon1=-121.7603
- **Olympia:** lat1=47.0379, lon1=-122.9007

**💡 Pro tip:** Save multiple versions of this file with different names:
- `near_seattle.sql`
- `near_spokane.sql`
- `near_mt_rainier.sql`

### Real-World Applications

**Example 1: Investigating Turbidity Sources**

Question: "Where is high turbidity coming from near the Snoqualmie River?"

```sql
-- Find high turbidity measurements near Snoqualmie Falls
-- Snoqualmie Falls: 47.5421° N, 121.8379° W

SELECT
  s.station_name,
  s.latitude,
  s.longitude,
  r.start_date,
  r.result_value as turbidity,
  (3959 * acos(
    cos(radians(47.5421)) * cos(radians(s.latitude))
    * cos(radians(s.longitude) - radians(-121.8379))
    + sin(radians(47.5421)) * sin(radians(s.latitude))
  )) AS distance_miles
FROM results r
JOIN stations s USING(station_id)
WHERE r.param_code = '00076'  -- Turbidity
  AND distance_miles < 15
  AND CAST(r.result_value AS REAL) > 10  -- High turbidity only
ORDER BY distance_miles, r.start_date;
```

**What to look for:**
- Are upstream stations clearer than downstream?
- When did turbidity spike? (after storms? seasonal?)
- Are certain tributaries muddier than others?

**Example 2: Temperature Gradients**

Question: "How does water temperature change as you move inland from Puget Sound?"

```sql
-- Temperature near the coast (Seattle) vs. inland (Spokane)
-- Compare stations within 20 miles of each city

-- Coastal (Seattle area)
SELECT
  AVG(CAST(result_value AS REAL)) as avg_temp,
  'Coastal' as region
FROM results r
JOIN stations s USING(station_id)
WHERE param_code = '00010'  -- Temperature
  AND (3959 * acos(
    cos(radians(47.6062)) * cos(radians(s.latitude))
    * cos(radians(s.longitude) - radians(-122.3321))
    + sin(radians(47.6062)) * sin(radians(s.latitude))
  )) < 20
  AND result_value NOT LIKE '%<%'

UNION ALL

-- Inland (Spokane area)
SELECT
  AVG(CAST(result_value AS REAL)) as avg_temp,
  'Inland' as region
FROM results r
JOIN stations s USING(station_id)
WHERE param_code = '00010'  -- Temperature
  AND (3959 * acos(
    cos(radians(47.7751)) * cos(radians(s.latitude))
    * cos(radians(s.longitude) - radians(-117.2937))
    + sin(radians(47.7751)) * sin(radians(s.latitude))
  )) < 20
  AND result_value NOT LIKE '%<%';
```

---

## Part 2: Interactive Maps with Leaflet

Now let's visualize this data on a map!

### What You'll Build

An interactive web map showing:
- **Station locations** as colored circles
- **Circle size** = number of measurements
- **Circle color** = average turbidity (blue = clear, red = muddy)
- **Click stations** to see details
- **Zoom and pan** to explore

### Step 1: Export Data from SQLite

First, get the data you want to map:

```sql
-- Export King County turbidity data with coordinates
.mode csv
.output king_county_turbidity_map.csv

SELECT
  s.station_id,
  s.station_name,
  s.latitude,
  s.longitude,
  s.county,
  AVG(CAST(r.result_value AS REAL)) as avg_turbidity,
  COUNT(*) as measurement_count
FROM results r
JOIN stations s USING(station_id)
WHERE r.param_code = '00076'  -- Turbidity
  AND s.county = 'King'
  AND r.result_value NOT LIKE '%<%'
  AND CAST(r.result_value AS REAL) > 0
GROUP BY s.station_id, s.station_name, s.latitude, s.longitude, s.county
HAVING measurement_count > 10;  -- Only stations with enough data

.output stdout
.mode column
```

### Step 2: Create the Map File

Create a new file called `turbidity_map.html` in VSCode:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>King County Turbidity Map</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossorigin=""/>

    <style>
        body { margin: 0; padding: 0; }
        #map { height: 100vh; width: 100%; }
        .legend {
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
        }
        .legend h4 {
            margin: 0 0 10px 0;
        }
        .legend-item {
            margin: 5px 0;
        }
        .legend-circle {
            display: inline-block;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 8px;
            border: 2px solid #333;
        }
    </style>
</head>
<body>
    <div id="map"></div>

    <!-- Leaflet JavaScript -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
            integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
            crossorigin=""></script>

    <!-- PapaParse for CSV reading -->
    <script src="https://unpkg.com/papaparse@5.4.1/papaparse.min.js"></script>

    <script>
        // Initialize the map centered on King County
        var map = L.map('map').setView([47.5, -122.0], 10);

        // Add OpenStreetMap tiles (free, no API key needed!)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Function to get color based on turbidity value
        function getColor(turbidity) {
            return turbidity > 20 ? '#8B0000' :  // Dark red: very muddy
                   turbidity > 10 ? '#FF4500' :  // Orange-red: muddy
                   turbidity > 5  ? '#FFA500' :  // Orange: moderate
                   turbidity > 2  ? '#FFD700' :  // Gold: slightly cloudy
                   turbidity > 1  ? '#90EE90' :  // Light green: clear
                                    '#006400';   // Dark green: very clear
        }

        // Function to get circle size based on measurement count
        function getRadius(count) {
            return Math.sqrt(count) * 2;  // Scale by square root
        }

        // Load and parse the CSV file
        Papa.parse('king_county_turbidity_map.csv', {
            download: true,
            header: true,
            complete: function(results) {
                // Add each station as a circle marker
                results.data.forEach(function(station) {
                    if (station.latitude && station.longitude) {
                        var turbidity = parseFloat(station.avg_turbidity);
                        var count = parseInt(station.measurement_count);

                        var circle = L.circleMarker([station.latitude, station.longitude], {
                            radius: getRadius(count),
                            fillColor: getColor(turbidity),
                            color: '#000',
                            weight: 1,
                            opacity: 1,
                            fillOpacity: 0.7
                        }).addTo(map);

                        // Popup with station details
                        circle.bindPopup(`
                            <b>${station.station_name}</b><br>
                            Average Turbidity: ${turbidity.toFixed(2)} FNU<br>
                            Measurements: ${count}<br>
                            Location: ${parseFloat(station.latitude).toFixed(4)},
                                      ${parseFloat(station.longitude).toFixed(4)}
                        `);
                    }
                });
            }
        });

        // Add legend
        var legend = L.control({position: 'bottomright'});
        legend.onAdd = function(map) {
            var div = L.DomUtil.create('div', 'legend');
            div.innerHTML = `
                <h4>Turbidity (FNU)</h4>
                <div class="legend-item">
                    <span class="legend-circle" style="background-color: #006400;"></span> 0-1 (Crystal clear)
                </div>
                <div class="legend-item">
                    <span class="legend-circle" style="background-color: #90EE90;"></span> 1-2 (Clear)
                </div>
                <div class="legend-item">
                    <span class="legend-circle" style="background-color: #FFD700;"></span> 2-5 (Slightly cloudy)
                </div>
                <div class="legend-item">
                    <span class="legend-circle" style="background-color: #FFA500;"></span> 5-10 (Moderate)
                </div>
                <div class="legend-item">
                    <span class="legend-circle" style="background-color: #FF4500;"></span> 10-20 (Muddy)
                </div>
                <div class="legend-item">
                    <span class="legend-circle" style="background-color: #8B0000;"></span> 20+ (Very muddy)
                </div>
                <div style="margin-top: 10px; font-size: 0.9em;">
                    Circle size = # of measurements
                </div>
            `;
            return div;
        };
        legend.addTo(map);
    </script>
</body>
</html>
```

### Step 3: Open the Map

1. **Make sure both files are in the same folder:**
   - `king_county_turbidity_map.csv`
   - `turbidity_map.html`

2. **Open `turbidity_map.html` in a web browser:**
   - Right-click → Open with → Chrome/Firefox/Edge
   - Or drag the file into your browser

3. **Explore the map!**
   - Zoom in/out with mouse wheel
   - Click circles to see station details
   - Look for patterns

### What to Investigate

**Question 1: Where does turbidity come from?**

Look at the map and notice:
- **Mountain streams** (east side of map) - Are they clearer or muddier?
- **Rivers in valleys** - Do they get muddier as they flow downstream?
- **Near urban areas** - Is there more turbidity near cities?
- **Elevation patterns** - Is there a correlation between elevation and water clarity?

**Why this matters:** Turbidity often increases downstream as water picks up sediment. Urban areas contribute runoff from roads, construction, and impervious surfaces.

**Question 2: Upstream vs. Downstream Patterns**

Compare water quality at different points along the same river:

```sql
-- Find stations along a river system (e.g., containing "Cedar River")
SELECT
  station_name,
  latitude,
  longitude,
  AVG(CAST(result_value AS REAL)) as avg_turbidity
FROM results r
JOIN stations s USING(station_id)
WHERE param_code = '00076'
  AND station_name LIKE '%Cedar River%'
  AND result_value NOT LIKE '%<%'
GROUP BY station_id
ORDER BY latitude DESC;  -- North to south (often upstream to downstream)
```

**What to look for:**
- Does turbidity increase downstream?
- Where are the biggest changes?
- What might be causing them? (use Google Maps to investigate)

**Question 3: Seasonal Patterns**

Modify your SQL query to filter by season:

```sql
-- Winter months (December-February) - storm season
WHERE r.param_code = '00076'
  AND SUBSTR(r.start_date, 6, 2) IN ('12', '01', '02')
```

```sql
-- Summer months (June-August) - dry season
WHERE r.param_code = '00076'
  AND SUBSTR(r.start_date, 6, 2) IN ('06', '07', '08')
```

Create separate maps for summer vs. winter. Do patterns change?

**Expected findings:**
- Winter: Higher turbidity from storms washing sediment into streams
- Summer: Lower turbidity, but potentially warmer temperatures

**Question 4: Coastal vs. Inland Temperature**

Do coastal areas have more moderate temperatures than inland areas?

```sql
-- Compare average temperatures by distance from Puget Sound
-- Puget Sound center: approximately 47.6° N, 122.4° W

SELECT
  CASE
    WHEN distance_miles < 5 THEN 'Coastal (0-5 mi)'
    WHEN distance_miles < 15 THEN 'Near Coast (5-15 mi)'
    WHEN distance_miles < 50 THEN 'Inland (15-50 mi)'
    ELSE 'Far Inland (50+ mi)'
  END as region,
  ROUND(AVG(CAST(r.result_value AS REAL)), 2) as avg_temp,
  COUNT(*) as measurements
FROM results r
JOIN stations s USING(station_id)
CROSS JOIN (
  SELECT (3959 * acos(
    cos(radians(47.6)) * cos(radians(s.latitude))
    * cos(radians(s.longitude) - radians(-122.4))
    + sin(radians(47.6)) * sin(radians(s.latitude))
  )) AS distance_miles
  FROM stations
  WHERE station_id = s.station_id
) dist
WHERE r.param_code = '00010'  -- Temperature
  AND r.result_value NOT LIKE '%<%'
  AND CAST(r.result_value AS REAL) BETWEEN 0 AND 30
GROUP BY region
ORDER BY MIN(distance_miles);
```

**Question 5: Visual Investigation with Google Maps**

For any interesting pattern you find:

1. **Export the stations** showing high values
2. **Open Google Maps** in satellite view
3. **Look for visible features:**
   - Construction sites (disturbed soil → turbidity)
   - Agricultural fields (fertilizer → nutrients)
   - Deforested areas (erosion → sediment)
   - Urban development (runoff → multiple pollutants)
   - Industrial facilities (point sources)
4. **Formulate hypotheses** about what you see

**Example workflow:**
- Find cluster of high turbidity stations
- Note their coordinates
- Search coordinates in Google Maps
- Switch to satellite view
- Look for large-scale earthmoving, development, or agriculture
- Hypothesize connection between land use and water quality

**Question 6: Clustering Analysis**

Are pollution problems concentrated in certain areas, or widespread?

1. Create a map with ALL stations colored by turbidity
2. Look for:
   - **Hot spots** - clusters of red (high turbidity)
   - **Clean zones** - clusters of blue (low turbidity)
   - **Transition zones** - where does water quality change?
3. Consider:
   - Watershed boundaries
   - Urban vs. rural areas
   - Mountainous vs. flat terrain
   - Rivers flowing through different land uses

### Customize Your Map

**Change the parameter:**

Temperature map:
```sql
WHERE r.param_code = '00010'  -- Temperature instead of turbidity
```

Update the color scale in the HTML:
```javascript
function getColor(temperature) {
    return temperature > 20 ? '#8B0000' :  // Hot
           temperature > 15 ? '#FFA500' :  // Warm
           temperature > 10 ? '#FFD700' :  // Moderate
           temperature > 5  ? '#90EE90' :  // Cool
                              '#006400';   // Cold
}
```

**Different region:**
```sql
WHERE s.county = 'Pierce'  -- Or Snohomish, Spokane, etc.
```

**Add more data:**

Include station type, agency, or date ranges:
```sql
SELECT
  s.station_id,
  s.station_name,
  s.latitude,
  s.longitude,
  s.county,
  s.station_type,  -- Add this
  AVG(CAST(r.result_value AS REAL)) as avg_turbidity,
  COUNT(*) as measurement_count,
  MIN(r.start_date) as first_measurement,  -- Add this
  MAX(r.start_date) as last_measurement     -- Add this
```

Update the popup in HTML to show new fields.

---

## Real-World Investigation Examples

### Example 1: Cedar River Watershed

**Background:** Seattle's drinking water comes from the Cedar River.

**Investigation:**
1. Find all stations in the Cedar River watershed
2. Map turbidity before and after rainstorms
3. Identify potential contamination sources
4. Track water quality from mountains to city

**Questions:**
- Is water clearer at higher elevations?
- How does logging affect turbidity?
- Where should Seattle focus monitoring?

### Example 2: Puget Sound Temperature

**Background:** Salmon need cold water (< 16°C / 61°F) to survive.

**Investigation:**
1. Map average summer temperatures in streams
2. Identify hot spots that are too warm for salmon
3. Correlate with stream shading (trees vs. cleared land)
4. Predict climate change impacts

**Questions:**
- Which streams are marginal for salmon?
- Does shade from trees help keep water cool?
- Are temperatures rising over time?

### Example 3: Elevation and Water Temperature

**Background:** Higher elevations tend to have cooler water temperatures.

**Investigation:**
1. Map temperature data across the state
2. Note elevation patterns (mountains vs. valleys)
3. Look for correlation between elevation and temperature
4. Consider implications for cold-water fish (like salmon)

**Questions:**
- Are mountain streams consistently cooler?
- How much does temperature change with elevation?
- Which lowland areas might be too warm for salmon?
- Are there seasonal differences in this pattern?

**SQL Query to Investigate:**
```sql
-- Compare temperatures at different elevations
-- (We don't have elevation in database, but latitude can be a proxy:
--  northern/eastern Washington has more mountains)

SELECT
  CASE
    WHEN latitude > 48.5 THEN 'Northern (mountainous)'
    WHEN latitude > 47.5 THEN 'Central'
    ELSE 'Southern'
  END as region,
  AVG(CAST(result_value AS REAL)) as avg_temp_celsius,
  COUNT(*) as measurements
FROM results r
JOIN stations s USING(station_id)
WHERE param_code = '00010'  -- Temperature
  AND result_value NOT LIKE '%<%'
  AND CAST(result_value AS REAL) BETWEEN 0 AND 30
GROUP BY region
ORDER BY region;
```

---

## Advanced Options (For Interested Students)

### Option 2: Python with Folium

If you want more control and automation, use Python:

**Why Python/Folium?**
- Automate map generation from SQL queries
- Create multiple maps programmatically
- Add heatmaps, clusters, time sliders
- Integrate with data analysis workflow

**Getting started:**
```bash
pip install folium geopy
```

**Simple example:**
```python
import sqlite3
import folium
import pandas as pd

# Query database
conn = sqlite3.connect('washington_water.db')
df = pd.read_sql_query("""
    SELECT latitude, longitude, station_name,
           AVG(CAST(result_value AS REAL)) as avg_turbidity
    FROM results JOIN stations USING(station_id)
    WHERE param_code = '00076' AND county = 'King'
    GROUP BY station_id
""", conn)

# Create map
m = folium.Map(location=[47.5, -122.0], zoom_start=10)

# Add markers
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=8,
        popup=f"{row['station_name']}<br>Turbidity: {row['avg_turbidity']:.2f}",
        color='red' if row['avg_turbidity'] > 10 else 'blue'
    ).add_to(m)

# Save
m.save('turbidity_map.html')
```

**Resources:**
- Folium documentation: https://python-visualization.github.io/folium/
- Tutorial: Search YouTube for "Python Folium tutorial"

### Option 3: QGIS (Professional GIS Software)

If you want industry-standard tools:

**Why QGIS?**
- Professional spatial analysis
- Direct SQLite database connection
- Advanced visualization (heatmaps, interpolation)
- Export to professional formats (shapefiles, GeoTIFF)
- Used by environmental consultants, government agencies

**Getting started:**
1. Download QGIS: https://qgis.org/download/ (free, ~600 MB)
2. Layer → Add Layer → Add Vector Layer
3. Choose SQLite database
4. Run SQL queries in DB Manager
5. Style by attribute (turbidity, temperature, etc.)

**Skills you'll learn:**
- Spatial joins
- Buffer analysis
- Interpolation (kriging, IDW)
- Map layout and export

**Resources:**
- QGIS Tutorials: https://www.qgistutorials.com/
- Video course: "QGIS for Absolute Beginners" on YouTube

---

## Summary

**What you learned:**
- ✅ Calculate distances on Earth's surface with Haversine formula
- ✅ Find stations near specific locations
- ✅ Export spatial data from SQLite
- ✅ Create interactive web maps with Leaflet
- ✅ Visualize patterns in water quality data
- ✅ Investigate real environmental questions

**Interview talking points:**
- "I used SQL spatial queries to find monitoring stations within a radius"
- "I created interactive maps to investigate turbidity sources"
- "I correlated water quality with geographic features and land use"
- "I visualized 3.1 million measurements to identify environmental patterns"

**Next steps:**
- Try different parameters (pH, dissolved oxygen, temperature)
- Investigate your own county or watershed
- Combine with temporal analysis (seasonal patterns)
- Share maps with friends to show what you learned!

---

**Questions?** See [WATER_DATA.html](Documentation/WATER_DATA.html) for more SQL examples.
