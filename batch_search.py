#!/usr/bin/env python3
# Background Google requests with optional browser-tab mode.
# Prints only "Finished." at the end.

import argparse, csv, time, sys, random, urllib.parse, webbrowser
from pathlib import Path
import requests

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def iter_cells(csv_path: Path, delimiter: str = ";", dedupe: bool = True):
    seen = set()
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            for cell in row:
                q = (cell or "").strip()
                if not q:
                    continue
                if dedupe and q in seen:
                    continue
                seen.add(q)
                yield q

def hit_google_http(query: str, method: str = "GET", timeout: float = 15.0):
    """
    HEAD/GET request to Google Search (no tab). Returns status or error string.
    """
    url = "https://www.google.com/search"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    params = {"q": query}
    try:
        if method == "HEAD":
            r = requests.head(url, headers=headers, params=params, timeout=timeout, allow_redirects=True)
        else:
            r = requests.get(url, headers=headers, params=params, timeout=timeout, stream=True, allow_redirects=True)
            next(r.iter_content(chunk_size=512), None)  # touch stream, then close
        code = r.status_code
        r.close()
        return code
    except requests.RequestException as e:
        return f"ERR:{e.__class__.__name__}"

def open_google_browser(query: str, new: int = 2):
    """
    Open Google Search in the default browser (new tab if possible).
    """
    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
    webbrowser.open(url, new=new)

def main():
    ap = argparse.ArgumentParser(description="Send Google Search requests (HEAD/GET) or open browser tabs for each CSV cell.")
    ap.add_argument("csv", type=Path, help="Path to the ;-separated CSV file")
    ap.add_argument("--times", "-t", type=int, default=10, help="How many times per query (default: 10)")
    ap.add_argument("--delay", "-d", type=float, default=1.5, help="Seconds between requests/tabs (default: 1.5)")
    ap.add_argument("--per-query-delay", "-pqd", type=float, default=3.0, help="Pause between different queries (default: 3.0)")
    ap.add_argument("--delimiter", default=";", help="CSV delimiter (default: ;)")
    ap.add_argument("--no-dedupe", action="store_true", help="Disable de-duplication of identical cells")
    ap.add_argument("--method", choices=["HEAD", "GET", "BROWSER"], default="GET",
                    help="HEAD/GET = background HTTP; BROWSER = open tabs (default: GET)")
    ap.add_argument("--jitter", type=float, default=0.4, help="± seconds randomness added to delays (default: 0.4)")
    ap.add_argument("--new-window", action="store_true", help="With BROWSER method, open new windows instead of tabs")
    args = ap.parse_args()

    if not args.csv.exists():
        print(f"CSV not found: {args.csv}", file=sys.stderr)
        sys.exit(1)

    for query in iter_cells(args.csv, args.delimiter, dedupe=not args.no_dedupe):
        for _ in range(args.times):
            if args.method == "BROWSER":
                open_google_browser(query, new=1 if args.new_window else 2)
            else:
                # HEAD/GET background request
                _status = hit_google_http(query, method=args.method)
            time.sleep(max(0.0, args.delay + random.uniform(-args.jitter, args.jitter)))
        time.sleep(max(0.0, args.per_query_delay + random.uniform(-args.jitter, args.jitter)))

    print("Finished.")

if __name__ == "__main__":
    main()
