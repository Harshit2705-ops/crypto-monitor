# crypto-monitor

Automated data pipeline that fetches daily cryptocurrency price data 
and commits snapshots to this repo on a schedule.

## What it does
- Pulls price data from coingreko every day at 11:00 UTC
- Saves snapshots to /data as timestamped CSV files
- Runs via GitHub Actions (see .github/workflows)

## Stack
- Python (requests, pandas)
- GitHub Actions for scheduling
- CSV storage


