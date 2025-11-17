# Washington State Water Quality Data - Time Code Documentation

## Overview

The `start_time` field in the results table contains a mix of actual sampling times and special code values. This field is stored as VARCHAR(10) rather than TIME to preserve the original data encoding.

## Data Format

Valid times are stored as 4-digit strings in 24-hour format without separators:
- `0730` = 7:30 AM
- `1330` = 1:30 PM
- `2359` = 11:59 PM

## Special Time Codes

Analysis of 3,178,425 water quality measurement records revealed the following special codes:

### Most Common Special Codes

| Code | Frequency | Percentage | Likely Meaning |
|------|-----------|------------|----------------|
| `2500` | 438,287 | 13.8% | **Time not recorded** or **Daily composite/average sample** |
| `0001` | 224,557 | 7.1% | **Start of day** or **Time unknown** |
| (empty) | 81,546 | 2.6% | **No time recorded** |
| `2400` | 1,874 | 0.06% | **Midnight** (end of day = 00:00) |
| `9999` | 11 | <0.01% | **Missing/Not applicable** |

### Interpretation Notes

#### Code 2500 - "Time Not Recorded" / "Daily Composite"

The most prevalent special code (13.8% of all records) strongly suggests this represents:
- **Composite samples** collected over a 24-hour period (no specific time)
- **Daily average** measurements
- **Time not documented** in field records

This is particularly common in:
- Automated monitoring stations
- Groundwater sampling (where time is less critical)
- Historical records where precise time wasn't recorded

#### Code 0001 - "Start of Day" / "Time Unknown"

The second most common code (7.1% of records) likely indicates:
- Samples taken at an unknown time during the day
- Default value for "beginning of sampling day"
- Legacy data where time precision wasn't maintained

#### Code 2400 - "Midnight"

Represents midnight (00:00) - technically valid as "end of previous day" notation in 24-hour time systems, though 0000 is more standard.

#### Code 9999 - "Missing/Not Applicable"

Rare occurrences suggest this is a standard "missing data" sentinel value used in environmental monitoring databases.

## Data Quality Implications

### For Time-Series Analysis

When performing temporal analysis:
- **Use `start_date` only** for daily/monthly/yearly aggregations
- **Filter out special codes** if analyzing intra-day patterns
- **Consider special codes as "all-day" measurements** for daily averages

### For Data Validation

Records with special time codes (2500, 0001, 9999) should **not** be considered errors or excluded from analysis - they represent valid measurement records where the specific sampling time was either:
- Not recorded
- Not applicable (composite samples)
- Historically unavailable

## Sample SQL Queries

### Identify Valid Times (HH:MM parseable)

```sql
SELECT COUNT(*)
FROM results
WHERE start_time ~ '^([01][0-9]|2[0-3])[0-5][0-9]$';
```

### Filter to Special Time Codes Only

```sql
SELECT start_time, COUNT(*) as count
FROM results
WHERE start_time IN ('2500', '0001', '2400', '9999', '')
GROUP BY start_time
ORDER BY count DESC;
```

### Exclude Special Codes for Time-of-Day Analysis

```sql
SELECT start_time, COUNT(*)
FROM results
WHERE start_time IS NOT NULL
  AND start_time != ''
  AND start_time NOT IN ('2500', '0001', '2400', '9999')
  AND start_time ~ '^([01][0-9]|2[0-3])[0-5][0-9]$'
GROUP BY start_time
ORDER BY start_time;
```

## References

This analysis is based on:
- EPA STORET (STOrage and RETrieval) legacy data system
- Water Quality Exchange (WQX) standards
- Analysis of 3,178,425 measurement records from Washington State

**Note**: The exact meanings of codes 2500 and 0001 are inferred from frequency analysis and common environmental monitoring practices. Official STORET/WQX documentation does not appear to be publicly available online for these legacy time codes.

For questions about specific code meanings, contact:
- EPA WQX Support: wqx@epa.gov
- Water Quality Portal: https://www.waterqualitydata.us/

---
*Last Updated: 2025-11-15*
*Data Source: Washington State Water Quality Monitoring Data (EPA STORET)*
