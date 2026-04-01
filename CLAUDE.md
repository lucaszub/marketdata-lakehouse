# marketData-Lakehouse

## Projet
Pipeline de données financières de bout en bout.
Collecte des données OHLCV toutes les 15 minutes pour 19 actifs (actions, ETF, indices, matières premières, FX)
via yfinance, les stocke dans Snowflake, et les expose dans un dashboard Streamlit.
Orchestré par Airflow sur un VPS, infrastructure provisionnée via Terraform.

## Architecture

```
yfinance (19 tickers)
    ↓ extract.py  →  data/raw_*.csv
    ↓ load.py     →  Snowflake RAW.OHLCV
    ↓ dbt         →  Snowflake ANALYTICS  (Sprint 5)
    ↓ app.py      →  Streamlit (Azure Container Apps)

Orchestration : Airflow sur VPS Hostinger (Docker Compose)
IaC           : Terraform (Snowflake + Azure)
Déploiement   : Ansible (VPS) + scripts/ (ACR + deploy)
```

## Sprints

| Sprint | Scope | Statut |
|:---|:---|:---|
| 1 | Ingestion locale (extract.py, 19 tickers, CSV) | ✓ |
| 2 | Snowflake (Terraform + load.py) | ✓ |
| 3 | Streamlit sur Azure Container Apps | ✓ |
| 4 | Airflow sur VPS Hostinger | 🚀 |
| 5 | dbt (RAW → ANALYTICS) | ⏳ |

## Navigation par dossier

| Dossier | Rôle | Contexte détaillé |
|:---|:---|:---|
| `terraform/` | IaC Snowflake + Azure | `terraform/CLAUDE.md` |
| `ansible/` | Provisioning VPS | `ansible/CLAUDE.md` |
| `dags/` | DAG Airflow | `dags/CLAUDE.md` |
| `docker/` | Images Docker | `docker/CLAUDE.md` |
| `scripts/` | Scripts de déploiement | `scripts/CLAUDE.md` |
| `requirements/` | Dépendances par service | `requirements/CLAUDE.md` |

## Skills disponibles

| Skill | Action |
|:---|:---|
| `/extract` | Lancer l'ingestion yfinance |
| `/load` | Charger le dernier CSV dans Snowflake |
| `/snowflake` | Requêter Snowflake (snow CLI) |
| `/deploy` | Déployer sur le VPS (git push + docker compose) |

## Commandes clés

```bash
source venv/bin/activate
python extract.py                  # ingestion → data/raw_*.csv
python load.py                     # CSV → Snowflake RAW.OHLCV
python validate_tickers.py         # validation one-shot des 19 tickers
./scripts/deploy.sh                # git push + deploy VPS
./scripts/push_to_acr.sh           # push image Streamlit → Azure ACR
```

## Conventions

- Dépendances : toujours mettre à jour `requirements/<service>.txt` avant d'installer
- Secrets : `.env` uniquement, jamais dans le code
- Logs : module `logging`, pas de `print`, en anglais
- Code : minimal, sans commentaires superflus

## Fichiers racine

| Fichier | Rôle |
|:---|:---|
| `extract.py` | Ingestion yfinance → CSV |
| `load.py` | CSV → Snowflake RAW.OHLCV |
| `app.py` | Dashboard Streamlit |
| `validate_tickers.py` | Validation one-shot (19 tickers) |
| `docker-compose.yml` | Stack Airflow (locale + VPS) |
| `.env` | Credentials (ne pas modifier via Claude) |
| `.env.example` | Template public |

## Actifs (19 tickers)

| yfinance | Nom | Devise |
|:---|:---|:---|
| XEON.DE | Xtrackers EUR Overnight ETF | EUR |
| ^TNX | US 10Y Treasury | USD |
| ^IRX | US 2Y Treasury | USD |
| BZ=F | Brent Crude | USD |
| ^STOXX | STOXX 600 | EUR |
| ^STOXX50E | Euro Stoxx 50 | EUR |
| SPY | S&P 500 ETF | USD |
| QQQ | Nasdaq 100 ETF | USD |
| NVDA | NVIDIA | USD |
| MSFT | Microsoft | USD |
| IWDA.AS | iShares MSCI World | EUR |
| IBM | IBM | USD |
| GOOGL | Alphabet | USD |
| GIB-A.TO | CGI Inc. | CAD |
| EURUSD=X | EUR/USD | USD |
| EEM | MSCI Emerging Markets | USD |
| CW8.PA | Amundi MSCI World | EUR |
| CAP.PA | Capgemini | EUR |
| ACN | Accenture | USD |

> FR10Y / FR02Y : non disponibles via yfinance — décision en attente avant Sprint 5
