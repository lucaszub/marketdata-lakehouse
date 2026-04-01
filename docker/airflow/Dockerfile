FROM apache/airflow:2.9.0

COPY requirements/ingestion.txt /tmp/ingestion.txt
RUN pip install --no-cache-dir -r /tmp/ingestion.txt
