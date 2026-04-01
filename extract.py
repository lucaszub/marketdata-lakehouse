import logging
import time
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

TICKERS = {
    "XEON.DE":   "EUR",
    "^TNX":      "USD",
    "^IRX":      "USD",
    "BZ=F":      "USD",
    "^STOXX":    "EUR",
    "^STOXX50E": "EUR",
    "SPY":       "USD",
    "QQQ":       "USD",
    "NVDA":      "USD",
    "MSFT":      "USD",
    "IWDA.AS":   "EUR",
    "IBM":       "USD",
    "GOOGL":     "USD",
    "GIB-A.TO":  "CAD",
    "EURUSD=X":  "USD",
    "EEM":       "USD",
    "CW8.PA":    "EUR",
    "CAP.PA":    "EUR",
    "ACN":       "USD",
}

MAX_RETRIES = 3
RETRY_DELAY = 5  # secondes entre chaque retry


def fetch_ticker(ticker: str, currency: str) -> pd.DataFrame | None:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            df = yf.Ticker(ticker).history(period="1d", interval="15m")
            if df.empty:
                raise ValueError("DataFrame vide")

            df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
            df.columns = ["open", "high", "low", "close", "volume"]
            df.index.name = "timestamp"
            df = df.reset_index()

            # Normaliser le timestamp en UTC sans timezone info
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_localize(None)

            df.insert(1, "ticker", ticker)
            df["currency"] = currency
            df["ingested_at"] = datetime.now(timezone.utc).replace(tzinfo=None)

            log.info(f"[OK]   {ticker:<14} {len(df):>3} lignes")
            return df

        except Exception as e:
            log.warning(f"[RETRY {attempt}/{MAX_RETRIES}] {ticker} — {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    log.error(f"[FAIL] {ticker} — abandon après {MAX_RETRIES} tentatives")
    return None


def run():
    log.info(f"Démarrage ingestion — {len(TICKERS)} tickers")
    ingested_at = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    frames = []
    failed = []

    for ticker, currency in TICKERS.items():
        df = fetch_ticker(ticker, currency)
        if df is not None:
            frames.append(df)
        else:
            failed.append(ticker)

    if not frames:
        log.error("Aucune donnée récupérée. Vérifier la connexion ou les tickers.")
        return

    result = pd.concat(frames, ignore_index=True)
    output_path = f"data/raw_{ingested_at}.csv"

    import os
    os.makedirs("data", exist_ok=True)
    result.to_csv(output_path, index=False)

    log.info(f"Export : {output_path}  ({len(result)} lignes, {result['ticker'].nunique()} tickers)")
    if failed:
        log.warning(f"Tickers en échec : {', '.join(failed)}")


if __name__ == "__main__":
    run()
