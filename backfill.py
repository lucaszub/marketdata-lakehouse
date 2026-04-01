import logging
import os

import pandas as pd
import snowflake.connector
import yfinance as yf
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger(__name__)

TICKERS = {
    "XEON.DE": "EUR", "^TNX": "USD", "^IRX": "USD", "BZ=F": "USD",
    "^STOXX": "EUR", "^STOXX50E": "EUR", "SPY": "USD", "QQQ": "USD",
    "NVDA": "USD", "MSFT": "USD", "IWDA.AS": "EUR", "IBM": "USD",
    "GOOGL": "USD", "GIB-A.TO": "CAD", "EURUSD=X": "USD", "EEM": "USD",
    "CW8.PA": "EUR", "CAP.PA": "EUR", "ACN": "USD",
}


def fetch_history(ticker: str, currency: str) -> pd.DataFrame | None:
    df = yf.Ticker(ticker).history(period="2y", interval="1d")
    if df.empty:
        log.warning("[SKIP] %s — no data", ticker)
        return None
    df = df.reset_index()[["Date", "Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["TIMESTAMP", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
    df["TICKER"] = ticker
    df["CURRENCY"] = currency
    df["INGESTED_AT"] = pd.Timestamp.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    log.info("[OK]   %-12s  %d lignes", ticker, len(df))
    return df


def run():
    frames = [fetch_history(t, c) for t, c in TICKERS.items()]
    result = pd.concat([f for f in frames if f is not None], ignore_index=True)
    log.info("Total : %d lignes — chargement Snowflake...", len(result))

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )
    success, _, nrows, _ = write_pandas(conn, result, table_name="OHLCV")
    conn.close()
    log.info("Chargement OK — %d lignes insérées", nrows)


if __name__ == "__main__":
    run()
