# crypto-monitor

Automated data pipeline that fetches daily cryptocurrency price data 
and commits snapshots to this repo on a schedule.

## What it does
- Pulls price data from [API name] every day at [time] UTC
- Saves snapshots to /data as timestamped CSV files
- Runs via GitHub Actions (see .github/workflows)

## Stack
- Python (requests, pandas)
- GitHub Actions for scheduling
- CSV storage

## How to run locally
[2-3 lines: install requirements, set env vars, run ingest.py]

## Why I built this
[1-2 lines: what you were learning or solving]# crypto-monitor
