import io
import os
import time
import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
COLUMNS = "unique_key,created_date,closed_date,agency,complaint_type,descriptor,borough,incident_zip,status,open_data_channel_type"
# Keep pages small enough that the public API reliably returns them without
# hanging on a single large CSV payload.
PAGE_SIZE = 10000

MONTHS = {
    "jan_week1": ("2025-01-01T00:00:00", "2025-01-07T23:59:59"),
}


RETRYABLE_ERRORS = (
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.Timeout,
    requests.exceptions.ConnectionError,
)

# Reused across page requests so TCP/TLS connections are kept alive.
SESSION = requests.Session()


def request_with_retry(params, timeout=180, max_retries=4):
    """GET the Socrata endpoint, retrying on transient connection errors.

    Returns the raw requests.Response, or raises if all attempts fail.
    """
    for attempt in range(1, max_retries + 1):
        try:
            r = SESSION.get(URL, params=params, timeout=timeout)
            r.raise_for_status()
            return r
        except RETRYABLE_ERRORS as e:
            if attempt < max_retries:
                wait_time = 2 ** attempt  # 2, 4, 8, 16 seconds
                print(f"    connection error on attempt {attempt} ({type(e).__name__}), "
                      f"retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    # Unreachable; kept for type checkers.
    raise RuntimeError("request_with_retry exhausted retries without returning")


def count_rows(start, end):
    """Ask the server how many rows exist in this date range."""
    params = {
        "$select": "count(*)",
        "$where": f"created_date between '{start}' and '{end}'",
    }
    r = request_with_retry(params)
    return int(pd.read_csv(io.StringIO(r.text)).iloc[0, 0])


def fetch_page(params):
    """Download one page of rows as a DataFrame of strings."""
    r = request_with_retry(params)
    return pd.read_csv(io.StringIO(r.text), dtype=str)


def download_month(name, start, end):
    """Download one date range, one page at a time."""
    total = count_rows(start, end)
    print(f"{name}: server says {total} rows")

    chunks = []
    offset = 0
    while True:
        params = {
            "$select": COLUMNS,
            "$where": f"created_date between '{start}' and '{end}'",
            "$order": "unique_key",
            "$limit": PAGE_SIZE,
            "$offset": offset,
        }
        chunk = fetch_page(params)
        chunks.append(chunk)
        print(f"  got {len(chunk)} rows (offset {offset})")

        if len(chunk) < PAGE_SIZE:   # last page reached
            break
        offset += PAGE_SIZE

    df = pd.concat(chunks, ignore_index=True)
    print(f"  expected {total}, downloaded {len(df)}")
    return df


if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    for name, (start, end) in MONTHS.items():
        df = download_month(name, start, end)
        path = f"data/raw/311_{name}_2025.csv"
        df.to_csv(path, index=False)
        print(f"saved to {path}")