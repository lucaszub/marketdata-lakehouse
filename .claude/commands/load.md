---
description: Load latest CSV into Snowflake table MARKETDATA.RAW.OHLCV
allowed-tools: Bash
---

Load the latest extracted CSV into Snowflake.

```bash
source venv/bin/activate && python load.py
```

Verify the log shows `rows inserted into OHLCV`. If connection fails, check `.env` has:
- `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_WAREHOUSE=MARKETDATA_WH`
- `SNOWFLAKE_DATABASE=MARKETDATA`, `SNOWFLAKE_SCHEMA=RAW`
