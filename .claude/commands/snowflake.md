Query Snowflake using the `snow` CLI. Use this to explore tables, run SQL, debug data issues.

## Prérequis
Verify snow CLI is available:
```bash
snow --version
```

If not installed: add `snowflake-cli` to requirements and install it.

## Tâches courantes

**Lister les tables RAW :**
```bash
snow sql -q "SHOW TABLES IN SCHEMA MARKETDATA.RAW"
```

**Compter les lignes dans OHLCV :**
```bash
snow sql -q "SELECT COUNT(*) FROM MARKETDATA.RAW.OHLCV"
```

**Voir les dernières données insérées :**
```bash
snow sql -q "SELECT * FROM MARKETDATA.RAW.OHLCV ORDER BY INGESTED_AT DESC LIMIT 20"
```

**Vérifier les tickers présents :**
```bash
snow sql -q "SELECT TICKER, COUNT(*) as n FROM MARKETDATA.RAW.OHLCV GROUP BY TICKER ORDER BY TICKER"
```

**Décrire la table OHLCV :**
```bash
snow sql -q "DESCRIBE TABLE MARKETDATA.RAW.OHLCV"
```

**Requête custom :**
Run the SQL query described in $ARGUMENTS against Snowflake and interpret the results.
