import os

import pandas as pd
import plotly.express as px
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Market Data", layout="wide")


@st.cache_data(ttl=900)
def load_data() -> pd.DataFrame:
    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )
    df = pd.read_sql(
        "SELECT TIMESTAMP, TICKER, CLOSE, VOLUME, CURRENCY FROM MARKETDATA.RAW.OHLCV ORDER BY TIMESTAMP",
        conn,
    )
    conn.close()
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    return df


df = load_data()

st.title("Market Data Dashboard")

col1, col2 = st.columns(2)
with col1:
    ticker = st.selectbox("Actif", sorted(df["TICKER"].unique()))
with col2:
    period = st.selectbox("Période", ["1J", "5J", "1M", "Max"], index=0)

period_map = {"1J": 1, "5J": 5, "1M": 30, "Max": None}
days = period_map[period]

filtered = df[df["TICKER"] == ticker].copy()
if days:
    cutoff = filtered["TIMESTAMP"].max() - pd.Timedelta(days=days)
    filtered = filtered[filtered["TIMESTAMP"] >= cutoff]

fig = px.line(
    filtered,
    x="TIMESTAMP",
    y="CLOSE",
    title=f"{ticker} — Prix de clôture",
    labels={"TIMESTAMP": "", "CLOSE": f"Close ({filtered['CURRENCY'].iloc[0]})"},
)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Dernier prix", f"{filtered['CLOSE'].iloc[-1]:.2f}")
col2.metric("Plus haut", f"{filtered['CLOSE'].max():.2f}")
col3.metric("Plus bas", f"{filtered['CLOSE'].min():.2f}")
