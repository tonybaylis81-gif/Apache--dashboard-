import streamlit as st
import alpaca_trade_api as tradeapi
import pandas as pd

# Page setup
st.set_page_config(page_title="Trading Dashboard", page_icon="💸", layout="wide")

st.title("💸 Trading Dashboard")
st.markdown("Switch between **Paper** and **Live** trading safely using Alpaca's API.")

# Sidebar controls
st.sidebar.header("⚙️ Trading Settings")
mode = st.sidebar.radio("Select Mode:", ["Paper Trading", "Live Trading"])

# Load API credentials from Streamlit secrets
if mode == "Paper Trading":
    API_KEY = st.secrets["PAPER_API_KEY"]
    API_SECRET = st.secrets["PAPER_API_SECRET"]
    BASE_URL = "https://paper-api.alpaca.markets"
else:
    API_KEY = st.secrets["LIVE_API_KEY"]
    API_SECRET = st.secrets["LIVE_API_SECRET"]
    BASE_URL = "https://api.alpaca.markets"

# Connect to Alpaca API
try:
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    account = api.get_account()
    st.success(f"Connected to {mode}")
except Exception as e:
    st.error(f"Connection failed: {e}")
    st.stop()

# Account overview
st.subheader("📈 Account Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Cash", f"${float(account.cash):,.2f}")
col2.metric("Buying Power", f"${float(account.buying_power):,.2f}")
col3.metric("Portfolio Value", f"${float(account.portfolio_value):,.2f}")

# Positions
st.subheader("📊 Current Positions")
positions = api.list_positions()

if positions:
    df = pd.DataFrame([{
        "Symbol": p.symbol,
        "Qty": p.qty,
        "Market Value ($)": float(p.market_value),
        "Unrealized P/L ($)": float(p.unrealized_pl)
    } for p in positions])
    st.dataframe(df)
else:
    st.info("No open positions found.")

# Trade form
st.sidebar.subheader("💼 Place a Trade")
symbol = st.sidebar.text_input("Symbol", "AAPL").upper()
qty = st.sidebar.number_input("Quantity", min_value=1, step=1)
side = st.sidebar.selectbox("Action", ["Buy", "Sell"])

if st.sidebar.button("Submit Order"):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side.lower(),
            type="market",
            time_in_force="gtc"
        )
        st.success(f"{side} order placed for {qty} shares of {symbol}.")
    except Exception as e:
        st.error(f"Order failed: {e}")
import streamlit as st

st.title("Alpaca Dashboard")
st.write("Welcome to the Alpaca Dashboard!")
# Add your Streamlit components and logic here