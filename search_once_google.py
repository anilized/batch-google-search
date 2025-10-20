#!/usr/bin/env python3
# One HEAD request per CSV cell, no extra CLI flags. Prints "Finished." when done.

import csv, sys
from pathlib import Path

import requests  # pip install requests

def iter_cells(csv_path: Path, delimiter: str = ";", dedupe: bool = True):
    seen = set()
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.reader(f, delimiter=delimiter):
            for cell in row:
                q = (cell or "").strip()
                if not q:
                    continue
                if dedupe and q in seen:
                    continue
                seen.add(q)
                yield q

def head_google(query: str, timeout: float = 15.0):
    url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    try:
        r = requests.head(url, headers=headers, params={"q": query},
                          timeout=timeout, allow_redirects=True)
        r.close()
    except requests.RequestException:
        pass  # ignore errors; goal is just to send one lightweight request

def main():
    if len(sys.argv) != 2:
        print("Usage: python search_once_head_windows.py <queries.csv>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        sys.exit(1)

    for query in iter_cells(csv_path):
        head_google(query)

    print("Finished.")

if __name__ == "__main__":
    main()
