# terraform/

## Rôle
Provisionne toute l'infrastructure du projet via Terraform :
- **Snowflake** : warehouse, database, schemas (RAW + ANALYTICS), table OHLCV
- **Azure** : resource group, ACR, Log Analytics, Container App Environment, Container App Streamlit

## Fichiers

| Fichier | Contenu |
|:---|:---|
| `main.tf` | Provider Snowflake + toutes les ressources Snowflake |
| `azure.tf` | Provider Azure + toutes les ressources Azure |
| `variables.tf` | Variables requises (account, user, password, subscription_id) |
| `terraform.tfvars` | Valeurs des variables — **jamais dans Git** |

## Ressources Snowflake (main.tf)

```
MARKETDATA_WH          warehouse X-SMALL, auto-suspend 60s, auto-resume
MARKETDATA             database
MARKETDATA.RAW         schema — données brutes (extract.py → load.py)
MARKETDATA.ANALYTICS   schema — données transformées (dbt, Sprint 5)
MARKETDATA.RAW.OHLCV   table — TIMESTAMP, TICKER, OPEN, HIGH, LOW, CLOSE, VOLUME, CURRENCY, INGESTED_AT
```

## Ressources Azure (azure.tf)

```
rg-marketdata                    resource group (westeurope)
marketdataregistry               ACR Basic (admin activé)
log-marketdata                   Log Analytics 30j retention
cae-marketdata                   Container App Environment
ca-marketdata-streamlit          Container App Streamlit
  image  : marketdataregistry.azurecr.io/marketdata-streamlit:latest
  port   : 8501
  CPU    : 0.5 / RAM : 1Gi
  scale  : 0 → 1 replica
  URL    : https://ca-marketdata-streamlit.lemonhill-74405919.westeurope.azurecontainerapps.io
```

## Commandes

```bash
cd terraform

# Voir ce qui va changer
terraform plan

# Appliquer les changements
terraform apply

# Détruire (attention : irréversible)
terraform destroy
```

## Variables requises (terraform.tfvars)

```hcl
snowflake_organization_name = "..."
snowflake_account_name      = "..."
snowflake_account           = "..."
snowflake_user              = "..."
snowflake_password          = "..."
azure_subscription_id       = "..."
```

> `terraform.tfvars` est dans `.gitignore` — ne jamais commiter.
