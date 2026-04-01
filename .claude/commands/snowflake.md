---
description: Query Snowflake via snow CLI — list tables, describe schema, run SQL, debug data
allowed-tools: Bash
---

Query Snowflake for: $ARGUMENTS

Run the appropriate command(s) below and interpret the results.

```bash
# List tables in RAW schema
snow sql -q "SHOW TABLES IN SCHEMA MARKETDATA.RAW"

# Count rows in OHLCV
snow sql -q "SELECT COUNT(*) FROM MARKETDATA.RAW.OHLCV"

# Latest rows inserted
snow sql -q "SELECT * FROM MARKETDATA.RAW.OHLCV ORDER BY INGESTED_AT DESC LIMIT 20"

# Tickers present
snow sql -q "SELECT TICKER, COUNT(*) as n FROM MARKETDATA.RAW.OHLCV GROUP BY TICKER ORDER BY TICKER"

# Describe table
snow sql -q "DESCRIBE TABLE MARKETDATA.RAW.OHLCV"
```

If `snow` is not found, check `requirements/ingestion.txt` and install via `pip install -r requirements/ingestion.txt`.
