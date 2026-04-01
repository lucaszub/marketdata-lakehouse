# requirements/

## Règle absolue
Toujours mettre à jour le bon fichier `requirements/<service>.txt` **avant** d'installer un paquet.
Ne jamais mélanger les dépendances entre services.

## Fichiers

| Fichier | Utilisé par | Image Docker |
|:---|:---|:---|
| `ingestion.txt` | `extract.py`, `load.py` | `docker/airflow/Dockerfile` |
| `streamlit.txt` | `app.py` | `Dockerfile` (racine) |
| `airflow.txt` | Référence uniquement | — |
| `dbt.txt` | Sprint 5 (dbt) | À créer |

## Ajouter une dépendance

```bash
# 1. Ajouter dans le bon fichier
echo "nom-du-paquet" >> requirements/ingestion.txt

# 2. Installer dans le venv local
pip install -r requirements/ingestion.txt

# 3. Rebuilder l'image si nécessaire
./scripts/deploy.sh   # pour Airflow
./scripts/push_to_acr.sh  # pour Streamlit
```
