# crypto-monitor

End-to-end crypto data pipeline: automated ingestion → 
GitHub storage → Power BI dashboard.

## Pipeline
1. **Ingest** (`ingest.py`) — pulls daily top-50 crypto 
   prices from CoinGecko API
2. **Schedule** (`.github/workflows`) — GitHub Actions 
   runs it daily, commits new snapshot automatically
3. **Store** (`/data`) — 100+ days of snapshots in CSV
4. **Visualize** (`/dashboard`) — Power BI dashboard 
   reads live from this repo

## Key Findings (100 days: May–Sept 2026)
- Total market cap grew from $2.46T to $2.69T (+9.2%)
- BTC ranged $58.6K–$80.9K, a 38% peak-to-trough swing
- Top 3 coins hold 77.7% of total market cap
- Biggest gainer: Zcash +130% | Biggest loser: MemeCore -60%

## Stack
Python · GitHub Actions · CoinGecko API · Power BI · DAX
