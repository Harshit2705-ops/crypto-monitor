# crypto-monitor

An end-to-end crypto data pipeline that runs itself. It pulls daily prices, stores them in Git, and reads them into a live dashboard, with no manual steps once it is set up.

**Live dashboard:** https://harshit2705-ops.github.io/crypto-monitor/

## How it works

1. **Ingest** — `ingest.py` pulls the top 50 coins by market cap from the CoinGecko API.
2. **Schedule** — `.github/workflows/daily.yml` runs the script every day at 06:00 UTC through GitHub Actions and commits the new rows automatically. It only commits when the data has actually changed.
3. **Store** — `/data/crypto_snapshots.csv` holds every snapshot, one row per coin per day.
4. **Visualise** — two ways:
   - `/docs` is a web dashboard (HTML and Chart.js) that reads the CSV on every load, so it always reflects the latest snapshot in the repo. This is the live version linked above.
   - A Power BI version is also included for anyone who prefers to open it in Power BI Desktop. It is a static export; see the note below on keeping it refreshed.

## What the data shows (100 days, May to Sept 2026)

- Total market cap moved from $2.46T to $2.69T, up 9.2%.
- Bitcoin ranged from $58.6K to $80.9K, a 38% swing from peak to trough.
- The top 3 coins hold 77.7% of total market cap.
- Biggest gainer: Zcash, up 130%. Biggest loser: MemeCore, down 60%.

## Stack

Python, GitHub Actions, CoinGecko API, Chart.js, GitHub Pages, Power BI, DAX.

## Keeping the Power BI file refreshed

The Power BI file in this repo now fixes this on its own: it pulls fresh data from GitHub every time it is opened in Power BI Desktop, so anyone who downloads it gets current numbers automatically, with no login needed. If you just received the file and want to open it, see the top of [`POWERBI_REFRESH.md`](POWERBI_REFRESH.md); the rest of that file is for whoever maintains the query later. The web dashboard in `/docs` needs none of this; it is always current.
