# Keeping the Power BI dashboard refreshed automatically

A `.pbix` file stored in this repo is a snapshot. GitHub cannot render it, and it does not refresh on its own. The data behind it (`data/crypto_snapshots.csv`) updates every day, but the Power BI file only shows whatever was last published.

There are two ways to close that gap. The web dashboard in `/docs` is already live and needs nothing further. If you also want the Power BI version to stay current, follow the steps below once.

## Point Power BI at the live CSV

The raw, always-current CSV lives at:

```
https://raw.githubusercontent.com/Harshit2705-ops/crypto-monitor/main/data/crypto_snapshots.csv
```

In Power BI Desktop:

1. **Get Data > Web**, and paste the URL above.
2. Load and shape the data as needed (set `snapshot_date` to a date type, and the price and market cap columns to decimal).
3. Rebuild or repoint your visuals against this query instead of a local file.
4. Save and re-publish the `.pbix`.

Using the web source instead of a local file is what makes automatic refresh possible.

## Set up scheduled refresh (Power BI Service)

1. Sign in to the Power BI Service at app.powerbi.com with your own account.
2. **Publish** the report from Power BI Desktop to a workspace.
3. In the Service, open the dataset **Settings**.
4. Under **Data source credentials**, sign in to the web source (Anonymous is fine for a public CSV).
5. Under **Scheduled refresh**, turn it on and set a daily time. Pick a time shortly after 06:00 UTC, since that is when the pipeline commits the new snapshot.

A public web CSV does not require an on-premises data gateway, so this is all that is needed.

## Optional: a public link

If you want recruiters to open the Power BI report without a login, use **File > Embed report > Publish to web (public)** in the Service. Note that this makes the report publicly visible to anyone with the link, so only use it for non-sensitive data like this.

## Which version to share

For most people, send the web dashboard link. It opens in any browser, needs no Power BI install, and is always current. Keep the Power BI version for anyone who specifically wants to explore the model in Power BI Desktop.
