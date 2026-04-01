# CLAUDE.md — marketData-Lakehouse

## Navigation rapide
- **Où on en est →** `memory/MEMORY.md` (sprints, prochaine étape)
- **Skills disponibles →** `.claude/commands/`
- **Infra Snowflake →** `terraform/`
- **Dépendances →** `requirements/` (un fichier par service)

## Stack
Python · Airflow · dbt · Snowflake · Terraform · Docker · Streamlit

## Sprints
| Sprint | Scope | Statut |
|:---|:---|:---|
| 1 | Ingestion locale (extract.py, 19 tickers, CSV) | ✓ |
| 2 | Snowflake (Terraform + load.py) | ✓ |
| 3 | Streamlit POC (app.py, linechart, ticker/période) | ✓ |
| 4 | Airflow sur VPS + Docker Compose | 🚀 |
| 5 | dbt (RAW → ANALYTICS) | ⏳ |

## Commandes clés
```bash
source venv/bin/activate
python extract.py                        # ingestion → data/raw_*.csv
python load.py                           # CSV → Snowflake RAW.OHLCV
python validate_tickers.py              # validation tickers (one-shot)
cd terraform && terraform plan           # preview infra Snowflake
cd terraform && terraform apply          # appliquer infra Snowflake
```

## Skills (.claude/commands/)
- `/snowflake` — requêter Snowflake (lister tables, compter lignes, SQL custom)
- `/extract` — lancer et monitorer l'ingestion yfinance
- `/load` — charger le dernier CSV dans Snowflake

## Conventions
- Dépendances : toujours mettre à jour `requirements/<service>.txt` avant d'installer
- Secrets : `.env` uniquement, jamais dans le code
- Logs : `logging` module, pas de `print`
- Code : minimal, sans commentaires superflus, logs en anglais

## Fichiers clés
| Fichier | Rôle |
|:---|:---|
| `extract.py` | Ingestion yfinance → CSV |
| `load.py` | CSV → Snowflake |
| `validate_tickers.py` | Validation one-shot des tickers |
| `terraform/main.tf` | Infrastructure Snowflake |
| `.env` | Credentials (ne pas toucher via Claude) |
| `.env.example` | Template public |

## Actifs (19 tickers actifs)
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

> FR10Y / FR02Y : en suspens (non disponibles via yfinance)

## Décisions en attente
- **FR10Y/FR02Y** : API Banque de France vs exclure vs remplacer par ^TNX/^IRX → avant Sprint 4
- **Streamlit hébergement** : VPS Hostinger vs Streamlit Cloud → à décider Sprint 3
