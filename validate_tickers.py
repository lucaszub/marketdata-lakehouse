import yfinance as yf
import pandas as pd

# FR10Y et FR02Y exclus (en suspens)
TICKERS = {
    "XEON.DE":   "Xtrackers EUR Overnight Rate ETF",
    "^TNX":      "US 10Y Treasury Yield",
    "^IRX":      "US 2Y Treasury Yield",
    "BZ=F":      "Pétrole brut Brent",
    "^STOXX":    "STOXX 600",
    "^STOXX50E": "Euro Stoxx 50",
    "SPY":       "S&P 500 ETF",
    "QQQ":       "Nasdaq 100 ETF",
    "NVDA":      "NVIDIA",
    "MSFT":      "Microsoft",
    "IWDA.AS":   "iShares MSCI World ETF",
    "IBM":       "IBM",
    "GOOGL":     "Alphabet (Google)",
    "GIB-A.TO":  "CGI Inc.",
    "EURUSD=X":  "Euro / Dollar",
    "EEM":       "MSCI Emerging Markets ETF",
    "CW8.PA":    "Amundi MSCI World ETF",
    "CAP.PA":    "Capgemini",
    "ACN":       "Accenture",
}

OK    = []
FAIL  = []

print(f"\n{'='*65}")
print(f"  Validation des tickers yfinance — {len(TICKERS)} actifs")
print(f"{'='*65}\n")

for ticker, name in TICKERS.items():
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="15m")
        if df.empty:
            raise ValueError("DataFrame vide")
        rows = len(df)
        currency = yf.Ticker(ticker).fast_info.get("currency", "N/A")
        print(f"  [OK]   {ticker:<14} {name:<35} {rows:>3} lignes  ({currency})")
        OK.append(ticker)
    except Exception as e:
        print(f"  [FAIL] {ticker:<14} {name:<35} -> {e}")
        FAIL.append(ticker)

print(f"\n{'='*65}")
print(f"  Résultat : {len(OK)} OK  /  {len(FAIL)} FAIL")
if FAIL:
    print(f"  Tickers en échec : {', '.join(FAIL)}")
print(f"{'='*65}\n")
