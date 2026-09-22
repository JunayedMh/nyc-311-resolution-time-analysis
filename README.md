# NYC 311 Resolution Time Analysis

Analyzing which complaint types and boroughs take longest to resolve in NYC's 311 service request system.

## Data

**Source:** NYC Open Data, 311 Service Requests  
**Period:** January 1-7, 2025  
**Original records:** 90,565  
**Cleaned and analyzed:** 85,122 (94%)

## Resolution Time Overview

After cleaning, 85,122 closed requests span a wide range of resolution speeds.

- **Median resolution time:** 0 days (half of requests close same-day)
- **Mean:** 6.65 days (pulled up by outliers)
- **Standard deviation:** 31.13 days
- **Range:** 0 to 622 days
- **75th percentile:** 1 day (three-quarters close within one day)

The distribution is heavily skewed—most requests close immediately, but a long tail extends to over 600 days. Median is the appropriate measure of typical resolution time.

## Data Quality

- **Status:** All 85,122 records are Closed (100%)
- **Core fields:** Zero missing values in created date, closed date, agency, complaint type, borough, or zip code
- **Optional fields:** 973 records (1.1%) have missing descriptor, which is a sub-classification detail, not critical to analysis

## Cleaning Decisions

- **Filtered to Closed requests only.** Excluded 462 in-progress, open, or pending requests (cannot calculate resolution time without close date)
- **Imputed missing close dates.** 230 Closed requests with no recorded close date were assigned January 7, 2025 at 11:59:59 PM (end of data collection week)
- **Dropped Unspecified borough.** 37 requests with borough="Unspecified" were excluded (not analyzable geographically)
- **Kept missing descriptors.** 973 records retain null descriptors since this is an optional lookup detail

## Next Steps: EDA and Visualization

This cleaned dataset is ready for exploratory analysis to answer:

- Which complaint types resolve fastest? Slowest?
- Do boroughs differ in resolution speed?
- Do agencies show different performance patterns?
- What drives the 622-day maximum outliers?

## Tools

Python 3.12, pandas, matplotlib, Socrata API

## Files

- `src/download_311.py` - API download script
- `data/raw/311_jan_week1_2025.csv` - raw download (in .gitignore)
- `data/clean/311_jan_week1_clean.csv` - cleaned data
- `notebooks/01_cleaning.ipynb` - cleaning decisions
- `notebooks/02_eda.ipynb` - analysis and findings
- `notebooks/03_visualization.ipynb` - charts
