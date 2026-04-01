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

**Flux :** `yfinance → CSV → Snowflake (MARKETDATA.RAW.OHLCV)`

### Tâches
- **extract** : appel yfinance pour 19 tickers → fichier `data/raw_*.csv`
- **load** : chargement du CSV dans Snowflake
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
        doc_md="Récupère les données OHLCV pour 19 tickers via yfinance et génère un CSV horodaté.",
    )

    load = BashOperator(
        task_id="load",
        bash_command="""
            echo "=== LOAD START ===" &&
            echo "Timestamp: $(date -u)" &&
            cd /opt/airflow && python load.py &&
            echo "=== LOAD END ==="
        """,
        doc_md="Charge le dernier CSV dans Snowflake (MARKETDATA.RAW.OHLCV).",
    )

    extract >> load
