# NYC 311 Resolution Time Analysis

Analyzing which complaint types and boroughs have the slowest 311 service request resolution times in NYC.

## Data

- Source: NYC Open Data, 311 Service Requests
- Period: January 1-7, 2025 (first week)
- Size: 90,565 requests
- Key columns: created_date, closed_date, complaint_type, borough, agency, status

## Findings

### Slowest complaint types (median days to close)

1. [Type A]: X days
2. [Type B]: Y days
3. ...

### Slowest boroughs

[Borough]: X days median

### Open requests

X% of requests are still open (no closed_date as of data pull date)

## Limitations

- First week only; seasonal variation not captured
- Does not include all 311 calls (see NYC data notes)
- Resolution time includes time waiting for customer follow-up, not just agency work time

## Files

- `src/download_311.py` - API download script
- `data/raw/311_jan_week1_2025.csv` - raw download (in .gitignore)
- `data/clean/311_jan_week1_clean.csv` - cleaned data
- `notebooks/01_cleaning.ipynb` - cleaning decisions
- `notebooks/02_eda.ipynb` - analysis and findings
- `notebooks/03_visualization.ipynb` - charts
