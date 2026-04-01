import glob
import logging
import os

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def get_latest_csv() -> str:
    files = glob.glob("data/raw_*.csv")
    if not files:
        raise FileNotFoundError("Aucun fichier CSV dans data/. Lance extract.py d'abord.")
    return max(files)


def load():
    csv_path = get_latest_csv()
    log.info(f"Fichier source : {csv_path}")

    df = pd.read_csv(csv_path)
    df.columns = [c.upper() for c in df.columns]
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], utc=True).dt.tz_convert(None)
    df["INGESTED_AT"] = pd.to_datetime(df["INGESTED_AT"], utc=True).dt.tz_convert(None)
    log.info(f"{len(df)} lignes à charger")

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )

    success, nchunks, nrows, _ = write_pandas(conn, df, table_name="OHLCV")

    if success:
        log.info(f"Chargement OK — {nrows} lignes insérées en {nchunks} chunk(s)")
    else:
        log.error("Échec du chargement")

    conn.close()


if __name__ == "__main__":
    load()
