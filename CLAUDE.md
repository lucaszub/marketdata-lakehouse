# CLAUDE.md — Stockerize Project

## Contexte du Projet
Pipeline de données financières end-to-end.
**Stack cible :** Airflow · dbt · Snowflake · Terraform · Docker · Streamlit

## Phase Actuelle : Sprint 1 — Ingestion Locale ✓ TERMINÉ

### Objectifs Sprint 1
1. ✓ Maîtriser `yfinance` : comprendre ce qu'on peut extraire et ses limites
2. ✓ Écrire un script d'ingestion robuste pour 19 tickers (+ validation)
3. ✓ Sortir un fichier CSV propre prêt pour un futur chargement en warehouse

### Format de sortie
- **CSV** — fichier nommé `data/raw_YYYYMMDD_HHMMSS.csv`
- 8 colonnes : `timestamp, ticker, open, high, low, close, volume, currency, ingested_at`
- Un fichier par run (pas d'écrasement)

### Actifs cibles (21 symboles)
Liste issue du watchlist de référence. Colonne "Symbole" = ticker plateforme, colonne "yfinance" = ticker à utiliser dans le code.

| Symbole | Nom | Catégorie | yfinance ticker |
|:---|:---|:---|:---|
| XEON | Xtrackers II EUR Overnight Rate Swap UCITS ETF | ETF Monétaire | XEON.DE |
| US10Y | Obligations gouvernement américain 10 ans | Taux | ^TNX |
| US02Y | Obligations gouvernement américain 2 ans | Taux | ^IRX |
| UKOIL | CFD sur Pétrole brut Brent | Commodité | BZ=F |
| SXXP | STOXX 600 | Indice | ^STOXX |
| SX5E | Indice Euro Stoxx 50 | Indice | ^STOXX50E |
| SPY | State Street SPDR S&P 500 ETF | ETF Actions | SPY |
| QQQ | Invesco QQQ Trust Series I | ETF Actions | QQQ |
| NVDA | NVIDIA Corporation | Action | NVDA |
| MSFT | Microsoft Corporation | Action | MSFT |
| IWDA | iShares Core MSCI World UCITS ETF | ETF Actions | IWDA.AS |
| IBM | International Business Machines | Action | IBM |
| GOOGL | Alphabet Inc (Google) Class A | Action | GOOGL |
| GIB.A | CGI Inc. Class A | Action | GIB-A.TO |
| FR10Y | France Obligations gouvernement 10 ans | Taux | À confirmer |
| FR02Y | France 2 Year Government Bond Yield | Taux | À confirmer |
| EURUSD | Euro / Dollar Américain | Forex | EURUSD=X |
| EEM | iShares MSCI Emerging Markets ETF | ETF Actions | EEM |
| CW8 | Amundi MSCI World Swap UCITS ETF | ETF Actions | CW8.PA |
| CAP | Capgemini SE | Action | CAP.PA |
| ACN | Accenture Plc Class A | Action | ACN |

> **Note :** FR10Y et FR02Y sont inclus dans le watchlist mais leur ingestion est **en suspens** (voir section Décisions en attente).

### Contraintes connues
- yfinance peut être bloqué par Yahoo Finance (rate limit, IP ban) → prévoir retry
- Fréquence cible finale : toutes les 15 minutes (batch)
- Budget infra : économiser sans nécessairement utiliser le Free Tier

## Ce qu'on NE fait PAS en Sprint 1
- Pas de Snowflake, pas de dbt, pas de Terraform, pas de Streamlit
- Pas de Docker encore (optionnel à la fin du sprint)
- Pas d'Airflow (le scheduling vient au sprint suivant)

## Conventions de Code
- Python 3.x, dépendances dans `requirements.txt`
- Variables d'environnement dans `.env` (jamais hardcodées)
- Pas de print statements en production, utiliser `logging`

## Fichiers du Projet
- `extract.py` : script d'ingestion en cours de développement
- `requirements.txt` : dépendances Python

## Décisions en attente

### FR10Y / FR02Y — Source de données pour les taux français
**Problème :** Ces deux tickers ne sont pas disponibles via yfinance.
**Options identifiées :**
1. API Banque de France (source officielle, gratuite)
2. Les remplacer par les équivalents US (`^TNX` pour 10 ans, `^IRX` pour 2 ans)
3. Les exclure du pipeline pour l'instant

**Statut :** À décider avant Sprint 2. Ne pas bloquer le Sprint 1 sur ce point.
