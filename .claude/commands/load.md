Charge le dernier CSV généré par extract.py dans Snowflake (table MARKETDATA.RAW.OHLCV).

```bash
cd /home/cgi/marketData-Lakehouse
source venv/bin/activate
python load.py
```

Après exécution :
1. Vérifie que le log indique "rows inserted into OHLCV"
2. Si snow CLI est disponible, confirme avec :
   ```bash
   snow sql -q "SELECT COUNT(*) FROM MARKETDATA.RAW.OHLCV"
   ```
3. En cas d'erreur de connexion, vérifie que `.env` contient bien `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_WAREHOUSE=MARKETDATA_WH`
