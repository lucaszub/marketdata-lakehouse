import os
from datetime import date, timedelta

import pandas as pd
import plotly.graph_objects as go
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Market Data", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #131722; color: #d1d4dc; }
    .stSelectbox label, .stMetric label { color: #787b86 !important; }
    div[data-testid="metric-container"] {
        background-color: #1e222d;
        border: 1px solid #2a2e39;
        border-radius: 6px;
        padding: 12px 16px;
    }
    div[data-testid="metric-container"] > div { color: #d1d4dc; }
    .period-btn button {
        background-color: #1e222d;
        color: #787b86;
        border: 1px solid #2a2e39;
        border-radius: 4px;
        font-size: 12px;
    }
    .block-container { padding-top: 1.5rem; }
    hr { border-color: #2a2e39; }
</style>
""", unsafe_allow_html=True)


def get_conn():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database="MARKETDATA",
        schema="ANALYTICS",
        role=os.getenv("SNOWFLAKE_ROLE"),
    )


@st.cache_data(ttl=900)
def load_intraday() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql(
        "SELECT TIMESTAMP, TICKER, OPEN, HIGH, LOW, CLOSE, VOLUME, CURRENCY "
        "FROM MARKETDATA.ANALYTICS.STG_OHLCV ORDER BY TIMESTAMP",
        conn,
    )
    conn.close()
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    return df


@st.cache_data(ttl=900)
def load_daily() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql(
        "SELECT DATE, TICKER, OPEN, HIGH, LOW, CLOSE, VOLUME, CURRENCY "
        "FROM MARKETDATA.ANALYTICS.OHLCV_DAILY ORDER BY DATE",
        conn,
    )
    conn.close()
    df["DATE"] = pd.to_datetime(df["DATE"])
    return df


@st.cache_data(ttl=900)
def load_latest() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql(
        "SELECT TICKER, LAST_PRICE, LAST_UPDATED, CURRENCY "
        "FROM MARKETDATA.ANALYTICS.LATEST_PRICES",
        conn,
    )
    conn.close()
    return df


TICKER_META = {
    "XEON.DE":   {"name": "Xtrackers EUR Overnight Rate Swap ETF", "type": "ETF",        "exchange": "XETRA"},
    "^TNX":      {"name": "US 10-Year Treasury Yield",             "type": "Bond",       "exchange": "CBOE"},
    "^IRX":      {"name": "US 13-Week Treasury Bill",              "type": "Bond",       "exchange": "CBOE"},
    "BZ=F":      {"name": "Brent Crude Oil",                       "type": "Commodity",  "exchange": "NYMEX"},
    "^STOXX":    {"name": "STOXX Europe 600",                      "type": "Index",      "exchange": "STOXX"},
    "^STOXX50E": {"name": "Euro Stoxx 50",                         "type": "Index",      "exchange": "STOXX"},
    "SPY":       {"name": "SPDR S&P 500 ETF Trust",                "type": "ETF",        "exchange": "NYSE"},
    "QQQ":       {"name": "Invesco QQQ Trust (Nasdaq 100)",        "type": "ETF",        "exchange": "NASDAQ"},
    "NVDA":      {"name": "NVIDIA Corporation",                    "type": "Stock",      "exchange": "NASDAQ"},
    "MSFT":      {"name": "Microsoft Corporation",                 "type": "Stock",      "exchange": "NASDAQ"},
    "IWDA.AS":   {"name": "iShares Core MSCI World ETF",           "type": "ETF",        "exchange": "Euronext"},
    "IBM":       {"name": "IBM Corporation",                       "type": "Stock",      "exchange": "NYSE"},
    "GOOGL":     {"name": "Alphabet Inc.",                         "type": "Stock",      "exchange": "NASDAQ"},
    "GIB-A.TO":  {"name": "CGI Inc.",                              "type": "Stock",      "exchange": "TSX"},
    "EURUSD=X":  {"name": "EUR/USD",                               "type": "Forex",      "exchange": "FX"},
    "EEM":       {"name": "iShares MSCI Emerging Markets ETF",     "type": "ETF",        "exchange": "NYSE"},
    "CW8.PA":    {"name": "Amundi MSCI World ETF",                 "type": "ETF",        "exchange": "Euronext"},
    "CAP.PA":    {"name": "Capgemini SE",                          "type": "Stock",      "exchange": "Euronext"},
    "ACN":       {"name": "Accenture plc",                         "type": "Stock",      "exchange": "NYSE"},
}

PERIODS = {
    "1D": 1,
    "5D": 5,
    "1M": 30,
    "3M": 90,
    "6M": 180,
    "YTD": None,
    "1Y": 365,
    "All": None,
}

intraday = load_intraday()
daily = load_daily()
latest = load_latest()

tickers = sorted(intraday["TICKER"].unique())

col_ticker, col_period = st.columns([3, 7])

with col_ticker:
    ticker = st.selectbox("", tickers, label_visibility="collapsed")

with col_period:
    period = st.radio("", list(PERIODS.keys()), horizontal=True, index=2, label_visibility="collapsed")

ticker_latest = latest[latest["TICKER"] == ticker]
currency = ticker_latest["CURRENCY"].iloc[0] if not ticker_latest.empty else ""
meta = TICKER_META.get(ticker, {"name": ticker, "type": "", "exchange": ""})

today = date.today()

if period in ("1D", "5D"):
    df = intraday[intraday["TICKER"] == ticker].copy()
    x_col = "TIMESTAMP"
else:
    df = daily[daily["TICKER"] == ticker].copy()
    x_col = "DATE"

days = PERIODS[period]
if period == "YTD":
    cutoff = pd.Timestamp(today.year, 1, 1)
    df = df[df[x_col] >= cutoff]
elif days:
    cutoff = df[x_col].max() - pd.Timedelta(days=days)
    df = df[df[x_col] >= cutoff]

if df.empty:
    st.warning("Pas de données pour cette période.")
    st.stop()

last_price = df["CLOSE"].iloc[-1]
prev_price = df["CLOSE"].iloc[0]
change = last_price - prev_price
change_pct = (change / prev_price) * 100
color = "#26a69a" if change >= 0 else "#ef5350"

last_row = df.iloc[-1]

st.markdown(
    f"""
    <div style='margin-bottom:4px'>
        <span style='font-size:1.5rem; font-weight:700; color:#d1d4dc'>{ticker}</span>
        <span style='font-size:0.85rem; color:#787b86; margin-left:10px'>{meta['name']}</span>
        <span style='font-size:0.75rem; color:#4c525e; margin-left:8px; border:1px solid #2a2e39; border-radius:3px; padding:1px 6px'>{meta['type']}</span>
        <span style='font-size:0.75rem; color:#4c525e; margin-left:4px; border:1px solid #2a2e39; border-radius:3px; padding:1px 6px'>{meta['exchange']}</span>
        <span style='font-size:0.75rem; color:#4c525e; margin-left:4px; border:1px solid #2a2e39; border-radius:3px; padding:1px 6px'>{currency}</span>
    </div>
    <div style='margin-bottom:8px'>
        <span style='font-size:1.8rem; font-weight:600; color:#d1d4dc'>{last_price:.2f}</span>
        <span style='font-size:1rem; color:{color}; margin-left:8px'>
            {'▲' if change >= 0 else '▼'} {abs(change):.2f} ({abs(change_pct):.2f}%)
        </span>
    </div>
    <div style='font-size:0.78rem; color:#787b86'>
        O&nbsp;<span style='color:#d1d4dc'>{last_row['OPEN']:.2f}</span>&nbsp;&nbsp;
        H&nbsp;<span style='color:#26a69a'>{last_row['HIGH']:.2f}</span>&nbsp;&nbsp;
        L&nbsp;<span style='color:#ef5350'>{last_row['LOW']:.2f}</span>&nbsp;&nbsp;
        C&nbsp;<span style='color:#d1d4dc'>{last_row['CLOSE']:.2f}</span>&nbsp;&nbsp;
        Vol&nbsp;<span style='color:#d1d4dc'>{last_row['VOLUME']:,.0f}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df[x_col],
    open=df["OPEN"],
    high=df["HIGH"],
    low=df["LOW"],
    close=df["CLOSE"],
    increasing_line_color="#26a69a",
    decreasing_line_color="#ef5350",
    increasing_fillcolor="#26a69a",
    decreasing_fillcolor="#ef5350",
    name=ticker,
))

fig.update_layout(
    paper_bgcolor="#131722",
    plot_bgcolor="#131722",
    font=dict(color="#787b86", size=11),
    xaxis=dict(
        gridcolor="#1e222d",
        linecolor="#2a2e39",
        rangeslider=dict(visible=False),
        type="date",
    ),
    yaxis=dict(
        gridcolor="#1e222d",
        linecolor="#2a2e39",
        side="right",
    ),
    margin=dict(l=0, r=60, t=20, b=20),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#1e222d", font_color="#d1d4dc"),
    showlegend=False,
    height=500,
)

st.plotly_chart(fig, use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Dernier", f"{last_price:.2f} {currency}")
c2.metric("Variation", f"{change_pct:+.2f}%", delta=f"{change:+.2f}")
c3.metric("Plus haut", f"{df['HIGH'].max():.2f}")
c4.metric("Plus bas", f"{df['LOW'].min():.2f}")
