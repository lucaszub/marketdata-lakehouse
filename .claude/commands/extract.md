Lance le script d'ingestion yfinance et vérifie le résultat.

```bash
cd /home/cgi/marketData-Lakehouse
source venv/bin/activate
python extract.py
```

Après exécution :
1. Vérifie que le fichier `data/raw_*.csv` a bien été créé
2. Vérifie le nombre de lignes (attendu ~398)
3. Vérifie qu'aucun ticker n'est en FAIL dans les logs
4. Affiche les 3 premières lignes du CSV pour confirmer la structure

Si des tickers sont en FAIL, diagnostique la cause (rate limit yfinance, ticker invalide, réseau).
