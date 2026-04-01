FROM apache/airflow:2.9.0

COPY requirements/ingestion.txt /tmp/ingestion.txt
COPY requirements/dbt.txt /tmp/dbt.txt
RUN pip install --no-cache-dir -r /tmp/ingestion.txt -r /tmp/dbt.txt
