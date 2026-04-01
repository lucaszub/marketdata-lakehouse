# docker/

## Rôle
Contient les Dockerfiles pour les services du projet.

## Fichiers

| Fichier | Service | Base image |
|:---|:---|:---|
| `airflow/Dockerfile` | Airflow (scheduler + webserver) | `apache/airflow:2.9.0` |

> Le Dockerfile Streamlit est à la racine du projet (`/Dockerfile`).

## airflow/Dockerfile

```dockerfile
FROM apache/airflow:2.9.0
COPY requirements/ingestion.txt /tmp/ingestion.txt
RUN pip install --no-cache-dir -r /tmp/ingestion.txt
```

Ajoute les dépendances d'ingestion (yfinance, pandas, snowflake-connector, python-dotenv)
à l'image Airflow officielle.

## Dockerfile (racine — Streamlit)

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements/streamlit.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Déployée sur Azure Container Apps via `scripts/push_to_acr.sh`.

## Rebuild après changement de dépendances

```bash
# Airflow (via VPS)
./scripts/deploy.sh   # git push + docker compose up -d --build

# Streamlit (Azure Container Apps)
./scripts/push_to_acr.sh
```
