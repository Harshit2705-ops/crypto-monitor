# Keeping the Power BI file current

`Crypto Dashboard.pbix` ships with the data baked in, so on its own it is a snapshot from whenever it was last saved. There are two ways to keep it current, and the first one needs no Microsoft or cloud login at all.

## Option 1: Auto-refresh on open (no login needed)

This makes the file pull the latest data from GitHub every time it is opened in Power BI Desktop. No Power BI Service account, no work email, nothing to sign into.

**Step 1: Point the query at the live data**

In Power BI Desktop: Home > Transform data > Power Query Editor. Select the query, open the Advanced Editor, and replace the `Source` step with this:

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

**Step 2: Turn on refresh-on-open**

File > Options and settings > Options > Current File > Data Load > tick "Refresh data when file is opened" > OK. Save the file.

That is the whole fix. Every time the file is opened, it pulls whatever is in `data/crypto_snapshots.csv` at that moment, and the pipeline updates that file daily. Anyone who downloads the `.pbix` and opens it gets current data automatically, no account required.

## Option 2: Scheduled cloud refresh (optional, needs a work email)

If a cloud-hosted, shareable version with refresh on a schedule (rather than on open) is wanted, that goes through the Power BI Service at app.powerbi.com. The signup there is built for a Microsoft 365 "work or school" account and generally rejects personal addresses like a Gmail account.

The common workaround is the Microsoft 365 Developer Program (developer.microsoft.com/microsoft-365/dev-program), which is free and gives a proper `@<something>.onmicrosoft.com` mailbox that Power BI Service accepts, without needing a real employer or a paid Microsoft 365 subscription. With that:

1. Publish the file to the Power BI Service.
2. In the dataset settings, point the source at the same raw CSV URL above.
3. Turn on scheduled refresh (daily is enough, since the pipeline only updates once a day).
4. Optionally generate a public embed link to share the report without anyone needing a Power BI account to view it.

This route is entirely optional. Option 1 already solves the "not updating" problem for anyone who opens the file.
