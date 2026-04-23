```
This script extracts Mozilla Firefox browsing history from the places.sqlite database.  
It executes a query that retrieves visit timestamps, URLs, page titles, visit types, and referrer IDs, 
then formats each record as a CSV-style line using SQLite’s printf() function. 
Displays history in sorted chronological order (newest first).
```

import sqlite3
import os
from datetime import datetime

PLACES_DB = r"{{ .PATHTOFIREFOXPLACES_DB }}"

if not os.path.exists(PLACES_DB):
    raise FileNotFoundError(f"places.sqlite not found at: {PLACES_DB}")

QUERY = """
SELECT
    'visited_at, url, title, visit_type, from_visit' AS csv_output
UNION ALL
SELECT
    printf(
        '%s, %s, %s, %d, %d',
        datetime(visit_date/1000000, 'unixepoch'),
        url,
        title,
        visit_type,
        from_visit
    ) AS csv_output
FROM (
    SELECT
        v.visit_date,
        p.url,
        p.title,
        v.visit_type,
        v.from_visit
    FROM moz_historyvisits v
    JOIN moz_places p
        ON v.place_id = p.id
    ORDER BY v.visit_date DESC
);
"""

def query_firefox_history(db_path):
    # Firefox locks DB if running; open with read-only mode
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = conn.cursor()

    cur.execute(QUERY)
    rows = cur.fetchall()

    columns = [desc[0] for desc in cur.description]

    conn.close()
    return columns, rows

def print_results(columns, rows):
    print("\t".join(columns))
    print("-" * 120)

    for r in rows:
        print(r[0])

if __name__ == "__main__":
    cols, results = query_firefox_history(PLACES_DB)
    print_results(cols, results)
