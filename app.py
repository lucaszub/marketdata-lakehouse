import os
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Market Data", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none; }
    .block-container { padding-top: 1.5rem; }
    div[data-testid="metric-container"] {
        background-color: #1e222d;
        border: 1px solid #2a2e39;
        border-radius: 6px;
        padding: 12px 16px;
    }
    div[data-baseweb="select"] > div {
        background-color: #1e222d !important;
        border: 1px solid #434651 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] > div:hover { border-color: #787b86 !important; }
    div[data-baseweb="select"] span { color: #d1d4dc !important; font-weight: 600 !important; }
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label {
        background-color: #1e222d;
        border: 1px solid #2a2e39;
        border-radius: 4px;
        padding: 2px 10px;
        color: #787b86;
        font-size: 0.8rem;
    }
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #2962ff;
        border-color: #2962ff;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

TICKER_META = {
    "XEON.DE":   {"name": "Xtrackers EUR Overnight Rate Swap ETF", "type": "ETF",       "exchange": "XETRA"},
    "^TNX":      {"name": "US 10-Year Treasury Yield",             "type": "Bond",      "exchange": "CBOE"},
    "^IRX":      {"name": "US 13-Week Treasury Bill",              "type": "Bond",      "exchange": "CBOE"},
    "BZ=F":      {"name": "Brent Crude Oil",                       "type": "Commodity", "exchange": "NYMEX"},
    "^STOXX":    {"name": "STOXX Europe 600",                      "type": "Index",     "exchange": "STOXX"},
    "^STOXX50E": {"name": "Euro Stoxx 50",                         "type": "Index",     "exchange": "STOXX"},
    "SPY":       {"name": "SPDR S&P 500 ETF Trust",                "type": "ETF",       "exchange": "NYSE"},
    "QQQ":       {"name": "Invesco QQQ Trust (Nasdaq 100)",        "type": "ETF",       "exchange": "NASDAQ"},
    "NVDA":      {"name": "NVIDIA Corporation",                    "type": "Stock",     "exchange": "NASDAQ"},
    "MSFT":      {"name": "Microsoft Corporation",                 "type": "Stock",     "exchange": "NASDAQ"},
    "IWDA.AS":   {"name": "iShares Core MSCI World ETF",           "type": "ETF",       "exchange": "Euronext"},
    "IBM":       {"name": "IBM Corporation",                       "type": "Stock",     "exchange": "NYSE"},
    "GOOGL":     {"name": "Alphabet Inc.",                         "type": "Stock",     "exchange": "NASDAQ"},
    "GIB-A.TO":  {"name": "CGI Inc.",                              "type": "Stock",     "exchange": "TSX"},
    "EURUSD=X":  {"name": "EUR/USD",                               "type": "Forex",     "exchange": "FX"},
    "EEM":       {"name": "iShares MSCI Emerging Markets ETF",     "type": "ETF",       "exchange": "NYSE"},
    "CW8.PA":    {"name": "Amundi MSCI World ETF",                 "type": "ETF",       "exchange": "Euronext"},
    "CAP.PA":    {"name": "Capgemini SE",                          "type": "Stock",     "exchange": "Euronext"},
    "ACN":       {"name": "Accenture plc",                         "type": "Stock",     "exchange": "NYSE"},
}

PERIODS = {"1D": 1, "5D": 5, "1M": 30, "3M": 90, "6M": 180, "YTD": -1, "1Y": 365, "2Y": 730}


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
        "FROM MARKETDATA.ANALYTICS.STG_OHLCV ORDER BY TIMESTAMP", conn)
    conn.close()
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    return df


@st.cache_data(ttl=900)
def load_daily() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql(
        "SELECT DATE, TICKER, OPEN, HIGH, LOW, CLOSE, VOLUME, CURRENCY "
        "FROM MARKETDATA.ANALYTICS.OHLCV_DAILY ORDER BY DATE", conn)
    conn.close()
    df["DATE"] = pd.to_datetime(df["DATE"])
    return df


intraday = load_intraday()
daily = load_daily()
tickers = sorted(daily["TICKER"].unique())

st.markdown("<h2 style='color:#d1d4dc; margin-bottom:0.5rem'>📈 Market Data</h2>", unsafe_allow_html=True)

col_ticker, col_period = st.columns([3, 7])
with col_ticker:
    ticker = st.selectbox("", tickers, label_visibility="collapsed")
with col_period:
    period = st.radio("", list(PERIODS.keys()), horizontal=True, index=2, label_visibility="collapsed")

# Choisir la source selon la période
if period in ("1D", "5D"):
    src = intraday[intraday["TICKER"] == ticker].copy()
    x_col = "TIMESTAMP"
else:
    src = daily[daily["TICKER"] == ticker].copy()
    x_col = "DATE"

# Filtrer selon la période
days = PERIODS[period]
if period == "YTD":
    src = src[src[x_col] >= pd.Timestamp(date.today().year, 1, 1)]
elif days > 0:
    src = src[src[x_col] >= src[x_col].max() - pd.Timedelta(days=days)]

if src.empty:
    st.warning("Pas de données pour cette période.")
    st.stop()

currency = src["CURRENCY"].iloc[0]
meta = TICKER_META.get(ticker, {"name": ticker, "type": "", "exchange": ""})
last = src.iloc[-1]
change = last["CLOSE"] - src.iloc[0]["CLOSE"]
change_pct = (change / src.iloc[0]["CLOSE"]) * 100
color = "#26a69a" if change >= 0 else "#ef5350"

st.markdown(f"""
<div style='margin-bottom:4px'>
    <span style='font-size:1.4rem; font-weight:700; color:#d1d4dc'>{ticker}</span>
    <span style='font-size:0.85rem; color:#787b86; margin-left:10px'>{meta['name']}</span>
    <span style='font-size:0.75rem; color:#4c525e; margin-left:8px; border:1px solid #2a2e39; border-radius:3px; padding:1px 6px'>{meta['type']}</span>
    <span style='font-size:0.75rem; color:#4c525e; margin-left:4px; border:1px solid #2a2e39; border-radius:3px; padding:1px 6px'>{meta['exchange']}</span>
    <span style='font-size:0.75rem; color:#4c525e; margin-left:4px; border:1px solid #2a2e39; border-radius:3px; padding:1px 6px'>{currency}</span>
</div>
<div style='margin-bottom:6px'>
    <span style='font-size:1.8rem; font-weight:600; color:#d1d4dc'>{last['CLOSE']:.2f}</span>
    <span style='font-size:1rem; color:{color}; margin-left:8px'>
        {'▲' if change >= 0 else '▼'} {abs(change):.2f} ({abs(change_pct):.2f}%)
    </span>
</div>
<div style='font-size:0.78rem; color:#787b86; margin-bottom:12px'>
    O&nbsp;<span style='color:#d1d4dc'>{last['OPEN']:.2f}</span>&nbsp;&nbsp;
    H&nbsp;<span style='color:#26a69a'>{last['HIGH']:.2f}</span>&nbsp;&nbsp;
    L&nbsp;<span style='color:#ef5350'>{last['LOW']:.2f}</span>&nbsp;&nbsp;
    C&nbsp;<span style='color:#d1d4dc'>{last['CLOSE']:.2f}</span>&nbsp;&nbsp;
    Vol&nbsp;<span style='color:#d1d4dc'>{last['VOLUME']:,.0f}</span>
</div>
""", unsafe_allow_html=True)

fig = go.Figure(go.Candlestick(
    x=src[x_col],
    open=src["OPEN"], high=src["HIGH"], low=src["LOW"], close=src["CLOSE"],
    increasing_line_color="#26a69a", decreasing_line_color="#ef5350",
    increasing_fillcolor="#26a69a", decreasing_fillcolor="#ef5350",
    name=ticker,
))
fig.update_layout(
    paper_bgcolor="#131722", plot_bgcolor="#131722",
    font=dict(color="#787b86", size=11),
    xaxis=dict(gridcolor="#1e222d", linecolor="#2a2e39", rangeslider=dict(visible=False)),
    yaxis=dict(gridcolor="#1e222d", linecolor="#2a2e39", side="right"),
    margin=dict(l=0, r=60, t=10, b=20),
    hovermode="x unified", hoverlabel=dict(bgcolor="#1e222d", font_color="#d1d4dc"),
    showlegend=False, height=500,
)
st.plotly_chart(fig, use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Dernier", f"{last['CLOSE']:.2f} {currency}")
c2.metric("Variation", f"{change_pct:+.2f}%", delta=f"{change:+.2f}")
c3.metric("Plus haut", f"{src['HIGH'].max():.2f}")
c4.metric("Plus bas", f"{src['LOW'].min():.2f}")
