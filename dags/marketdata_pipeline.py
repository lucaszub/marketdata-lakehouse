from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="marketdata_pipeline",
    schedule="*/15 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["marketdata"],
    doc_md="""
## Market Data Pipeline

Ingestion toutes les 15 minutes pour 19 actifs financiers.

**Flux :** `yfinance → CSV → Snowflake RAW.OHLCV → dbt → ANALYTICS`

### Tâches
- **extract** : appel yfinance → `data/raw_*.csv`
- **load** : CSV → Snowflake `RAW.OHLCV`
- **transform** : dbt run → `ANALYTICS` (stg_ohlcv, ohlcv_daily, latest_prices)
- **cleanup** : supprime les CSV de plus de 24h
""",
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="""
            echo "=== EXTRACT START ===" &&
            echo "Timestamp: $(date -u)" &&
            cd /opt/airflow && python extract.py &&
            echo "=== CSV FILES ===" &&
            ls -lht data/raw_*.csv | head -3 &&
            echo "=== ROW COUNT ===" &&
            wc -l data/raw_*.csv | tail -1 &&
            echo "=== EXTRACT END ==="
        """,
        doc_md="Récupère les données OHLCV pour 19 tickers via yfinance.",
    )

    load = BashOperator(
        task_id="load",
        bash_command="""
            echo "=== LOAD START ===" &&
            echo "Timestamp: $(date -u)" &&
            cd /opt/airflow && python load.py &&
            echo "=== LOAD END ==="
        """,
        doc_md="Charge le dernier CSV dans Snowflake RAW.OHLCV.",
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="""
            echo "=== TRANSFORM START ===" &&
            echo "Timestamp: $(date -u)" &&
            cd /opt/airflow/marketdata && /home/airflow/.local/bin/dbt run --profiles-dir . &&
            echo "=== TRANSFORM END ==="
        """,
        doc_md="Lance dbt pour rafraîchir ANALYTICS (stg_ohlcv, ohlcv_daily, latest_prices).",
    )

    cleanup = BashOperator(
        task_id="cleanup",
        bash_command="""
            echo "=== CLEANUP START ===" &&
            find /opt/airflow/data -name "raw_*.csv" -mmin +1440 -delete &&
            echo "CSV older than 24h deleted" &&
            ls /opt/airflow/data/ &&
            echo "=== CLEANUP END ==="
        """,
        doc_md="Supprime les fichiers CSV de plus de 24h.",
    )

    extract >> load >> transform >> cleanup
