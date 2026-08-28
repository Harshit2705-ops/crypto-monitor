#!/usr/bin/env python3
"""
Crypto Market Monitor — daily ingestion.

Pulls the top-N coins from the free CoinGecko API and appends one row per coin
per day to data/crypto_snapshots.csv. Run daily (GitHub Actions does this for
you). First time, use --backfill to seed ~90 days of history so your dashboard
isn't empty on day one.

Usage:
    python ingest.py                 # append today's snapshot
    python ingest.py --backfill 90   # seed 90 days of history, then also today

No API key is required for light use. If you hit rate limits, get a free
CoinGecko "Demo" API key and set it as the COINGECKO_API_KEY environment
variable (GitHub: repo Settings > Secrets > Actions).
"""
import csv, os, sys, time, datetime as dt
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

BASE = "https://api.coingecko.com/api/v3"
TOP_N = 50
CSV_PATH = os.path.join("data", "crypto_snapshots.csv")
HEADER = ["snapshot_date", "coin_id", "symbol", "name",
          "market_cap_rank", "price_usd", "market_cap_usd", "volume_24h_usd"]
API_KEY = os.environ.get("COINGECKO_API_KEY", "").strip()


def _get(path, params):
    url = f"{BASE}{path}?{urlencode(params)}"
    headers = {"User-Agent": "crypto-monitor/1.0", "Accept": "application/json"}
    if API_KEY:
        headers["x-cg-demo-api-key"] = API_KEY
    for attempt in range(5):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            wait = 8 * (attempt + 1)
            print(f"  request failed ({e}); retry in {wait}s")
            time.sleep(wait)
    raise SystemExit(f"Gave up on {url}")


def top_coins():
    """Current top-N coins by market cap (one API call)."""
    return _get("/coins/markets", {
        "vs_currency": "usd", "order": "market_cap_desc",
        "per_page": TOP_N, "page": 1, "sparkline": "false",
    })


def read_existing_keys():
    """(snapshot_date, coin_id) pairs already stored, to avoid duplicates."""
    keys = set()
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="") as f:
            for row in csv.DictReader(f):
                keys.add((row["snapshot_date"], row["coin_id"]))
    return keys


def write_rows(rows):
    exists = os.path.exists(CSV_PATH)
    os.makedirs("data", exist_ok=True)
    with open(CSV_PATH, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(HEADER)
        w.writerows(rows)


def snapshot_today(coins, keys):
    today = dt.date.today().isoformat()
    rows = []
    for c in coins:
        k = (today, c["id"])
        if k in keys:
            continue
        rows.append([today, c["id"], c["symbol"], c["name"],
                     c.get("market_cap_rank"), c.get("current_price"),
                     c.get("market_cap"), c.get("total_volume")])
    return rows


def backfill(coins, days, keys):
    """Seed daily price/mcap/volume history for each coin (rank unknown historically)."""
    rows = []
    for i, c in enumerate(coins, 1):
        print(f"  backfilling {c['id']} ({i}/{len(coins)})")
        data = _get(f"/coins/{c['id']}/market_chart",
                    {"vs_currency": "usd", "days": days, "interval": "daily"})
        prices = data.get("prices", [])
        mcaps = {p[0]: p[1] for p in data.get("market_caps", [])}
        vols = {p[0]: p[1] for p in data.get("total_volumes", [])}
        for ts, price in prices:
            d = dt.datetime.utcfromtimestamp(ts / 1000).date().isoformat()
            k = (d, c["id"])
            if k in keys:
                continue
            keys.add(k)
            rows.append([d, c["id"], c["symbol"], c["name"], "",
                         round(price, 6), mcaps.get(ts, ""), vols.get(ts, "")])
        time.sleep(2.5)  # be gentle with the free API
    return rows


def main():
    keys = read_existing_keys()
    coins = top_coins()
    print(f"Fetched {len(coins)} coins.")
    all_rows = []
    if len(sys.argv) > 2 and sys.argv[1] == "--backfill":
        all_rows += backfill(coins, int(sys.argv[2]), keys)
    all_rows += snapshot_today(coins, keys)
    if all_rows:
        write_rows(all_rows)
    print(f"Wrote {len(all_rows)} new rows to {CSV_PATH}.")


if __name__ == "__main__":
    main()
