---
description: Run yfinance ingestion pipeline — fetch OHLCV data for 19 tickers and output CSV
allowed-tools: Bash, Read
---

Run the extraction pipeline and verify the output.

```bash
source venv/bin/activate && python extract.py
```

Then verify:
1. A new `data/raw_YYYYMMDD_HHMMSS.csv` file was created
2. All 19 tickers show `[OK]` in logs — report any `[FAIL]`
3. Check row count (expected ~380-420 rows depending on market hours)
