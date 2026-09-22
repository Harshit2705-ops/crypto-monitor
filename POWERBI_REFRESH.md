# Keeping the Power BI file current

If you just want to open the dashboard and look at it, start with the section right below. If you're the one maintaining this file, the technical setup is further down.

## If you just received this file

Download `Crypto Dashboard.pbix` from this repo using the download button on the file's page. If you don't already have Power BI Desktop, install it first; it's free, from the Microsoft Store or powerbi.microsoft.com, and no Microsoft or work account is needed just to open a file. Then open the file. It should refresh itself automatically and pull the latest prices, with no sign-in required. If it opens showing old numbers, click Refresh once in the Home ribbon; that always pulls the current data.

That covers viewing it. Everything below is for whoever maintains this file, in case the query ever needs fixing again.

## How the auto-refresh is set up

`Crypto Dashboard.pbix` ships with the data baked in, so on its own it's a snapshot from whenever it was last saved. The fix below makes it pull fresh data from GitHub every time it's opened in Power BI Desktop, no Power BI Service account, no work email, nothing to sign into.

### Step 1: Point the query at the live data

In Power BI Desktop go to Home, then Transform data, then Power Query Editor. Select the query, open the Advanced Editor, and replace the Source step with this:

```
let
    Source = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Harshit2705-ops/crypto-monitor/main/data/crypto_snapshots.csv"),
        [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"snapshot_date", type date},
        {"coin_id", type text},
        {"symbol", type text},
        {"name", type text},
        {"market_cap_rank", Int64.Type},
        {"price_usd", type number},
        {"market_cap_usd", type number},
        {"volume_24h_usd", type number}
    })
in
    ChangedTypes
```

Click Close & Apply. The file now reads straight from the CSV in this repo instead of a frozen copy.

### Step 2: Turn on refresh-on-open

Go to File, then Options and settings, then Options, then Current File, then Data Load, and tick "Refresh data when file is opened," then click OK and save the file.

That's the whole fix. Every time the file is opened, it pulls whatever is in `data/crypto_snapshots.csv` at that moment, and the pipeline updates that file daily. Anyone who downloads the `.pbix` and opens it gets current data automatically, no account required.

## Optional: a cloud-hosted version with scheduled refresh

If a version hosted on the Power BI Service with refresh on a schedule, rather than on open, is ever needed, that requires a Microsoft 365 work or school account. A personal Gmail-type address won't work for signing up there. The free Microsoft 365 Developer Program gives a proper mailbox for this without needing a real employer. From there it's the usual routine: publish, point the dataset at the same CSV URL, and turn on scheduled refresh. Most people opening this file don't need to bother with this.
