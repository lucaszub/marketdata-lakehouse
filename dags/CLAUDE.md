# dags/

## Rôle
Contient les DAGs Airflow orchestrant le pipeline de données.

## DAG : marketdata_pipeline

| Paramètre | Valeur |
|:---|:---|
| Fichier | `marketdata_pipeline.py` |
| Schedule | `*/15 * * * *` (toutes les 15 minutes) |
| Start date | 2026-01-01 |
| Catchup | False |

## Tâches

```
extract  →  load
```

| Tâche | Commande | Résultat attendu |
|:---|:---|:---|
| `extract` | `python extract.py` | Nouveau fichier `data/raw_*.csv` (~380 lignes) |
| `load` | `python load.py` | Insertion dans `MARKETDATA.RAW.OHLCV` |

## Environnement d'exécution

Les scripts tournent dans le container Airflow avec :
- Working directory : `/opt/airflow`
- `extract.py` et `load.py` montés via volume Docker
- Variables `SNOWFLAKE_*` injectées depuis `.env` via `docker-compose.yml`

## Déclencher manuellement (UI Airflow)

1. Ouvrir `http://$VPS_HOST:8080` (admin / admin)
2. Activer le DAG `marketdata_pipeline`
3. Cliquer "Trigger DAG"

## Ajouter un nouveau DAG

1. Créer `dags/nom_du_dag.py`
2. Il apparaît automatiquement dans l'UI (volume monté)
