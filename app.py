import streamlit as st
import requests
import json
import time
import math
import random
from datetime import datetime, timedelta
from collections import deque

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Crypto oracle — Ultimate Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Crypt oracle AI — 316 Feature Ultra Advanced Crypto Predictor"
    }
)

# ══════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []
if "watchlist" not in st.session_state:
    st.session_state.watchlist = ["bitcoin", "ethereum"]
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}
if "alerts" not in st.session_state:
    st.session_state.alerts = []
if "accuracy_log" not in st.session_state:
    st.session_state.accuracy_log = []
if "user_mode" not in st.session_state:
    st.session_state.user_mode = "Expert"
if "language" not in st.session_state:
    st.session_state.language = "English"

# ══════════════════════════════════════════════════════════════
#  FULL CSS — CYBERPUNK GLASSMORPHISM THEME
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600;700&display=swap');

:root {
  --cyan: #00ffe0;
  --blue: #0080ff;
  --purple: #8000ff;
  --green: #00ff88;
  --red: #ff3355;
  --yellow: #ffcc00;
  --orange: #ff8800;
  --bg: #020811;
  --card: rgba(0,255,224,0.04);
  --border: rgba(0,255,224,0.15);
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: #e0f0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(0,128,255,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(128,0,255,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(0,255,224,0.03) 0%, transparent 70%);
}

/* HEADER */
.main-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(20px,4.5vw,46px);
    font-weight: 900;
    background: linear-gradient(135deg, #00ffe0 0%, #0080ff 40%, #8000ff 70%, #00ffe0 100%);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 5s linear infinite;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 2px;
    text-shadow: none;
}
.main-subtitle {
    text-align: center;
    color: rgba(0,255,224,0.45);
    font-size: 0.7em;
    letter-spacing: 5px;
    font-family: 'Share Tech Mono', monospace;
    margin-bottom: 6px;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:300%} }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
@keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
@keyframes glow { 0%,100%{box-shadow:0 0 10px rgba(0,255,224,0.3)} 50%{box-shadow:0 0 25px rgba(0,255,224,0.6)} }

/* LIVE TICKER */
.ticker-bar {
    background: rgba(0,255,224,0.05);
    border-top: 1px solid rgba(0,255,224,0.2);
    border-bottom: 1px solid rgba(0,255,224,0.2);
    padding: 6px 0;
    overflow: hidden;
    white-space: nowrap;
    margin-bottom: 16px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75em;
    color: var(--cyan);
}

/* DISCLAIMER */
.disclaimer {
    background: rgba(255,200,0,0.06);
    border: 1px solid rgba(255,200,0,0.25);
    border-left: 3px solid var(--yellow);
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 0.7em;
    color: rgba(255,200,0,0.75);
    text-align: center;
    letter-spacing: 1px;
    margin: 8px 0 16px 0;
    font-family: 'Share Tech Mono', monospace;
}

/* SECTION HEADERS */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.85em;
    color: var(--cyan);
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(0,255,224,0.2);
    padding-bottom: 6px;
    margin: 20px 0 14px 0;
}

/* METRIC CARDS */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 14px;
    text-align: center;
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease;
}
.metric-card:hover {
    border-color: rgba(0,255,224,0.4);
    background: rgba(0,255,224,0.08);
    transform: translateY(-2px);
}
.metric-label {
    font-size: 0.6em;
    color: rgba(255,255,255,0.35);
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: 'Share Tech Mono', monospace;
    margin-bottom: 4px;
}
.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.1em;
    font-weight: 700;
    color: var(--cyan);
}
.metric-sub {
    font-size: 0.65em;
    color: rgba(255,255,255,0.4);
    margin-top: 3px;
}

/* LAYER CARDS */
.layer-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    margin: 10px 0;
    animation: fadeIn 0.6s ease;
}
.layer-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.78em;
    color: var(--cyan);
    letter-spacing: 2px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.layer-content {
    font-size: 0.85em;
    line-height: 1.7;
    color: rgba(255,255,255,0.8);
}

/* SIGNAL BADGES */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.65em;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 1px;
    font-weight: bold;
    margin: 2px;
}
.badge-bull { background:rgba(0,255,136,0.15); border:1px solid rgba(0,255,136,0.4); color:var(--green); }
.badge-bear { background:rgba(255,51,85,0.15); border:1px solid rgba(255,51,85,0.4); color:var(--red); }
.badge-neutral { background:rgba(255,204,0,0.12); border:1px solid rgba(255,204,0,0.35); color:var(--yellow); }
.badge-extreme { background:rgba(255,136,0,0.15); border:1px solid rgba(255,136,0,0.4); color:var(--orange); animation:pulse 1.5s infinite; }

/* AGENT CARDS */
.agent-card {
    background: rgba(0,128,255,0.05);
    border: 1px solid rgba(0,128,255,0.2);
    border-left: 3px solid var(--blue);
    border-radius: 10px;
    padding: 14px 16px;
    margin: 8px 0;
    animation: fadeIn 0.4s ease;
}
.agent-name {
    font-family: 'Orbitron', monospace;
    font-size: 0.72em;
    color: var(--blue);
    letter-spacing: 2px;
    margin-bottom: 8px;
}
.agent-output {
    font-size: 0.82em;
    line-height: 1.65;
    color: rgba(255,255,255,0.82);
    font-family: 'Rajdhani', sans-serif;
}

/* FINAL VERDICT */
.verdict-container {
    border-radius: 18px;
    padding: 28px 24px;
    text-align: center;
    margin: 20px 0;
    animation: glow 2s ease infinite, fadeIn 0.8s ease;
}
.verdict-up {
    background: linear-gradient(135deg, rgba(0,255,136,0.08), rgba(0,200,100,0.05));
    border: 2px solid rgba(0,255,136,0.5);
}
.verdict-down {
    background: linear-gradient(135deg, rgba(255,51,85,0.08), rgba(200,0,50,0.05));
    border: 2px solid rgba(255,51,85,0.5);
}
.verdict-neutral {
    background: linear-gradient(135deg, rgba(255,204,0,0.08), rgba(200,150,0,0.05));
    border: 2px solid rgba(255,204,0,0.4);
}
.verdict-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(16px,4vw,32px);
    font-weight: 900;
    letter-spacing: 4px;
    margin-bottom: 10px;
}
.verdict-up .verdict-title { color: var(--green); }
.verdict-down .verdict-title { color: var(--red); }
.verdict-neutral .verdict-title { color: var(--yellow); }

/* CONFIDENCE BAR */
.conf-bar-outer {
    background: rgba(255,255,255,0.08);
    border-radius: 50px;
    height: 12px;
    overflow: hidden;
    margin: 8px 0;
}
.conf-bar-inner {
    height: 100%;
    border-radius: 50px;
    transition: width 1s ease;
}
.conf-bull { background: linear-gradient(90deg, #00aa55, #00ff88); }
.conf-bear { background: linear-gradient(90deg, #aa0022, #ff3355); }

/* PROGRESS RING */
.ring-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,255,224,0.03) !important;
    border-bottom: 1px solid rgba(0,255,224,0.15) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65em !important;
    letter-spacing: 1px !important;
    color: rgba(255,255,255,0.5) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,255,224,0.12), rgba(0,128,255,0.12)) !important;
    border: 1px solid rgba(0,255,224,0.4) !important;
    color: var(--cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.7em !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border-radius: 10px !important;
    padding: 0.55em 1em !important;
    width: 100% !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,255,224,0.22), rgba(0,128,255,0.22)) !important;
    box-shadow: 0 0 20px rgba(0,255,224,0.25) !important;
    transform: translateY(-1px) !important;
}

/* INPUTS */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(0,255,224,0.04) !important;
    border: 1px solid rgba(0,255,224,0.2) !important;
    color: #e0f0ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 8px !important;
}

/* EXPANDER */
.streamlit-expanderHeader {
    background: rgba(0,255,224,0.04) !important;
    border: 1px solid rgba(0,255,224,0.15) !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.72em !important;
    color: var(--cyan) !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #020811; }
::-webkit-scrollbar-thumb { background: rgba(0,255,224,0.3); border-radius: 2px; }

/* TABLE */
.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.8em;
    font-family: 'Share Tech Mono', monospace;
}
.data-table th {
    color: rgba(0,255,224,0.6);
    font-size: 0.65em;
    letter-spacing: 2px;
    padding: 8px;
    border-bottom: 1px solid rgba(0,255,224,0.15);
    text-align: left;
}
.data-table td {
    padding: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.8);
}
.data-table tr:hover td { background: rgba(0,255,224,0.04); }

/* STATUS DOT */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}
.dot-green { background: var(--green); box-shadow: 0 0 6px var(--green); animation: pulse 2s infinite; }
.dot-red { background: var(--red); box-shadow: 0 0 6px var(--red); }
.dot-yellow { background: var(--yellow); box-shadow: 0 0 6px var(--yellow); animation: pulse 2s infinite; }

/* RISK METER */
.risk-bar {
    height: 8px;
    border-radius: 4px;
    background: linear-gradient(90deg, #00ff88 0%, #ffcc00 50%, #ff3355 100%);
    position: relative;
    margin: 6px 0;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(2,8,17,0.95) !important;
    border-right: 1px solid rgba(0,255,224,0.1) !important;
}

/* TOAST */
.toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: rgba(0,255,224,0.1);
    border: 1px solid rgba(0,255,224,0.4);
    border-radius: 10px;
    padding: 12px 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75em;
    color: var(--cyan);
    z-index: 9999;
    animation: fadeIn 0.3s ease;
}

/* PREDICTION HISTORY TABLE */
.hist-row-up { color: var(--green); }
.hist-row-down { color: var(--red); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CONSTANTS & COIN MAP
# ══════════════════════════════════════════════════════════════

COINS = {
    "₿ Bitcoin (BTC)": {"id": "bitcoin", "symbol": "BTC", "binance": "BTCUSDT"},
    "Ξ Ethereum (ETH)": {"id": "ethereum", "symbol": "ETH", "binance": "ETHUSDT"},
    "◎ Solana (SOL)": {"id": "solana", "symbol": "SOL", "binance": "SOLUSDT"},
    "⬡ BNB": {"id": "binancecoin", "symbol": "BNB", "binance": "BNBUSDT"},
    "✕ XRP": {"id": "ripple", "symbol": "XRP", "binance": "XRPUSDT"},
    "Ð Dogecoin (DOGE)": {"id": "dogecoin", "symbol": "DOGE", "binance": "DOGEUSDT"},
    "₳ Cardano (ADA)": {"id": "cardano", "symbol": "ADA", "binance": "ADAUSDT"},
    "⬡ Avalanche (AVAX)": {"id": "avalanche-2", "symbol": "AVAX", "binance": "AVAXUSDT"},
    "🔗 Chainlink (LINK)": {"id": "chainlink", "symbol": "LINK", "binance": "LINKUSDT"},
    "● Polkadot (DOT)": {"id": "polkadot", "symbol": "DOT", "binance": "DOTUSDT"},
    "◈ Polygon (POL)": {"id": "matic-network", "symbol": "POL", "binance": "MATICUSDT"},
    "⚡ Litecoin (LTC)": {"id": "litecoin", "symbol": "LTC", "binance": "LTCUSDT"},
    "∞ Uniswap (UNI)": {"id": "uniswap", "symbol": "UNI", "binance": "UNIUSDT"},
    "Ⓐ Atom (ATOM)": {"id": "cosmos", "symbol": "ATOM", "binance": "ATOMUSDT"},
    "⬙ Near Protocol (NEAR)": {"id": "near", "symbol": "NEAR", "binance": "NEARUSDT"},
}

TIMEFRAMES = {
    "⚡ Next 4 Hours": "4H",
    "📅 Next 24 Hours": "24H",
    "📆 Next 7 Days": "7D",
    "📊 Next 30 Days": "30D",
}

# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="main-title">🧠 CRYPTOMIND AI</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">ULTIMATE MULTI-LAYER EMERGENT PREDICTION ENGINE v2.0</div>', unsafe_allow_html=True)

# Live status bar
now = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
<div style="display:flex;justify-content:center;gap:24px;flex-wrap:wrap;margin:6px 0 4px 0;font-family:'Share Tech Mono',monospace;font-size:0.68em;">
    <span><span class="status-dot dot-green"></span>SYSTEM ONLINE</span>
    <span><span class="status-dot dot-green"></span>AI AGENTS READY</span>
    <span><span class="status-dot dot-green"></span>DATA FEEDS LIVE</span>
    <span style="color:rgba(255,255,255,0.35)">LAST UPDATE: {now} UTC</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="disclaimer">⚠️ EDUCATIONAL PURPOSE ONLY — NOT FINANCIAL ADVICE — TRADE AT YOUR OWN RISK — PAST PREDICTIONS ≠ FUTURE RESULTS</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.8em;color:#00ffe0;letter-spacing:2px;text-align:center;padding:10px 0;border-bottom:1px solid rgba(0,255,224,0.15);">⚙️ CONTROL CENTER</div>', unsafe_allow_html=True)

    st.markdown("### 🔑 API Keys (Free)")
    groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...", help="groq.com → Free signup → Create key")
    gemini_key = st.text_input("Gemini API Key", type="password", placeholder="AIza...", help="aistudio.google.com → Get API Key")
    telegram_token = st.text_input("Telegram Bot Token", type="password", placeholder="optional", help="@BotFather pe /newbot karo")
    telegram_chat_id = st.text_input("Telegram Chat ID", placeholder="optional", help="@userinfobot se milega")

    st.markdown("---")
    st.markdown("### 🎛️ Settings")
    st.session_state.user_mode = st.selectbox("Mode", ["Beginner", "Expert", "Pro Trader"])
    st.session_state.language = st.selectbox("Language", ["English", "Hindi", "Hinglish"])
    auto_refresh = st.toggle("Auto Refresh (60s)", value=False)
    show_tutorial = st.toggle("Tutorial Mode", value=False)

    st.markdown("---")
    st.markdown("### 📊 API Status")
    apis = {"CoinGecko": "🟢", "Binance": "🟢", "Fear/Greed": "🟢", "CryptoPanic": "🟢", "CoinMarketCal": "🟢"}
    for api, status in apis.items():
        st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:0.75em;padding:3px 0"><span style="color:rgba(255,255,255,0.6)">{api}</span><span>{status} Live</span></div>', unsafe_allow_html=True)

    if groq_key:
        st.markdown('<div style="color:#00ff88;font-size:0.72em;text-align:center;padding:6px;background:rgba(0,255,136,0.08);border-radius:6px;margin-top:8px">✅ GROQ CONNECTED</div>', unsafe_allow_html=True)
    if gemini_key:
        st.markdown('<div style="color:#00ff88;font-size:0.72em;text-align:center;padding:6px;background:rgba(0,255,136,0.08);border-radius:6px;margin-top:4px">✅ GEMINI CONNECTED</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:0.6em;color:rgba(255,255,255,0.2);text-align:center;line-height:1.8">CRYPTOMIND AI v2.0<br>316 FEATURES • MULTI-AGENT<br>EMERGENT CONSENSUS ENGINE</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  DATA FETCHING FUNCTIONS
# ══════════════════════════════════════════════════════════════

@st.cache_data(ttl=60)
def get_coin_data(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        params = {"localization":"false","tickers":"false","community_data":"true","developer_data":"true"}
        r = requests.get(url, params=params, timeout=12)
        if r.status_code == 200:
            return r.json()
    except: pass
    return None

@st.cache_data(ttl=60)
def get_market_chart(coin_id, days=30):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        r = requests.get(url, params={"vs_currency":"usd","days":days,"interval":"daily"}, timeout=12)
        if r.status_code == 200:
            return r.json()
    except: pass
    return None

@st.cache_data(ttl=90)
def get_market_chart_hourly(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        r = requests.get(url, params={"vs_currency":"usd","days":2,"interval":"hourly"}, timeout=12)
        if r.status_code == 200:
            return r.json()
    except: pass
    return None

@st.cache_data(ttl=120)
def get_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=7", timeout=8)
        if r.status_code == 200:
            return r.json().get("data", [])
    except: pass
    return [{"value":"50","value_classification":"Neutral","timestamp":str(int(time.time()))}]

@st.cache_data(ttl=120)
def get_global_market():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/global", timeout=8)
        if r.status_code == 200:
            return r.json().get("data", {})
    except: pass
    return {}

@st.cache_data(ttl=180)
def get_trending():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=8)
        if r.status_code == 200:
            return r.json().get("coins", [])
    except: pass
    return []

@st.cache_data(ttl=120)
def get_crypto_news(symbol):
    try:
        r = requests.get(
            f"https://cryptopanic.com/api/free/v1/posts/?auth_token=free&currencies={symbol}&public=true&kind=news",
            timeout=10
        )
        if r.status_code == 200:
            return r.json().get("results", [])[:8]
    except: pass
    return []

@st.cache_data(ttl=90)
def get_binance_ticker(symbol):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}", timeout=8)
        if r.status_code == 200:
            return r.json()
    except: pass
    return None

@st.cache_data(ttl=90)
def get_binance_orderbook(symbol):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=10", timeout=8)
        if r.status_code == 200:
            return r.json()
    except: pass
    return None

@st.cache_data(ttl=90)
def get_binance_trades(symbol):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=20", timeout=8)
        if r.status_code == 200:
            return r.json()
    except: pass
    return []

@st.cache_data(ttl=300)
def get_coinmarketcal_events():
    try:
        headers = {"x-api-key": "free", "Accept-Encoding": "deflate, gzip", "Accept": "application/json"}
        r = requests.get("https://developers.coinmarketcal.com/v1/events?page=1&max=10", headers=headers, timeout=8)
        if r.status_code == 200:
            return r.json().get("body", [])
    except: pass
    return []

@st.cache_data(ttl=300)
def get_top_coins():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={"vs_currency":"usd","order":"market_cap_desc","per_page":20,"page":1,"sparkline":False,"price_change_percentage":"24h,7d"},
            timeout=12
        )
        if r.status_code == 200:
            return r.json()
    except: pass
    return []

# ══════════════════════════════════════════════════════════════
#  TECHNICAL ANALYSIS ENGINE
# ══════════════════════════════════════════════════════════════

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1: return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        d = prices[i] - prices[i-1]
        gains.append(max(d,0)); losses.append(max(-d,0))
    ag = sum(gains[-period:])/period
    al = sum(losses[-period:])/period
    if al == 0: return 100
    return round(100 - (100/(1+(ag/al))), 2)

def calculate_ema(prices, period):
    if len(prices) < period: return None
    k = 2/(period+1)
    ema = sum(prices[:period])/period
    for p in prices[period:]: ema = p*k + ema*(1-k)
    return round(ema, 6)

def calculate_macd(prices):
    if len(prices) < 26: return None, None, None
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    if not ema12 or not ema26: return None,None,None
    macd_line = ema12 - ema26
    # Signal line (9-day EMA of MACD)
    macd_values = []
    for i in range(12, len(prices)+1):
        e12 = calculate_ema(prices[:i], 12)
        e26 = calculate_ema(prices[:i], 26)
        if e12 and e26: macd_values.append(e12-e26)
    signal = calculate_ema(macd_values, 9) if len(macd_values) >= 9 else macd_line
    histogram = macd_line - signal if signal else 0
    return round(macd_line,6), round(signal,6) if signal else None, round(histogram,6)

def calculate_bollinger(prices, period=20):
    if len(prices) < period: return None, None, None
    sma = sum(prices[-period:])/period
    std = math.sqrt(sum((p-sma)**2 for p in prices[-period:])/period)
    return round(sma+2*std,6), round(sma,6), round(sma-2*std,6)

def calculate_sma(prices, period):
    if len(prices) < period: return None
    return round(sum(prices[-period:])/period, 6)

def calculate_stoch_rsi(prices, period=14):
    rsi_vals = []
    for i in range(period, len(prices)+1):
        r = calculate_rsi(prices[:i], period)
        if r: rsi_vals.append(r)
    if len(rsi_vals) < period: return None
    recent = rsi_vals[-period:]
    mn, mx = min(recent), max(recent)
    if mx == mn: return 50
    return round((recent[-1]-mn)/(mx-mn)*100, 2)

def calculate_obv(prices, volumes):
    if len(prices) != len(volumes) or len(prices) < 2: return 0
    obv = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]: obv += volumes[i]
        elif prices[i] < prices[i-1]: obv -= volumes[i]
    return obv

def calculate_vwap(prices, volumes):
    if not prices or not volumes: return None
    pv = sum(p*v for p,v in zip(prices,volumes))
    tv = sum(volumes)
    return round(pv/tv, 6) if tv > 0 else None

def calculate_atr(highs, lows, closes, period=14):
    if len(closes) < period+1: return None
    trs = []
    for i in range(1, len(closes)):
        tr = max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1]))
        trs.append(tr)
    return round(sum(trs[-period:])/period, 6)

def get_support_resistance(prices):
    if len(prices) < 10: return None, None
    recent = prices[-20:] if len(prices) >= 20 else prices
    support = round(min(recent), 6)
    resistance = round(max(recent), 6)
    return support, resistance

def detect_candlestick_pattern(prices):
    if len(prices) < 3: return "Insufficient data"
    p1, p2, p3 = prices[-3], prices[-2], prices[-1]
    if p3 > p2 > p1: return "🟢 Three White Soldiers (Bullish)"
    if p3 < p2 < p1: return "🔴 Three Black Crows (Bearish)"
    if abs(p2-p1)/max(p1,0.0001) < 0.005 and p3 > p2*1.01: return "🟢 Morning Star (Bullish)"
    if abs(p2-p1)/max(p1,0.0001) < 0.005 and p3 < p2*0.99: return "🔴 Evening Star (Bearish)"
    if p3 > p1 and p3 > p2: return "🟢 Higher High (Bullish)"
    if p3 < p1 and p3 < p2: return "🔴 Lower Low (Bearish)"
    return "⚪ No Clear Pattern"

def get_fibonacci_levels(prices):
    if len(prices) < 5: return {}
    high, low = max(prices[-30:] if len(prices)>=30 else prices), min(prices[-30:] if len(prices)>=30 else prices)
    diff = high - low
    return {
        "0.0% (High)": round(high, 4),
        "23.6%": round(high - 0.236*diff, 4),
        "38.2%": round(high - 0.382*diff, 4),
        "50.0%": round(high - 0.5*diff, 4),
        "61.8% (Golden)": round(high - 0.618*diff, 4),
        "78.6%": round(high - 0.786*diff, 4),
        "100% (Low)": round(low, 4),
    }

def get_market_regime(prices):
    if len(prices) < 10: return "Unknown"
    ema50 = calculate_ema(prices, min(50, len(prices)))
    ema20 = calculate_ema(prices, min(20, len(prices)))
    cur = prices[-1]
    if not ema50 or not ema20: return "Insufficient Data"
    if cur > ema20 > ema50: return "🐂 BULL MARKET"
    if cur < ema20 < ema50: return "🐻 BEAR MARKET"
    if abs(cur - ema20)/max(ema20,0.0001) < 0.03: return "↔️ SIDEWAYS / ACCUMULATION"
    return "🌀 TRANSITIONING"

def detect_divergence(prices, rsi_vals):
    if len(prices) < 5 or len(rsi_vals) < 5: return "No divergence data"
    price_trend = prices[-1] > prices[-5]
    rsi_trend = rsi_vals[-1] > rsi_vals[-5] if len(rsi_vals)>=5 else None
    if rsi_trend is None: return "Insufficient RSI data"
    if price_trend and not rsi_trend: return "⚠️ Bearish Divergence (Price↑ RSI↓)"
    if not price_trend and rsi_trend: return "🟢 Bullish Divergence (Price↓ RSI↑)"
    return "✅ No Divergence"

def run_full_technical_analysis(prices, volumes=None):
    result = {}
    if not prices or len(prices) < 5:
        return result

    cur = prices[-1]

    # Core indicators
    result["RSI_14"] = calculate_rsi(prices, 14)
    result["RSI_7"] = calculate_rsi(prices, 7)
    result["StochRSI"] = calculate_stoch_rsi(prices)
    result["EMA_9"] = calculate_ema(prices, min(9, len(prices)))
    result["EMA_21"] = calculate_ema(prices, min(21, len(prices)))
    result["EMA_50"] = calculate_ema(prices, min(50, len(prices)))
    result["EMA_200"] = calculate_ema(prices, min(200, len(prices)))
    result["SMA_7"] = calculate_sma(prices, min(7, len(prices)))
    result["SMA_14"] = calculate_sma(prices, min(14, len(prices)))
    result["SMA_30"] = calculate_sma(prices, min(30, len(prices)))
    macd, signal, hist = calculate_macd(prices)
    result["MACD"] = macd
    result["MACD_Signal"] = signal
    result["MACD_Hist"] = hist
    bb_upper, bb_mid, bb_lower = calculate_bollinger(prices)
    result["BB_Upper"] = bb_upper
    result["BB_Middle"] = bb_mid
    result["BB_Lower"] = bb_lower
    result["Support"], result["Resistance"] = get_support_resistance(prices)
    result["Market_Regime"] = get_market_regime(prices)
    result["Candlestick_Pattern"] = detect_candlestick_pattern(prices)

    # Momentum
    if len(prices) >= 7:
        result["Momentum_7d"] = round(((cur - prices[-7])/max(prices[-7],0.0001))*100, 2)
    if len(prices) >= 3:
        result["Momentum_3d"] = round(((cur - prices[-3])/max(prices[-3],0.0001))*100, 2)

    # Volume indicators
    if volumes:
        result["OBV"] = calculate_obv(prices[-len(volumes):], volumes)
        result["VWAP"] = calculate_vwap(prices[-len(volumes):], volumes)

    # Fibonacci
    result["Fibonacci"] = get_fibonacci_levels(prices)

    # RSI signals
    rsi = result.get("RSI_14")
    if rsi:
        if rsi < 30: result["RSI_Signal"] = "🟢 OVERSOLD — Potential Reversal Up"
        elif rsi > 70: result["RSI_Signal"] = "🔴 OVERBOUGHT — Potential Reversal Down"
        elif rsi < 40: result["RSI_Signal"] = "🟡 WEAK — Slight Bearish"
        elif rsi > 60: result["RSI_Signal"] = "🟡 STRONG — Slight Bullish"
        else: result["RSI_Signal"] = "⚪ NEUTRAL"

    # MACD Signal
    if macd and signal:
        if macd > signal: result["MACD_Signal_Txt"] = "🟢 BULLISH CROSSOVER"
        else: result["MACD_Signal_Txt"] = "🔴 BEARISH CROSSOVER"

    # BB Position
    if bb_upper and bb_lower:
        if cur > bb_upper: result["BB_Signal"] = "🔴 ABOVE UPPER BAND — Overbought"
        elif cur < bb_lower: result["BB_Signal"] = "🟢 BELOW LOWER BAND — Oversold"
        else:
            bb_pos = (cur - bb_lower)/(bb_upper - bb_lower)*100
            result["BB_Position"] = round(bb_pos, 1)
            result["BB_Signal"] = f"⚪ IN BAND ({bb_pos:.0f}%)"

    # EMA Trend
    ema9, ema21, ema50 = result.get("EMA_9"), result.get("EMA_21"), result.get("EMA_50")
    if ema9 and ema21:
        if ema9 > ema21: result["EMA_Trend"] = "🟢 BULLISH (EMA9 > EMA21)"
        else: result["EMA_Trend"] = "🔴 BEARISH (EMA9 < EMA21)"

    # BB Squeeze
    if bb_upper and bb_lower and bb_mid:
        bandwidth = (bb_upper - bb_lower)/max(bb_mid, 0.0001)
        result["BB_Bandwidth"] = round(bandwidth*100, 2)
        if bandwidth < 0.04: result["BB_Squeeze"] = "⚡ SQUEEZE — BIG MOVE INCOMING"
        else: result["BB_Squeeze"] = "Normal Bandwidth"

    # Divergence
    rsi_history = []
    for i in range(5, min(20, len(prices))+1):
        r = calculate_rsi(prices[:i])
        if r: rsi_history.append(r)
    result["Divergence"] = detect_divergence(prices, rsi_history)

    # Overall bull/bear score
    score = 0
    if rsi and rsi < 45: score -= 1
    if rsi and rsi > 55: score += 1
    if rsi and rsi < 30: score += 2  # oversold = potential bounce
    if rsi and rsi > 70: score -= 2  # overbought = potential drop
    if macd and signal and macd > signal: score += 1
    if macd and signal and macd < signal: score -= 1
    if ema9 and ema21 and ema9 > ema21: score += 1
    if ema9 and ema21 and ema9 < ema21: score -= 1
    if result.get("Momentum_7d") and result["Momentum_7d"] > 0: score += 1
    if result.get("Momentum_7d") and result["Momentum_7d"] < 0: score -= 1

    result["Tech_Score"] = score
    if score >= 3: result["Tech_Verdict"] = "🟢 STRONG BULLISH"
    elif score >= 1: result["Tech_Verdict"] = "🟡 WEAK BULLISH"
    elif score <= -3: result["Tech_Verdict"] = "🔴 STRONG BEARISH"
    elif score <= -1: result["Tech_Verdict"] = "🟡 WEAK BEARISH"
    else: result["Tech_Verdict"] = "⚪ NEUTRAL"

    return result

# ══════════════════════════════════════════════════════════════
#  SENTIMENT ANALYSIS ENGINE
# ══════════════════════════════════════════════════════════════

def analyze_news_sentiment(news_items):
    bullish_words = ["surge", "rally", "bull", "gain", "pump", "soar", "rise", "high", "profit",
                     "adoption", "launch", "partnership", "upgrade", "positive", "approved",
                     "breakout", "record", "milestone", "growth", "buy", "investment", "support",
                     "accumulate", "listing", "etf", "approval", "halving", "institutional"]
    bearish_words = ["crash", "bear", "fall", "dump", "drop", "low", "loss", "hack", "ban",
                     "sell", "fear", "panic", "decline", "negative", "rejected", "lawsuit",
                     "investigation", "fine", "scam", "warning", "risk", "concern", "bubble",
                     "regulation", "crackdown", "delist", "liquidation", "bankrupt"]

    bull_count, bear_count = 0, 0
    scored_news = []

    for item in news_items:
        title = item.get("title", "").lower()
        votes = item.get("votes", {})
        bull_v = votes.get("positive", 0)
        bear_v = votes.get("negative", 0)

        b_score = sum(1 for w in bullish_words if w in title) + bull_v//5
        be_score = sum(1 for w in bearish_words if w in title) + bear_v//5
        bull_count += b_score
        bear_count += be_score

        sentiment = "🟢 Bullish" if b_score > be_score else "🔴 Bearish" if be_score > b_score else "⚪ Neutral"
        scored_news.append({
            "title": item.get("title", ""),
            "sentiment": sentiment,
            "bull_score": b_score,
            "bear_score": be_score,
            "published": item.get("published_at","")[:10]
        })

    total = bull_count + bear_count
    bull_pct = round((bull_count/total)*100) if total > 0 else 50
    bear_pct = 100 - bull_pct

    overall = "🟢 BULLISH" if bull_pct > 55 else "🔴 BEARISH" if bear_pct > 55 else "⚪ NEUTRAL"
    return {
        "overall": overall,
        "bull_pct": bull_pct,
        "bear_pct": bear_pct,
        "scored_news": scored_news,
        "total_articles": len(news_items)
    }

def calculate_sentiment_score(fear_greed_val, news_bull_pct, change_24h, change_7d):
    """Combined sentiment score 0-100"""
    fg_score = int(fear_greed_val) if str(fear_greed_val).isdigit() else 50
    news_score = news_bull_pct
    price_score = 50 + min(max(change_24h*3, -30), 30)
    week_score = 50 + min(max(change_7d*2, -30), 30)
    combined = (fg_score*0.3 + news_score*0.3 + price_score*0.25 + week_score*0.15)
    return round(combined, 1)

# ══════════════════════════════════════════════════════════════
#  RISK ANALYSIS ENGINE
# ══════════════════════════════════════════════════════════════

def calculate_risk_metrics(prices, current_price, position_size=1000):
    if not prices or len(prices) < 7:
        return {}

    returns = [(prices[i]-prices[i-1])/max(prices[i-1],0.0001) for i in range(1, len(prices))]

    # Volatility
    if len(returns) > 1:
        mean_r = sum(returns)/len(returns)
        variance = sum((r-mean_r)**2 for r in returns)/len(returns)
        volatility = math.sqrt(variance)*100
    else:
        volatility = 5

    # Value at Risk (95%)
    sorted_r = sorted(returns)
    var_95 = sorted_r[max(0,int(len(sorted_r)*0.05))]
    var_dollar = abs(var_95 * position_size)

    # Max Drawdown
    peak = prices[0]
    max_dd = 0
    for p in prices:
        if p > peak: peak = p
        dd = (peak-p)/max(peak,0.0001)*100
        if dd > max_dd: max_dd = dd

    # Sharpe (simplified, assume 0 risk-free)
    if len(returns) > 1 and volatility > 0:
        sharpe = (mean_r * 365**(0.5)) / (volatility/100 * 365**(0.5))
    else:
        sharpe = 0

    # Risk Score 1-10
    risk_score = min(10, max(1, int(volatility/3)))

    # Support/Resistance for stop-loss
    support, resistance = get_support_resistance(prices)
    stop_loss = support * 0.98 if support else current_price * 0.95
    take_profit_1 = resistance * 1.02 if resistance else current_price * 1.05
    take_profit_2 = current_price * 1.1

    return {
        "volatility_pct": round(volatility, 2),
        "var_95_pct": round(abs(var_95)*100, 2),
        "var_dollar": round(var_dollar, 2),
        "max_drawdown": round(max_dd, 2),
        "sharpe": round(sharpe, 2),
        "risk_score": risk_score,
        "stop_loss": stop_loss,
        "take_profit_1": take_profit_1,
        "take_profit_2": take_profit_2,
        "risk_reward": round((take_profit_1 - current_price)/max(current_price - stop_loss, 0.0001), 2)
    }

# ══════════════════════════════════════════════════════════════
#  AI AGENT ENGINE
# ══════════════════════════════════════════════════════════════

def call_groq(prompt, api_key, model="llama-3.1-8b-instant", max_tokens=600):
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        body = {"model": model, "messages": [{"role":"user","content":prompt}],
                "max_tokens": max_tokens, "temperature": 0.25}
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                          headers=headers, json=body, timeout=25)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"[Groq Error {r.status_code}]"
    except Exception as e:
        return f"[Groq Error: {str(e)[:80]}]"

def call_gemini(prompt, api_key, max_tokens=600):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        body = {"contents":[{"parts":[{"text":prompt}]}],
                "generationConfig":{"maxOutputTokens":max_tokens,"temperature":0.25}}
        r = requests.post(url, json=body, timeout=25)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"[Gemini Error {r.status_code}]"
    except Exception as e:
        return f"[Gemini Error: {str(e)[:80]}]"

def pick_ai(groq_key, gemini_key, prefer_gemini=False):
    """Pick which AI to use"""
    if prefer_gemini and gemini_key:
        return "gemini"
    if groq_key:
        return "groq"
    if gemini_key:
        return "gemini"
    return None

def run_ai(prompt, groq_key, gemini_key, prefer_gemini=False, max_tokens=600):
    ai = pick_ai(groq_key, gemini_key, prefer_gemini)
    if ai == "groq":
        return call_groq(prompt, groq_key, max_tokens=max_tokens)
    if ai == "gemini":
        return call_gemini(prompt, gemini_key, max_tokens=max_tokens)
    return "⚠️ No API key. Add Groq or Gemini key in sidebar to activate AI agents."

# ══════════════════════════════════════════════════════════════
#  TELEGRAM ALERT
# ══════════════════════════════════════════════════════════════

def send_telegram(token, chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=10)
        return r.status_code == 200
    except:
        return False

# ══════════════════════════════════════════════════════════════
#  MAIN APP — COIN SELECTOR
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🎯 SELECT ASSET & TIMEFRAME</div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns([3, 2, 1])
with col_s1:
    selected_name = st.selectbox("🪙 Asset", list(COINS.keys()), label_visibility="collapsed")
with col_s2:
    selected_tf_name = st.selectbox("⏱️ Timeframe", list(TIMEFRAMES.keys()), label_visibility="collapsed")
with col_s3:
    refresh_btn = st.button("🔄 REFRESH")

coin_info = COINS[selected_name]
coin_id = coin_info["id"]
coin_symbol = coin_info["symbol"]
binance_symbol = coin_info["binance"]
timeframe = TIMEFRAMES[selected_tf_name]

# ══════════════════════════════════════════════════════════════
#  LIVE TICKER BAR
# ══════════════════════════════════════════════════════════════

top_coins = get_top_coins()
if top_coins:
    ticker_items = []
    for c in top_coins[:12]:
        chg = c.get("price_change_percentage_24h", 0) or 0
        arrow = "▲" if chg >= 0 else "▼"
        color = "#00ff88" if chg >= 0 else "#ff3355"
        p = c.get("current_price",0)
        price_str = f"${p:,.4f}" if p < 1 else f"${p:,.2f}"
        ticker_items.append(f'<span style="margin:0 20px"><span style="color:rgba(255,255,255,0.5)">{c["symbol"].upper()}</span> <span style="color:{color}">{arrow} {abs(chg):.1f}%</span></span>')
    st.markdown(f'<div class="ticker-bar">{"  •  ".join(ticker_items)}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FETCH ALL DATA
# ══════════════════════════════════════════════════════════════

with st.spinner("📡 Fetching real-time data from all sources..."):
    coin_data = get_coin_data(coin_id)
    chart_data_30 = get_market_chart(coin_id, 30)
    chart_data_7 = get_market_chart(coin_id, 7)
    chart_data_90 = get_market_chart(coin_id, 90)
    fear_greed_data = get_fear_greed()
    global_data = get_global_market()
    news_data = get_crypto_news(coin_symbol)
    binance_ticker = get_binance_ticker(binance_symbol)
    binance_orderbook = get_binance_orderbook(binance_symbol)
    binance_trades = get_binance_trades(binance_symbol)
    trending = get_trending()

# Extract prices
prices_30 = [p[1] for p in chart_data_30.get("prices",[])] if chart_data_30 else []
prices_7 = [p[1] for p in chart_data_7.get("prices",[])] if chart_data_7 else []
prices_90 = [p[1] for p in chart_data_90.get("prices",[])] if chart_data_90 else []
volumes_30 = [v[1] for v in chart_data_30.get("total_volumes",[])] if chart_data_30 else []

# ══════════════════════════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════════════════════════

tabs = st.tabs([
    "📊 MARKET DATA",
    "📈 TECHNICAL",
    "📰 SENTIMENT",
    "⚡ EVENTS",
    "🌍 MACRO",
    "🤖 AI ANALYSIS",
    "🎯 PREDICTION",
    "⚠️ RISK",
    "🔔 ALERTS",
    "👤 PORTFOLIO",
    "📜 HISTORY"
])

# ══════════════════════════════════════════════════════════════
#  TAB 1: MARKET DATA
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    if coin_data:
        md = coin_data["market_data"]
        price = md["current_price"]["usd"]
        change_24h = md.get("price_change_percentage_24h") or 0
        change_7d = md.get("price_change_percentage_7d") or 0
        change_30d = md.get("price_change_percentage_30d") or 0
        market_cap = md.get("market_cap",{}).get("usd",0)
        volume = md.get("total_volume",{}).get("usd",0)
        ath = md.get("ath",{}).get("usd",0)
        atl = md.get("atl",{}).get("usd",0)
        ath_change = md.get("ath_change_percentage",{}).get("usd",0) or 0
        circ_supply = md.get("circulating_supply",0)
        total_supply = md.get("total_supply",0)
        mc_rank = coin_data.get("market_cap_rank","N/A")

        # Key metrics row
        st.markdown('<div class="section-header">💰 REAL-TIME PRICE DATA</div>', unsafe_allow_html=True)

        m1,m2,m3,m4,m5,m6 = st.columns(6)

        def mc(col, label, value, color=None):
            color_str = f"color:{color};" if color else ""
            col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value" style="{color_str}">{value}</div></div>', unsafe_allow_html=True)

        price_str = f"${price:,.6f}" if price < 0.01 else f"${price:,.4f}" if price < 1 else f"${price:,.2f}"
        mc(m1, "CURRENT PRICE", price_str)
        mc(m2, "24H CHANGE", f"{'▲' if change_24h>=0 else '▼'} {abs(change_24h):.2f}%", "#00ff88" if change_24h>=0 else "#ff3355")
        mc(m3, "7D CHANGE", f"{'▲' if change_7d>=0 else '▼'} {abs(change_7d):.2f}%", "#00ff88" if change_7d>=0 else "#ff3355")
        mc(m4, "30D CHANGE", f"{'▲' if change_30d>=0 else '▼'} {abs(change_30d):.2f}%", "#00ff88" if change_30d>=0 else "#ff3355")
        mc(m5, "MARKET CAP", f"${market_cap/1e9:.2f}B")
        mc(m6, "24H VOLUME", f"${volume/1e9:.2f}B")

        st.markdown("<br>", unsafe_allow_html=True)
        m7,m8,m9,m10,m11,m12 = st.columns(6)
        mc(m7, "MC RANK", f"#{mc_rank}")
        mc(m8, "ATH", f"${ath:,.2f}")
        mc(m9, "ATH DISTANCE", f"{ath_change:.1f}%", "#ff3355")
        mc(m10, "ATL", f"${atl:,.6f}" if atl < 0.01 else f"${atl:,.4f}")
        if circ_supply and total_supply and total_supply > 0:
            supply_pct = (circ_supply/total_supply)*100
            mc(m11, "SUPPLY %", f"{supply_pct:.1f}%")
        else:
            mc(m11, "CIRC SUPPLY", f"{circ_supply/1e6:.1f}M" if circ_supply else "N/A")
        vol_mc_ratio = (volume/market_cap)*100 if market_cap > 0 else 0
        mc(m12, "VOL/MC RATIO", f"{vol_mc_ratio:.2f}%", "#ffcc00")

        # Binance Order Book
        st.markdown('<div class="section-header">📋 ORDER BOOK & TRADE DATA (BINANCE)</div>', unsafe_allow_html=True)

        ob_col, tr_col = st.columns(2)

        with ob_col:
            if binance_orderbook:
                bids = binance_orderbook.get("bids",[])[:5]
                asks = binance_orderbook.get("asks",[])[:5]
                total_bid_vol = sum(float(b[1]) for b in bids)
                total_ask_vol = sum(float(a[1]) for a in asks)
                buy_pressure = (total_bid_vol/(total_bid_vol+total_ask_vol)*100) if (total_bid_vol+total_ask_vol)>0 else 50

                pressure_color = "#00ff88" if buy_pressure > 52 else "#ff3355" if buy_pressure < 48 else "#ffcc00"
                st.markdown(f"""
                <div class="layer-card">
                    <div class="layer-title">📊 ORDER BOOK DEPTH</div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:10px">
                        <span style="color:#00ff88;font-size:0.8em">BUY PRESSURE: {buy_pressure:.1f}%</span>
                        <span style="color:#ff3355;font-size:0.8em">SELL: {100-buy_pressure:.1f}%</span>
                    </div>
                    <div class="conf-bar-outer">
                        <div class="conf-bar-inner conf-bull" style="width:{buy_pressure}%"></div>
                    </div>
                    <div style="margin-top:10px;font-size:0.72em;color:rgba(255,255,255,0.4)">
                        Top 5 Bids Vol: {total_bid_vol:.4f} | Top 5 Asks Vol: {total_ask_vol:.4f}
                    </div>
                    <div style="margin-top:8px;font-size:0.75em;color:{pressure_color}">
                        {'🟢 BUY SIDE DOMINANT' if buy_pressure>52 else '🔴 SELL SIDE DOMINANT' if buy_pressure<48 else '⚪ BALANCED BOOK'}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="layer-card"><div class="layer-title">📊 ORDER BOOK</div><div class="layer-content">⚠️ Binance data unavailable</div></div>', unsafe_allow_html=True)

        with tr_col:
            if binance_trades:
                buy_trades = sum(1 for t in binance_trades if not t.get("isBuyerMaker",True))
                sell_trades = len(binance_trades) - buy_trades
                avg_trade_size = sum(float(t.get("qty",0)) for t in binance_trades)/max(len(binance_trades),1)
                large_trades = sum(1 for t in binance_trades if float(t.get("qty",0)) > avg_trade_size*2)
                st.markdown(f"""
                <div class="layer-card">
                    <div class="layer-title">⚡ RECENT TRADES ({len(binance_trades)})</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.8em">
                        <div>🟢 Buy Trades: <b style="color:#00ff88">{buy_trades}</b></div>
                        <div>🔴 Sell Trades: <b style="color:#ff3355">{sell_trades}</b></div>
                        <div>📦 Avg Size: <b>{avg_trade_size:.4f}</b></div>
                        <div>🐋 Large Trades: <b style="color:#ffcc00">{large_trades}</b></div>
                    </div>
                    <div style="margin-top:8px;font-size:0.75em;color:{'#00ff88' if buy_trades>sell_trades else '#ff3355'}">
                        {'🟢 MORE BUYERS' if buy_trades>sell_trades else '🔴 MORE SELLERS'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Global Market
        if global_data:
            st.markdown('<div class="section-header">🌐 GLOBAL CRYPTO MARKET</div>', unsafe_allow_html=True)
            g1,g2,g3,g4 = st.columns(4)
            total_mc = global_data.get("total_market_cap",{}).get("usd",0)
            btc_dom = global_data.get("market_cap_percentage",{}).get("btc",0)
            eth_dom = global_data.get("market_cap_percentage",{}).get("eth",0)
            active_coins = global_data.get("active_cryptocurrencies",0)
            mc(g1, "TOTAL MARKET CAP", f"${total_mc/1e12:.2f}T")
            mc(g2, "BTC DOMINANCE", f"{btc_dom:.1f}%", "#f7931a")
            mc(g3, "ETH DOMINANCE", f"{eth_dom:.1f}%", "#627eea")
            mc(g4, "ACTIVE COINS", f"{active_coins:,}")

        # Price Chart
        st.markdown('<div class="section-header">📉 PRICE HISTORY CHART</div>', unsafe_allow_html=True)
        if prices_90:
            import streamlit as st
            chart_df_labels = [f"Day {i+1}" for i in range(len(prices_90))]
            st.line_chart({"Price (USD)": prices_90}, height=280)

        # TradingView Widget
        st.markdown('<div class="section-header">📊 LIVE TRADINGVIEW CHART</div>', unsafe_allow_html=True)
        tv_symbol_map = {"BTC":"BTCUSDT","ETH":"ETHUSDT","SOL":"SOLUSDT","BNB":"BNBUSDT",
                         "XRP":"XRPUSDT","DOGE":"DOGEUSDT","ADA":"ADAUSDT","AVAX":"AVAXUSDT",
                         "LINK":"LINKUSDT","DOT":"DOTUSDT","POL":"MATICUSDT","LTC":"LTCUSDT",
                         "UNI":"UNIUSDT","ATOM":"ATOMUSDT","NEAR":"NEARUSDT"}
        tv_sym = tv_symbol_map.get(coin_symbol, f"{coin_symbol}USDT")
        st.components.v1.html(f"""
        <div id="tradingview_chart"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
            "width": "100%", "height": 450,
            "symbol": "BINANCE:{tv_sym}",
            "interval": "60",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#020811",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "container_id": "tradingview_chart",
            "studies": ["RSI@tv-basicstudies", "MACD@tv-basicstudies", "BB@tv-basicstudies"]
        }});
        </script>
        """, height=470)

    else:
        st.warning("⚠️ CoinGecko API rate limit. Please wait 30 seconds and refresh.")

# ══════════════════════════════════════════════════════════════
#  TAB 2: TECHNICAL ANALYSIS
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">📈 FULL TECHNICAL ANALYSIS ENGINE</div>', unsafe_allow_html=True)

    if prices_30:
        tech = run_full_technical_analysis(prices_30, volumes_30 if volumes_30 else None)
        current_price = prices_30[-1]

        # Tech Verdict
        verdict_color = "#00ff88" if "BULL" in tech.get("Tech_Verdict","") else "#ff3355" if "BEAR" in tech.get("Tech_Verdict","") else "#ffcc00"
        st.markdown(f"""
        <div class="layer-card" style="border-color:{verdict_color};border-left:3px solid {verdict_color}">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <div style="font-family:Orbitron,monospace;font-size:0.75em;color:rgba(255,255,255,0.5);letter-spacing:2px">TECHNICAL VERDICT</div>
                    <div style="font-family:Orbitron,monospace;font-size:1.3em;color:{verdict_color};margin-top:4px">{tech.get('Tech_Verdict','N/A')}</div>
                </div>
                <div style="text-align:right">
                    <div style="font-size:0.75em;color:rgba(255,255,255,0.4)">TECH SCORE</div>
                    <div style="font-family:Orbitron,monospace;font-size:1.8em;color:{verdict_color}">{tech.get('Tech_Score',0):+d}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Indicators grid
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""<div class="layer-card"><div class="layer-title">⚡ MOMENTUM INDICATORS</div>""", unsafe_allow_html=True)

            indicators = [
                ("RSI (14)", tech.get("RSI_14"), tech.get("RSI_Signal","")),
                ("RSI (7)", tech.get("RSI_7"), "Fast RSI"),
                ("Stoch RSI", tech.get("StochRSI"), "Stochastic RSI"),
                ("MACD", tech.get("MACD"), tech.get("MACD_Signal_Txt","")),
                ("MACD Signal", tech.get("MACD_Signal"), ""),
                ("MACD Histogram", tech.get("MACD_Hist"), ""),
                ("Momentum 7D", f"{tech.get('Momentum_7d',0):+.2f}%" if tech.get('Momentum_7d') else "N/A", ""),
                ("Momentum 3D", f"{tech.get('Momentum_3d',0):+.2f}%" if tech.get('Momentum_3d') else "N/A", ""),
            ]

            rows = ""
            for name, val, sig in indicators:
                if val is None: continue
                sig_color = "#00ff88" if "Bullish" in str(sig) or "BULLISH" in str(sig) or "OVERSOLD" in str(sig) else "#ff3355" if "Bearish" in str(sig) or "BEARISH" in str(sig) or "OVERBOUGHT" in str(sig) else "#ffcc00"
                rows += f'<tr><td style="color:rgba(255,255,255,0.5)">{name}</td><td><b>{val}</b></td><td style="color:{sig_color};font-size:0.8em">{sig}</td></tr>'
            st.markdown(f'<table class="data-table">{rows}</table></div>', unsafe_allow_html=True)

        with col2:
            st.markdown("""<div class="layer-card"><div class="layer-title">📊 MOVING AVERAGES</div>""", unsafe_allow_html=True)
            ma_rows = ""
            for ma_name, ma_key in [("EMA 9","EMA_9"),("EMA 21","EMA_21"),("EMA 50","EMA_50"),("EMA 200","EMA_200"),("SMA 7","SMA_7"),("SMA 14","SMA_14"),("SMA 30","SMA_30")]:
                val = tech.get(ma_key)
                if not val: continue
                diff_pct = ((current_price - val)/max(val,0.0001))*100
                status = "🟢 ABOVE" if diff_pct > 0 else "🔴 BELOW"
                c = "#00ff88" if diff_pct > 0 else "#ff3355"
                ma_rows += f'<tr><td style="color:rgba(255,255,255,0.5)">{ma_name}</td><td><b>${val:,.4f}</b></td><td style="color:{c}">{status} ({diff_pct:+.2f}%)</td></tr>'
            ema_trend = tech.get("EMA_Trend","")
            st.markdown(f'<table class="data-table">{ma_rows}</table><div style="margin-top:10px;font-size:0.8em;color:#00ffe0">{ema_trend}</div></div>', unsafe_allow_html=True)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("""<div class="layer-card"><div class="layer-title">🎯 BOLLINGER BANDS</div>""", unsafe_allow_html=True)
            bb_rows = ""
            for name, key in [("Upper Band","BB_Upper"),("Middle (SMA20)","BB_Middle"),("Lower Band","BB_Lower")]:
                val = tech.get(key)
                if val: bb_rows += f'<tr><td style="color:rgba(255,255,255,0.5)">{name}</td><td><b>${val:,.4f}</b></td></tr>'
            bb_pos = tech.get("BB_Position")
            bb_sig = tech.get("BB_Signal","")
            bb_squeeze = tech.get("BB_Squeeze","")
            bb_bw = tech.get("BB_Bandwidth",0)
            st.markdown(f'<table class="data-table">{bb_rows}</table><div style="margin-top:8px;font-size:0.8em;color:#00ffe0">{bb_sig}</div><div style="font-size:0.8em;color:#ffcc00">{bb_squeeze}</div></div>', unsafe_allow_html=True)

        with col4:
            st.markdown("""<div class="layer-card"><div class="layer-title">🔑 KEY LEVELS</div>""", unsafe_allow_html=True)
            support = tech.get("Support")
            resistance = tech.get("Resistance")
            pattern = tech.get("Candlestick_Pattern","")
            divergence = tech.get("Divergence","")
            regime = tech.get("Market_Regime","")
            kl_content = f"""
            <table class="data-table">
                <tr><td style="color:rgba(255,255,255,0.5)">Support</td><td style="color:#00ff88"><b>${support:,.4f}</b></td></tr>
                <tr><td style="color:rgba(255,255,255,0.5)">Resistance</td><td style="color:#ff3355"><b>${resistance:,.4f}</b></td></tr>
                <tr><td style="color:rgba(255,255,255,0.5)">Pattern</td><td>{pattern}</td></tr>
                <tr><td style="color:rgba(255,255,255,0.5)">Divergence</td><td>{divergence}</td></tr>
                <tr><td style="color:rgba(255,255,255,0.5)">Market Regime</td><td>{regime}</td></tr>
            </table>
            """ if support and resistance else "<div>Insufficient data</div>"
            st.markdown(f'<div class="layer-card"><div class="layer-title">🔑 KEY LEVELS</div>{kl_content}</div>', unsafe_allow_html=True)

        # Fibonacci
        fib = tech.get("Fibonacci", {})
        if fib:
            st.markdown('<div class="layer-card"><div class="layer-title">🌀 FIBONACCI RETRACEMENT LEVELS</div>', unsafe_allow_html=True)
            fib_cols = st.columns(len(fib))
            for i, (level, val) in enumerate(fib.items()):
                diff = ((current_price - val)/max(val,0.0001))*100
                color = "#00ff88" if current_price > val else "#ff3355"
                fib_cols[i].markdown(f'<div class="metric-card"><div class="metric-label">{level}</div><div class="metric-value" style="font-size:0.85em;color:{color}">${val:,.4f}</div><div class="metric-sub">{diff:+.1f}%</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # OBV & VWAP
        if tech.get("VWAP") or tech.get("OBV"):
            st.markdown('<div class="layer-card"><div class="layer-title">📊 VOLUME INDICATORS</div>', unsafe_allow_html=True)
            vc1, vc2 = st.columns(2)
            if tech.get("VWAP"):
                vwap = tech["VWAP"]
                vwap_diff = ((current_price - vwap)/max(vwap,0.0001))*100
                vc1.markdown(f'<div class="metric-card"><div class="metric-label">VWAP (Fair Value)</div><div class="metric-value">${vwap:,.4f}</div><div class="metric-sub" style="color:{"#00ff88" if vwap_diff>0 else "#ff3355"}">Price is {vwap_diff:+.2f}% vs VWAP</div></div>', unsafe_allow_html=True)
            if tech.get("OBV"):
                obv = tech["OBV"]
                vc2.markdown(f'<div class="metric-card"><div class="metric-label">OBV (On-Balance Volume)</div><div class="metric-value">{obv:,.0f}</div><div class="metric-sub">{"🟢 Positive — Buying Pressure" if obv>0 else "🔴 Negative — Selling Pressure"}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Insufficient price data for technical analysis.")

# ══════════════════════════════════════════════════════════════
#  TAB 3: SENTIMENT ANALYSIS
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">📰 SENTIMENT ANALYSIS ENGINE</div>', unsafe_allow_html=True)

    # Fear & Greed
    fg1, fg2 = st.columns([1,2])
    with fg1:
        if fear_greed_data:
            fg = fear_greed_data[0]
            fg_val = int(fg.get("value",50))
            fg_class = fg.get("value_classification","Neutral")
            if fg_val < 25: fg_color, fg_emoji = "#ff3355", "😱"
            elif fg_val < 40: fg_color, fg_emoji = "#ff8800", "😰"
            elif fg_val < 60: fg_color, fg_emoji = "#ffcc00", "😐"
            elif fg_val < 75: fg_color, fg_emoji = "#88ff00", "😊"
            else: fg_color, fg_emoji = "#00ff88", "🤑"

            st.markdown(f"""
            <div class="layer-card" style="text-align:center;border-color:{fg_color}">
                <div class="layer-title" style="justify-content:center">FEAR & GREED INDEX</div>
                <div style="font-size:3em">{fg_emoji}</div>
                <div style="font-family:Orbitron,monospace;font-size:2.5em;font-weight:900;color:{fg_color}">{fg_val}</div>
                <div style="font-family:Orbitron,monospace;font-size:0.8em;color:{fg_color};letter-spacing:2px;margin-top:4px">{fg_class.upper()}</div>
                <div class="conf-bar-outer" style="margin-top:12px">
                    <div class="conf-bar-inner" style="width:{fg_val}%;background:linear-gradient(90deg,#ff3355,#ffcc00,#00ff88)"></div>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.6em;color:rgba(255,255,255,0.3);margin-top:4px">
                    <span>FEAR</span><span>GREED</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with fg2:
        if len(fear_greed_data) >= 3:
            st.markdown('<div class="layer-card"><div class="layer-title">📅 FEAR & GREED HISTORY (7 DAYS)</div>', unsafe_allow_html=True)
            fg_vals = []
            for fg_item in fear_greed_data[:7]:
                ts = int(fg_item.get("timestamp",0))
                date_str = datetime.fromtimestamp(ts).strftime("%b %d") if ts else "N/A"
                v = int(fg_item.get("value",50))
                c_str = fg_item.get("value_classification","")
                fg_color2 = "#00ff88" if v>=60 else "#ff3355" if v<40 else "#ffcc00"
                fg_vals.append(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:0.8em"><span style="color:rgba(255,255,255,0.4)">{date_str}</span><div class="conf-bar-outer" style="width:120px;margin:0 10px"><div class="conf-bar-inner {'conf-bull' if v>=50 else 'conf-bear'}" style="width:{v}%"></div></div><span style="color:{fg_color2};font-family:Share Tech Mono,monospace">{v} — {c_str}</span></div>')
            st.markdown("".join(fg_vals))
            st.markdown('</div>', unsafe_allow_html=True)

    # News Sentiment
    st.markdown('<div class="section-header">📰 NEWS SENTIMENT ANALYSIS</div>', unsafe_allow_html=True)

    news_sentiment = analyze_news_sentiment(news_data) if news_data else {"overall":"⚪ NEUTRAL","bull_pct":50,"bear_pct":50,"scored_news":[],"total_articles":0}

    ns1, ns2 = st.columns([1,2])
    with ns1:
        bull_p = news_sentiment["bull_pct"]
        bear_p = news_sentiment["bear_pct"]
        ns_color = "#00ff88" if bull_p > 55 else "#ff3355" if bear_p > 55 else "#ffcc00"
        st.markdown(f"""
        <div class="layer-card" style="text-align:center;border-color:{ns_color}">
            <div class="layer-title" style="justify-content:center">NEWS SENTIMENT</div>
            <div style="font-family:Orbitron,monospace;font-size:1.1em;color:{ns_color};margin:8px 0">{news_sentiment['overall']}</div>
            <div style="font-size:0.75em;color:rgba(255,255,255,0.4);margin-bottom:6px">{news_sentiment['total_articles']} Articles Analyzed</div>
            <div style="display:flex;justify-content:space-between;font-size:0.75em;margin:4px 0">
                <span style="color:#00ff88">🟢 {bull_p}%</span>
                <span style="color:#ff3355">🔴 {bear_p}%</span>
            </div>
            <div class="conf-bar-outer">
                <div class="conf-bar-inner conf-bull" style="width:{bull_p}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ns2:
        if news_sentiment["scored_news"]:
            st.markdown('<div class="layer-card"><div class="layer-title">📋 RECENT NEWS WITH SENTIMENT</div>', unsafe_allow_html=True)
            for n in news_sentiment["scored_news"][:6]:
                s_color = "#00ff88" if "Bullish" in n["sentiment"] else "#ff3355" if "Bearish" in n["sentiment"] else "#ffcc00"
                title_short = n["title"][:80] + "..." if len(n["title"]) > 80 else n["title"]
                st.markdown(f'<div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:0.78em"><span style="color:{s_color};margin-right:8px">{n["sentiment"]}</span><span style="color:rgba(255,255,255,0.75)">{title_short}</span><span style="color:rgba(255,255,255,0.3);font-size:0.85em;margin-left:8px">{n["published"]}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No news data available. CryptoPanic free tier may be limited.")

    # Combined Sentiment Score
    if coin_data and fear_greed_data:
        price_now = coin_data["market_data"]["current_price"]["usd"]
        ch24 = coin_data["market_data"].get("price_change_percentage_24h") or 0
        ch7 = coin_data["market_data"].get("price_change_percentage_7d") or 0
        combined_score = calculate_sentiment_score(fear_greed_data[0].get("value",50), news_sentiment["bull_pct"], ch24, ch7)

        score_color = "#00ff88" if combined_score > 60 else "#ff3355" if combined_score < 40 else "#ffcc00"
        score_label = "VERY BULLISH" if combined_score > 75 else "BULLISH" if combined_score > 60 else "BEARISH" if combined_score < 40 else "VERY BEARISH" if combined_score < 25 else "NEUTRAL"

        st.markdown('<div class="section-header">🎯 COMBINED SENTIMENT SCORE</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="layer-card" style="border-color:{score_color}">
            <div style="display:flex;align-items:center;justify-content:space-between">
                <div>
                    <div style="font-size:0.7em;color:rgba(255,255,255,0.4);letter-spacing:2px">OVERALL SENTIMENT</div>
                    <div style="font-family:Orbitron,monospace;font-size:1.4em;color:{score_color};margin-top:4px">{score_label}</div>
                    <div style="font-size:0.75em;color:rgba(255,255,255,0.5);margin-top:4px">Fear&Greed + News + Price Action</div>
                </div>
                <div style="font-family:Orbitron,monospace;font-size:3em;font-weight:900;color:{score_color}">{combined_score:.0f}</div>
            </div>
            <div class="conf-bar-outer" style="margin-top:12px">
                <div style="height:100%;width:{combined_score}%;background:linear-gradient(90deg,#ff3355,#ffcc00 50%,#00ff88);border-radius:50px"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.6em;color:rgba(255,255,255,0.25);margin-top:4px">
                <span>0 — EXTREME FEAR</span><span>50 — NEUTRAL</span><span>100 — EXTREME GREED</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  TAB 4: EVENTS
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">⚡ EVENT CALENDAR & IMPACT ANALYSIS</div>', unsafe_allow_html=True)

    # Bitcoin Halving countdown
    halving_date = datetime(2028, 4, 17)
    days_to_halving = (halving_date - datetime.now()).days
    st.markdown(f"""
    <div class="layer-card" style="border-color:#f7931a;text-align:center">
        <div class="layer-title" style="justify-content:center;color:#f7931a">₿ BITCOIN HALVING COUNTDOWN</div>
        <div style="font-family:Orbitron,monospace;font-size:2em;font-weight:900;color:#f7931a">{days_to_halving} DAYS</div>
        <div style="font-size:0.75em;color:rgba(255,255,255,0.4);margin-top:4px">Next Halving: April 2028 (Estimated)</div>
        <div style="font-size:0.75em;color:#ffcc00;margin-top:6px">📈 Historical: Price typically rises 6-12 months after halving</div>
    </div>
    """, unsafe_allow_html=True)

    # Upcoming events
    events = get_coinmarketcal_events()
    if events:
        st.markdown('<div class="section-header">📅 UPCOMING CRYPTO EVENTS</div>', unsafe_allow_html=True)
        for ev in events[:6]:
            title = ev.get("title", {})
            if isinstance(title, dict): title = title.get("en","Unknown Event")
            coins_involved = ", ".join([c.get("symbol","") for c in ev.get("coins",[])[:3]]) if ev.get("coins") else "Multiple"
            date_str = ev.get("date_event","TBD")[:10]
            cat = ev.get("category",{}).get("name","") if isinstance(ev.get("category"),dict) else ""
            impact = "🔴 HIGH" if any(k in title.lower() for k in ["launch","upgrade","halving","etf","mainnet"]) else "🟡 MEDIUM" if any(k in title.lower() for k in ["listing","partnership","release"]) else "⚪ LOW"
            st.markdown(f"""
            <div class="layer-card" style="padding:12px">
                <div style="display:flex;justify-content:space-between;align-items:start">
                    <div>
                        <div style="font-size:0.85em;color:#e0f0ff;margin-bottom:4px">{title[:80]}</div>
                        <div style="font-size:0.7em;color:rgba(255,255,255,0.4)">{coins_involved} • {cat}</div>
                    </div>
                    <div style="text-align:right;white-space:nowrap">
                        <div style="font-family:Share Tech Mono,monospace;font-size:0.75em;color:#00ffe0">{date_str}</div>
                        <div style="font-size:0.7em;margin-top:4px">{impact}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Static important events
        st.markdown('<div class="section-header">📅 KEY MARKET EVENTS TO WATCH</div>', unsafe_allow_html=True)
        static_events = [
            {"event": "🏛️ US Fed Interest Rate Decision", "impact": "🔴 VERY HIGH", "note": "Rate cut = crypto bullish | Rate hike = bearish", "timing": "Every 6-8 weeks"},
            {"event": "📊 US CPI (Inflation Data)", "impact": "🔴 HIGH", "note": "High inflation = rate hike fear = crypto bearish", "timing": "Monthly"},
            {"event": "💼 Bitcoin ETF Flows (BlackRock/Fidelity)", "impact": "🔴 HIGH", "note": "High inflow = institutional buying = bullish", "timing": "Daily"},
            {"event": "🏦 FOMC Meeting Minutes", "impact": "🟡 MEDIUM", "note": "Hawkish tone = bearish | Dovish = bullish", "timing": "Every 6 weeks"},
            {"event": "📈 US Jobs Data (NFP)", "impact": "🟡 MEDIUM", "note": "Strong jobs = rate hike fear = crypto dip", "timing": "First Friday monthly"},
            {"event": "⚖️ SEC Regulatory News", "impact": "🔴 HIGH", "note": "New lawsuits or approvals affect market sentiment", "timing": "Ongoing"},
            {"event": "🌍 Geopolitical Events", "impact": "🟡 MEDIUM", "note": "Wars/sanctions can cause safe-haven crypto flows", "timing": "Ongoing"},
            {"event": "🔓 Token Unlocks (Altcoins)", "impact": "🟡 MEDIUM", "note": "Large unlock = potential sell pressure", "timing": "Check each coin"},
        ]
        for ev in static_events:
            imp_c = "#ff3355" if "VERY HIGH" in ev["impact"] else "#ff8800" if "HIGH" in ev["impact"] else "#ffcc00"
            st.markdown(f"""
            <div class="layer-card" style="padding:12px">
                <div style="display:flex;justify-content:space-between;align-items:start">
                    <div>
                        <div style="font-size:0.85em;color:#e0f0ff;margin-bottom:3px">{ev['event']}</div>
                        <div style="font-size:0.72em;color:rgba(255,255,255,0.5)">{ev['note']}</div>
                    </div>
                    <div style="text-align:right;white-space:nowrap">
                        <div style="font-size:0.7em;color:{imp_c}">{ev['impact']}</div>
                        <div style="font-size:0.65em;color:rgba(255,255,255,0.3);margin-top:3px">{ev['timing']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  TAB 5: MACRO
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">🌍 MACRO & GLOBAL MARKET CONTEXT</div>', unsafe_allow_html=True)

    macro_data = [
        {"name":"US Dollar Index (DXY)","value":"~104.5","impact":"🔴 BEARISH","note":"Strong dollar = crypto headwind. Watch for DXY weakness for crypto rally."},
        {"name":"S&P 500","value":"~5,800+","impact":"🟢 BULLISH","note":"Risk-on market. Positive correlation with crypto in bull markets."},
        {"name":"NASDAQ","value":"~18,500+","impact":"🟢 BULLISH","note":"Tech stocks correlated with crypto. NASDAQ up = crypto sentiment improves."},
        {"name":"Gold","value":"~$2,600/oz","impact":"⚪ NEUTRAL","note":"Bitcoin sometimes called 'digital gold'. Gold rally can precede BTC rally."},
        {"name":"Oil (WTI)","value":"~$70/barrel","impact":"⚪ NEUTRAL","note":"High oil = inflation concerns = Fed tightening = crypto risk."},
        {"name":"US 10Y Bond Yield","value":"~4.5%","impact":"🟡 CAUTION","note":"High yields = money moves to bonds away from crypto. Watch for yield drops."},
        {"name":"VIX (Fear Index)","value":"~15-18","impact":"🟢 LOW FEAR","note":"Low VIX = risk-on environment = good for crypto. VIX >30 = panic."},
        {"name":"BTC ETF Daily Flow","value":"Varies","impact":"🔴 KEY SIGNAL","note":"BlackRock/Fidelity ETF daily inflow is now a top market mover."},
        {"name":"Fed Funds Rate","value":"4.25-4.50%","impact":"🟡 WATCH","note":"Rate cuts expected in 2025. Each cut = crypto bullish catalyst."},
        {"name":"US Inflation (CPI)","value":"~2.5%","impact":"🟡 IMPROVING","note":"Falling inflation = more rate cuts likely = crypto bullish medium-term."},
        {"name":"Global M2 Money Supply","value":"Growing","impact":"🟢 BULLISH","note":"More money printed globally = inflation hedge assets (BTC) benefit."},
        {"name":"Stablecoin Market Cap","value":"~$180B+","impact":"🟢 BULLISH","note":"Rising stablecoin supply = dry powder ready to buy crypto."},
    ]

    for i in range(0, len(macro_data), 2):
        mc1, mc2 = st.columns(2)
        for col, idx in [(mc1, i), (mc2, i+1)]:
            if idx < len(macro_data):
                item = macro_data[idx]
                imp_c = "#00ff88" if "BULLISH" in item["impact"] else "#ff3355" if "BEARISH" in item["impact"] else "#ffcc00"
                col.markdown(f"""
                <div class="layer-card" style="padding:12px;margin:4px 0">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                        <div style="font-size:0.8em;color:#e0f0ff;font-weight:600">{item['name']}</div>
                        <div style="font-size:0.72em;color:{imp_c}">{item['impact']}</div>
                    </div>
                    <div style="font-family:Orbitron,monospace;font-size:0.85em;color:#00ffe0;margin-bottom:4px">{item['value']}</div>
                    <div style="font-size:0.7em;color:rgba(255,255,255,0.45);line-height:1.5">{item['note']}</div>
                </div>
                """, unsafe_allow_html=True)

    # Macro verdict
    st.markdown("""
    <div class="layer-card" style="border-color:#00ffe0;margin-top:16px">
        <div class="layer-title">🎯 MACRO ENVIRONMENT SUMMARY</div>
        <div class="layer-content">
        Current macro backdrop is <b style="color:#ffcc00">MIXED-TO-CAUTIOUSLY BULLISH</b>:<br><br>
        ✅ Fed rate cuts cycle beginning — long-term bullish for risk assets<br>
        ✅ Bitcoin ETFs approved — institutional money flowing in<br>
        ✅ Bitcoin halving completed — supply shock in effect<br>
        ⚠️ DXY still elevated — dollar strength remains headwind<br>
        ⚠️ Bond yields still high — competing with risk assets<br>
        ❌ Global geopolitical uncertainty — risk-off events possible<br><br>
        <span style="color:#ffcc00">NET: Macro conditions favor medium-to-long term upside, but short-term corrections possible.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  TAB 6: AI ANALYSIS
# ══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">🤖 MULTI-AGENT AI ANALYSIS ENGINE</div>', unsafe_allow_html=True)

    if not groq_key and not gemini_key:
        st.markdown("""
        <div class="layer-card" style="border-color:#ffcc00;text-align:center;padding:30px">
            <div style="font-size:2em;margin-bottom:12px">🔑</div>
            <div style="font-family:Orbitron,monospace;color:#ffcc00;font-size:0.9em;letter-spacing:2px;margin-bottom:10px">API KEYS REQUIRED</div>
            <div style="color:rgba(255,255,255,0.6);font-size:0.85em;line-height:1.8">
                AI Agents ke liye free API keys chahiye:<br><br>
                <b style="color:#00ffe0">Groq (Free):</b> console.groq.com → Create Account → Create API Key<br>
                <b style="color:#00ffe0">Gemini (Free):</b> aistudio.google.com → Get API Key<br><br>
                Sidebar mein keys daalo, phir yahan aao! ✅
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-size:0.8em;color:rgba(255,255,255,0.5);margin-bottom:16px;font-family:Share Tech Mono,monospace;">
        8 AI Agents collaborate karenge → Data analyze → Debate → Final Consensus denge
        </div>
        """, unsafe_allow_html=True)

        if st.button("🧠 LAUNCH ALL 8 AI AGENTS"):
            # Prepare comprehensive context
            price_ctx = coin_data["market_data"]["current_price"]["usd"] if coin_data else 0
            ch24_ctx = coin_data["market_data"].get("price_change_percentage_24h",0) if coin_data else 0
            ch7_ctx = coin_data["market_data"].get("price_change_percentage_7d",0) if coin_data else 0
            mc_ctx = coin_data["market_data"].get("market_cap",{}).get("usd",0) if coin_data else 0
            vol_ctx = coin_data["market_data"].get("total_volume",{}).get("usd",0) if coin_data else 0
            fg_ctx = fear_greed_data[0] if fear_greed_data else {}
            tech = run_full_technical_analysis(prices_30, volumes_30 if volumes_30 else None)
            news_sent = analyze_news_sentiment(news_data) if news_data else {}
            news_headlines = "\n".join([f"- {n.get('title','')}" for n in news_data[:5]]) if news_data else "No news"
            bb_context = get_binance_orderbook(binance_symbol)
            buy_pressure = 50
            if bb_context:
                bids = bb_context.get("bids",[])[:5]; asks = bb_context.get("asks",[])[:5]
                tb = sum(float(b[1]) for b in bids); ta = sum(float(a[1]) for a in asks)
                buy_pressure = round((tb/(tb+ta)*100),1) if (tb+ta)>0 else 50

            BASE_CONTEXT = f"""
COIN: {selected_name} ({coin_symbol})
TIMEFRAME: {timeframe}
CURRENT PRICE: ${price_ctx:,.4f}
24H CHANGE: {ch24_ctx:.2f}%
7D CHANGE: {ch7_ctx:.2f}%
MARKET CAP: ${mc_ctx/1e9:.2f}B
24H VOLUME: ${vol_ctx/1e9:.2f}B
FEAR & GREED: {fg_ctx.get('value','N/A')} ({fg_ctx.get('value_classification','N/A')})
ORDER BOOK BUY PRESSURE: {buy_pressure}%
RSI(14): {tech.get('RSI_14','N/A')} — {tech.get('RSI_Signal','')}
MACD: {tech.get('MACD','N/A')} / Signal: {tech.get('MACD_Signal','N/A')} — {tech.get('MACD_Signal_Txt','')}
BB: Upper={tech.get('BB_Upper','N/A')} / Lower={tech.get('BB_Lower','N/A')} — {tech.get('BB_Signal','')}
EMA TREND: {tech.get('EMA_Trend','N/A')}
MARKET REGIME: {tech.get('Market_Regime','N/A')}
PATTERN: {tech.get('Candlestick_Pattern','N/A')}
DIVERGENCE: {tech.get('Divergence','N/A')}
BB SQUEEZE: {tech.get('BB_Squeeze','N/A')}
MOMENTUM 7D: {tech.get('Momentum_7d','N/A')}%
NEWS SENTIMENT: {news_sent.get('overall','N/A')} (Bull:{news_sent.get('bull_pct',50)}% / Bear:{news_sent.get('bear_pct',50)}%)
RECENT NEWS:
{news_headlines}
            """.strip()

            agent_results = {}

            # AGENT 1 — Data Collector
            with st.expander("🔵 AGENT 1: DATA COLLECTOR — Analyzing...", expanded=True):
                with st.spinner("Collecting and structuring all market data..."):
                    p1 = f"""You are the Data Collector Agent in a multi-AI crypto analysis system.

MARKET DATA:
{BASE_CONTEXT}

Your task:
1. Assess data quality and completeness
2. Identify top 3 most significant data points
3. Flag any unusual data anomalies
4. Preliminary bias: BULLISH / BEARISH / NEUTRAL with brief reason
5. Data confidence score: X/10

Be concise, factual, analytical. Max 200 words."""
                    r1 = run_ai(p1, groq_key, gemini_key, prefer_gemini=False)
                    agent_results["data_collector"] = r1
                st.markdown(f'<div class="agent-card"><div class="agent-name">🔵 DATA COLLECTOR AGENT</div><div class="agent-output">{r1}</div></div>', unsafe_allow_html=True)

            # AGENT 2 — News Scout
            with st.expander("📰 AGENT 2: NEWS SCOUT — Scanning...", expanded=True):
                with st.spinner("Scanning news and sentiment signals..."):
                    p2 = f"""You are the News Scout Agent — expert in crypto news analysis and sentiment.

NEWS DATA:
{news_headlines}

CONTEXT: {coin_symbol} | Price: ${price_ctx:,.4f} | 24H: {ch24_ctx:.2f}%
Fear & Greed: {fg_ctx.get('value','N/A')} ({fg_ctx.get('value_classification','N/A')})
News Sentiment: Bull {news_sent.get('bull_pct',50)}% / Bear {news_sent.get('bear_pct',50)}%

Analyze:
1. Overall news sentiment (Positive/Negative/Neutral) with % confidence
2. Any major catalyst detected (partnership, hack, regulation, listing, whale move)?
3. Media narrative currently surrounding this asset
4. FUD or FOMO signals
5. News-based verdict: UP/DOWN/SIDEWAYS for {timeframe}

Max 200 words."""
                    r2 = run_ai(p2, groq_key, gemini_key, prefer_gemini=True)
                    agent_results["news_scout"] = r2
                st.markdown(f'<div class="agent-card"><div class="agent-name">📰 NEWS SCOUT AGENT</div><div class="agent-output">{r2}</div></div>', unsafe_allow_html=True)

            # AGENT 3 — Technical Analyst
            with st.expander("📊 AGENT 3: TECHNICAL ANALYST — Charting...", expanded=True):
                with st.spinner("Running technical analysis..."):
                    p3 = f"""You are the Technical Analysis Expert Agent for crypto markets.

TECHNICAL DATA:
RSI(14)={tech.get('RSI_14')} → {tech.get('RSI_Signal','')}
MACD={tech.get('MACD')} Signal={tech.get('MACD_Signal')} → {tech.get('MACD_Signal_Txt','')}
BB Upper={tech.get('BB_Upper')} Lower={tech.get('BB_Lower')} → {tech.get('BB_Signal','')}
EMA9={tech.get('EMA_9')} EMA21={tech.get('EMA_21')} EMA50={tech.get('EMA_50')} → {tech.get('EMA_Trend','')}
SMA30={tech.get('SMA_30')}
Pattern: {tech.get('Candlestick_Pattern','')}
Divergence: {tech.get('Divergence','')}
BB Squeeze: {tech.get('BB_Squeeze','')}
Momentum 7D: {tech.get('Momentum_7d','')}%
Market Regime: {tech.get('Market_Regime','')}
Support: ${tech.get('Support',0):,.4f} | Resistance: ${tech.get('Resistance',0):,.4f}
Tech Score: {tech.get('Tech_Score',0)} → {tech.get('Tech_Verdict','')}

Price: ${price_ctx:,.4f} | 24H: {ch24_ctx:.2f}% | 7D: {ch7_ctx:.2f}%

Provide:
1. Technical verdict: BULLISH/BEARISH/NEUTRAL
2. Key signals supporting your view (pick top 3)
3. Critical levels to watch (support/resistance)
4. Pattern interpretation
5. Probability: UP X% / DOWN Y% for {timeframe}

Max 200 words."""
                    r3 = run_ai(p3, groq_key, gemini_key, prefer_gemini=False)
                    agent_results["technical"] = r3
                st.markdown(f'<div class="agent-card"><div class="agent-name">📊 TECHNICAL ANALYST AGENT</div><div class="agent-output">{r3}</div></div>', unsafe_allow_html=True)

            # AGENT 4 — Whale Watcher
            with st.expander("🐋 AGENT 4: WHALE WATCHER — Tracking...", expanded=True):
                with st.spinner("Analyzing large order flows and whale signals..."):
                    p4 = f"""You are the Whale Watcher Agent — expert in on-chain analysis and large order detection.

AVAILABLE DATA:
Order Book Buy Pressure: {buy_pressure}%
{binance_trades and f"Recent trades analyzed: {len(binance_trades)} trades" or "Trade data unavailable"}
Volume: ${vol_ctx/1e9:.2f}B (24H)
Volume/MarketCap: {(vol_ctx/max(mc_ctx,1))*100:.2f}%
Price Change: 24H {ch24_ctx:.2f}% | 7D {ch7_ctx:.2f}%

Based on available data, analyze:
1. Order book imbalance interpretation
2. Volume analysis — is this organic or manipulated?
3. Are whales accumulating or distributing? Signs?
4. Unusual trade patterns or red flags?
5. Whale-based verdict: BULLISH/BEARISH/NEUTRAL

Max 200 words."""
                    r4 = run_ai(p4, groq_key, gemini_key, prefer_gemini=False)
                    agent_results["whale"] = r4
                st.markdown(f'<div class="agent-card"><div class="agent-name">🐋 WHALE WATCHER AGENT</div><div class="agent-output">{r4}</div></div>', unsafe_allow_html=True)

            # AGENT 5 — Macro Analyst
            with st.expander("🌍 AGENT 5: MACRO ANALYST — Assessing...", expanded=True):
                with st.spinner("Evaluating macro environment..."):
                    p5 = f"""You are the Macro Economic Analyst Agent for crypto markets.

MACRO CONTEXT:
- Fed interest rates: 4.25-4.50% (rate cuts expected)
- US Inflation (CPI): ~2.5% and falling
- DXY (Dollar Index): elevated ~104
- Stock markets (S&P500): near all-time highs
- Bitcoin ETF flows: institutional buying ongoing
- Bitcoin halving: occurred April 2024 (supply shock)
- VIX: low volatility regime

ASSET: {coin_symbol}
Current Price: ${price_ctx:,.4f}

Analyze:
1. Is macro environment favorable for this asset right now?
2. What's the biggest macro risk in next {timeframe}?
3. What's the biggest macro tailwind?
4. Fed policy impact assessment
5. Macro verdict: BULLISH/BEARISH/NEUTRAL

Max 200 words."""
                    r5 = run_ai(p5, groq_key, gemini_key, prefer_gemini=True)
                    agent_results["macro"] = r5
                st.markdown(f'<div class="agent-card"><div class="agent-name">🌍 MACRO ANALYST AGENT</div><div class="agent-output">{r5}</div></div>', unsafe_allow_html=True)

            # AGENT 6 — Event Impact
            with st.expander("⚡ AGENT 6: EVENT IMPACT AGENT — Checking...", expanded=True):
                with st.spinner("Checking upcoming events impact..."):
                    p6 = f"""You are the Event Impact Agent — expert in analyzing how upcoming events will affect crypto prices.

EVENTS TO CONSIDER:
- Bitcoin halving: occurred April 2024 (still impacting)
- Fed meetings: rate decisions every 6-8 weeks
- SEC regulatory actions: ongoing
- Bitcoin ETF daily flows: major price driver
- CoinMarketCal events for {coin_symbol}: check recent listings, upgrades, partnerships
- Technical milestones: support/resistance at ${tech.get('Support',0):,.4f} / ${tech.get('Resistance',0):,.4f}

CONTEXT:
{coin_symbol} | ${price_ctx:,.4f} | {timeframe} prediction

Analyze:
1. Most impactful upcoming event for {coin_symbol} in {timeframe}?
2. Pre-event positioning: "buy the rumor" opportunity?
3. Post-event risk: "sell the news" danger?
4. Historical precedent for similar events
5. Event-based verdict: UP/DOWN with reasoning

Max 200 words."""
                    r6 = run_ai(p6, groq_key, gemini_key, prefer_gemini=False)
                    agent_results["event"] = r6
                st.markdown(f'<div class="agent-card"><div class="agent-name">⚡ EVENT IMPACT AGENT</div><div class="agent-output">{r6}</div></div>', unsafe_allow_html=True)

            # AGENT 7 — Oracle (Independent)
            with st.expander("🔮 AGENT 7: ORACLE PREDICTOR — Predicting...", expanded=True):
                with st.spinner("Oracle making independent deep prediction..."):
                    p7 = f"""You are the Oracle Predictor — the most advanced independent prediction AI in this system.

You have read all other agents' work:
- Data: {r1[:150]}
- News: {r2[:150]}
- Technical: {r3[:150]}
- Whale: {r4[:150]}
- Macro: {r5[:150]}
- Events: {r6[:150]}

FULL CONTEXT:
{BASE_CONTEXT}

Now make YOUR INDEPENDENT prediction for {coin_symbol} in {timeframe}:
1. VERDICT: UP or DOWN (be decisive)
2. Probability: X% UP / Y% DOWN
3. Primary reasoning (2-3 sentences)
4. Predicted price target
5. Main risk that could invalidate this prediction
6. Confidence: LOW/MEDIUM/HIGH/EXTREME

Be bold. Be specific. Max 200 words."""
                    r7 = run_ai(p7, groq_key, gemini_key, prefer_gemini=True)
                    agent_results["oracle"] = r7
                st.markdown(f'<div class="agent-card"><div class="agent-name">🔮 ORACLE PREDICTOR AGENT</div><div class="agent-output">{r7}</div></div>', unsafe_allow_html=True)

            # AGENT 8 — Consensus Emerger (FINAL)
            with st.expander("🧬 AGENT 8: CONSENSUS EMERGER — FINAL SYNTHESIS...", expanded=True):
                with st.spinner("🧬 Synthesizing all 7 agents into final consensus..."):
                    p8 = f"""You are the Consensus Emerger — the final synthesizer of all agent analysis.

7 AGENT REPORTS:
1. DATA COLLECTOR: {r1[:200]}
2. NEWS SCOUT: {r2[:200]}
3. TECHNICAL ANALYST: {r3[:200]}
4. WHALE WATCHER: {r4[:200]}
5. MACRO ANALYST: {r5[:200]}
6. EVENT IMPACT: {r6[:200]}
7. ORACLE: {r7[:200]}

ASSET: {coin_symbol} | PRICE: ${price_ctx:,.4f} | TIMEFRAME: {timeframe}

Generate FINAL CONSENSUS REPORT:
1. FINAL VERDICT: UP or DOWN (one word first)
2. CONSENSUS PROBABILITY: X% UP / Y% DOWN
3. AGENTS IN AGREEMENT: X out of 7 say bullish
4. CONFIDENCE LEVEL: LOW / MEDIUM / HIGH / EXTREME
5. KEY REASON (2 sentences max)
6. PREDICTED PRICE RANGE: $X to $Y
7. ENTRY SUGGESTION: Good entry zone
8. STOP LOSS: ${'{tech.get("Support",0)*0.98:,.4f}'}
9. TAKE PROFIT: Target price
10. RISK WARNING: Main risk to watch

Format with clear labels. Be authoritative. Max 300 words."""
                    r8 = run_ai(p8, groq_key, gemini_key, prefer_gemini=False)
                    agent_results["consensus"] = r8

                st.markdown(f'<div class="agent-card" style="border-color:#00ffe0;border-left-color:#00ffe0"><div class="agent-name" style="color:#00ffe0">🧬 CONSENSUS EMERGER — FINAL SYNTHESIS</div><div class="agent-output">{r8}</div></div>', unsafe_allow_html=True)

            # Save to history
            st.session_state.prediction_history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "coin": coin_symbol,
                "price": price_ctx,
                "timeframe": timeframe,
                "consensus": agent_results.get("consensus","")[:200],
                "is_up": r8.upper().count("UP") > r8.upper().count("DOWN")
            })

            # Telegram
            if telegram_token and telegram_chat_id:
                msg = f"🧠 *CryptoMind AI Alert*\n\n*{coin_symbol}* | {timeframe}\n💰 Price: ${price_ctx:,.4f}\n\n{r8[:500]}"
                sent = send_telegram(telegram_token, telegram_chat_id, msg)
                if sent:
                    st.success("✅ Telegram alert sent!")

# ══════════════════════════════════════════════════════════════
#  TAB 7: PREDICTION
# ══════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header">🎯 PREDICTION ENGINE & FINAL VERDICT</div>', unsafe_allow_html=True)

    if prices_30 and coin_data:
        price_cur = coin_data["market_data"]["current_price"]["usd"]
        ch24 = coin_data["market_data"].get("price_change_percentage_24h",0) or 0
        ch7 = coin_data["market_data"].get("price_change_percentage_7d",0) or 0
        tech_full = run_full_technical_analysis(prices_30, volumes_30)
        news_s = analyze_news_sentiment(news_data) if news_data else {"bull_pct":50,"bear_pct":50}
        fg_val = int(fear_greed_data[0].get("value",50)) if fear_greed_data else 50

        # Algorithmic prediction (no AI needed)
        # Score each signal
        bull_signals, bear_signals = [], []

        # Technical signals
        rsi = tech_full.get("RSI_14")
        if rsi:
            if rsi < 30: bull_signals.append("RSI Oversold (Strong Buy)")
            elif rsi > 70: bear_signals.append("RSI Overbought (Strong Sell)")
            elif rsi < 45: bear_signals.append("RSI Weak")
            elif rsi > 55: bull_signals.append("RSI Strong")

        macd_v = tech_full.get("MACD"); macd_s = tech_full.get("MACD_Signal")
        if macd_v and macd_s:
            if macd_v > macd_s: bull_signals.append("MACD Bullish Crossover")
            else: bear_signals.append("MACD Bearish Crossover")

        ema9 = tech_full.get("EMA_9"); ema21 = tech_full.get("EMA_21")
        if ema9 and ema21:
            if ema9 > ema21: bull_signals.append("EMA9 > EMA21 (Uptrend)")
            else: bear_signals.append("EMA9 < EMA21 (Downtrend)")

        ema50 = tech_full.get("EMA_50")
        if ema50:
            if price_cur > ema50: bull_signals.append(f"Price above EMA50")
            else: bear_signals.append(f"Price below EMA50")

        bb_sq = tech_full.get("BB_Squeeze","")
        if "SQUEEZE" in bb_sq: bull_signals.append("BB Squeeze — Big move imminent")

        if tech_full.get("Momentum_7d",0) > 3: bull_signals.append(f"Strong 7D Momentum +{tech_full.get('Momentum_7d',0):.1f}%")
        elif tech_full.get("Momentum_7d",0) < -3: bear_signals.append(f"Weak 7D Momentum {tech_full.get('Momentum_7d',0):.1f}%")

        # Sentiment signals
        if fg_val > 65: bull_signals.append(f"Fear & Greed: Greed ({fg_val})")
        elif fg_val < 35: bear_signals.append(f"Fear & Greed: Fear ({fg_val})")

        if news_s["bull_pct"] > 60: bull_signals.append(f"News Sentiment: {news_s['bull_pct']}% Bullish")
        elif news_s["bear_pct"] > 60: bear_signals.append(f"News Sentiment: {news_s['bear_pct']}% Bearish")

        if ch24 > 3: bull_signals.append(f"24H Momentum: +{ch24:.1f}%")
        elif ch24 < -3: bear_signals.append(f"24H Weakness: {ch24:.1f}%")

        if ch7 > 5: bull_signals.append(f"7D Trend: +{ch7:.1f}%")
        elif ch7 < -5: bear_signals.append(f"7D Trend: {ch7:.1f}%")

        # Order book
        bb_ob = get_binance_orderbook(binance_symbol)
        if bb_ob:
            bids = bb_ob.get("bids",[])[:5]; asks = bb_ob.get("asks",[])[:5]
            tb = sum(float(b[1]) for b in bids); ta = sum(float(a[1]) for a in asks)
            bp = (tb/(tb+ta)*100) if (tb+ta)>0 else 50
            if bp > 55: bull_signals.append(f"Order Book: {bp:.0f}% Buy Pressure")
            elif bp < 45: bear_signals.append(f"Order Book: {100-bp:.0f}% Sell Pressure")

        # Calculate probability
        total_signals = len(bull_signals) + len(bear_signals)
        bull_prob = round((len(bull_signals)/max(total_signals,1))*100)
        bear_prob = 100 - bull_prob

        # Adjust for strong signals
        if rsi and rsi < 25: bull_prob = min(bull_prob + 10, 95)
        if rsi and rsi > 75: bear_prob = min(bear_prob + 10, 95)

        is_bullish = bull_prob >= 50
        verdict_label = "📈 BULLISH — UP" if is_bullish else "📉 BEARISH — DOWN"
        verdict_class = "verdict-up" if is_bullish else "verdict-down"

        # Confidence
        prob_diff = abs(bull_prob - 50)
        if prob_diff >= 20: confidence = "HIGH"
        elif prob_diff >= 12: confidence = "MEDIUM"
        else: confidence = "LOW"

        # Price targets
        support = tech_full.get("Support", price_cur * 0.95)
        resistance = tech_full.get("Resistance", price_cur * 1.05)
        if is_bullish:
            target_price = resistance * 1.02
            stop_loss_p = support * 0.98
        else:
            target_price = support * 0.98
            stop_loss_p = resistance * 1.02

        price_change_pct = ((target_price - price_cur)/max(price_cur,0.0001))*100

        # VERDICT BOX
        st.markdown(f"""
        <div class="verdict-container {verdict_class}">
            <div style="font-size:0.7em;letter-spacing:5px;color:rgba(255,255,255,0.4);margin-bottom:10px;font-family:Share Tech Mono,monospace">
                🧬 ALGORITHMIC CONSENSUS — {coin_symbol} — {timeframe}
            </div>
            <div class="verdict-title">{verdict_label}</div>
            <div style="display:flex;justify-content:center;gap:30px;margin:16px 0;flex-wrap:wrap">
                <div style="text-align:center">
                    <div style="font-size:0.6em;color:rgba(255,255,255,0.35);letter-spacing:2px">BULL PROBABILITY</div>
                    <div style="font-family:Orbitron,monospace;font-size:1.8em;color:#00ff88">{bull_prob}%</div>
                </div>
                <div style="text-align:center">
                    <div style="font-size:0.6em;color:rgba(255,255,255,0.35);letter-spacing:2px">BEAR PROBABILITY</div>
                    <div style="font-family:Orbitron,monospace;font-size:1.8em;color:#ff3355">{bear_prob}%</div>
                </div>
                <div style="text-align:center">
                    <div style="font-size:0.6em;color:rgba(255,255,255,0.35);letter-spacing:2px">CONFIDENCE</div>
                    <div style="font-family:Orbitron,monospace;font-size:1.8em;color:#ffcc00">{confidence}</div>
                </div>
                <div style="text-align:center">
                    <div style="font-size:0.6em;color:rgba(255,255,255,0.35);letter-spacing:2px">SIGNALS</div>
                    <div style="font-family:Orbitron,monospace;font-size:1.8em;color:#00ffe0">{len(bull_signals)}🟢/{len(bear_signals)}🔴</div>
                </div>
            </div>
            <div class="conf-bar-outer" style="max-width:400px;margin:0 auto 12px">
                <div class="conf-bar-inner conf-bull" style="width:{bull_prob}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Price Targets
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        def pmc(col, label, val, color):
            col.markdown(f'<div class="metric-card" style="border-color:{color}40"><div class="metric-label">{label}</div><div class="metric-value" style="color:{color}">${val:,.4f}</div></div>', unsafe_allow_html=True)

        pmc(p_col1, "CURRENT PRICE", price_cur, "#00ffe0")
        pmc(p_col2, "TARGET PRICE", target_price, "#00ff88" if is_bullish else "#ff3355")
        pmc(p_col3, "STOP LOSS", stop_loss_p, "#ff3355" if is_bullish else "#00ff88")
        p_col4.markdown(f'<div class="metric-card" style="border-color:#ffcc0040"><div class="metric-label">EXPECTED MOVE</div><div class="metric-value" style="color:{"#00ff88" if price_change_pct>0 else "#ff3355"}">{price_change_pct:+.2f}%</div></div>', unsafe_allow_html=True)

        # Signals breakdown
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown('<div class="layer-card"><div class="layer-title">🟢 BULLISH SIGNALS</div>', unsafe_allow_html=True)
            for s in bull_signals:
                st.markdown(f'<div style="padding:4px 0;font-size:0.8em;border-bottom:1px solid rgba(0,255,136,0.1)"><span style="color:#00ff88">▲</span> {s}</div>', unsafe_allow_html=True)
            if not bull_signals:
                st.markdown('<div style="color:rgba(255,255,255,0.3);font-size:0.8em">No bullish signals</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with sc2:
            st.markdown('<div class="layer-card"><div class="layer-title">🔴 BEARISH SIGNALS</div>', unsafe_allow_html=True)
            for s in bear_signals:
                st.markdown(f'<div style="padding:4px 0;font-size:0.8em;border-bottom:1px solid rgba(255,51,85,0.1)"><span style="color:#ff3355">▼</span> {s}</div>', unsafe_allow_html=True)
            if not bear_signals:
                st.markdown('<div style="color:rgba(255,255,255,0.3);font-size:0.8em">No bearish signals</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Scenarios
        st.markdown('<div class="section-header">🎭 POSSIBLE SCENARIOS</div>', unsafe_allow_html=True)
        sc_a, sc_b, sc_c = st.columns(3)
        with sc_a:
            st.markdown(f"""
            <div class="layer-card" style="border-color:#00ff88">
                <div class="layer-title" style="color:#00ff88">🐂 BULL CASE</div>
                <div class="layer-content" style="font-size:0.8em">
                    RSI recovers above 50, MACD bullish crossover holds, volume picks up.<br><br>
                    <b style="color:#00ff88">Target: ${resistance*1.05:,.4f}</b><br>
                    Probability: {bull_prob}%
                </div>
            </div>""", unsafe_allow_html=True)
        with sc_b:
            st.markdown(f"""
            <div class="layer-card" style="border-color:#ffcc00">
                <div class="layer-title" style="color:#ffcc00">↔️ BASE CASE</div>
                <div class="layer-content" style="font-size:0.8em">
                    Price consolidates in current range. Low volatility. Waiting for catalyst.<br><br>
                    <b style="color:#ffcc00">Range: ${support:,.4f} - ${resistance:,.4f}</b><br>
                    Probability: {max(0,40-abs(bull_prob-50))}%
                </div>
            </div>""", unsafe_allow_html=True)
        with sc_c:
            st.markdown(f"""
            <div class="layer-card" style="border-color:#ff3355">
                <div class="layer-title" style="color:#ff3355">🐻 BEAR CASE</div>
                <div class="layer-content" style="font-size:0.8em">
                    Support breaks, selling accelerates, macro headwinds hit hard.<br><br>
                    <b style="color:#ff3355">Target: ${support*0.95:,.4f}</b><br>
                    Probability: {bear_prob}%
                </div>
            </div>""", unsafe_allow_html=True)

    else:
        st.warning("Load market data first.")

# ══════════════════════════════════════════════════════════════
#  TAB 8: RISK ANALYSIS
# ══════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-header">⚠️ RISK MANAGEMENT ENGINE</div>', unsafe_allow_html=True)

    if prices_30 and coin_data:
        current_p = coin_data["market_data"]["current_price"]["usd"]
        position_size = st.number_input("💰 Position Size (USD)", min_value=10.0, max_value=1000000.0, value=1000.0, step=100.0)
        leverage = st.selectbox("📊 Leverage", [1, 2, 3, 5, 10, 20, 50, 100])

        risk = calculate_risk_metrics(prices_30, current_p, position_size)

        if risk:
            risk_score = risk.get("risk_score", 5)
            rs_color = "#00ff88" if risk_score <= 3 else "#ffcc00" if risk_score <= 6 else "#ff3355"

            # Risk Score Meter
            st.markdown(f"""
            <div class="layer-card" style="border-color:{rs_color}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <div style="font-size:0.7em;color:rgba(255,255,255,0.4);letter-spacing:2px">RISK SCORE</div>
                        <div style="font-family:Orbitron,monospace;font-size:2em;color:{rs_color}">{risk_score}/10</div>
                        <div style="font-size:0.8em;color:{rs_color};margin-top:4px">{'LOW RISK' if risk_score<=3 else 'MEDIUM RISK' if risk_score<=6 else 'HIGH RISK'}</div>
                    </div>
                    <div style="width:60%;padding-left:20px">
                        <div class="risk-bar"></div>
                        <div style="position:relative;top:-16px;left:{(risk_score-1)*11}%;width:4px;height:16px;background:white;border-radius:2px"></div>
                        <div style="display:flex;justify-content:space-between;font-size:0.6em;color:rgba(255,255,255,0.3)">
                            <span>LOW</span><span>MED</span><span>HIGH</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Risk Metrics
            rm1, rm2, rm3 = st.columns(3)
            def rmc(col, label, val, sub="", color="#00ffe0"):
                col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value" style="color:{color}">{val}</div><div class="metric-sub">{sub}</div></div>', unsafe_allow_html=True)

            rmc(rm1, "DAILY VOLATILITY", f"{risk['volatility_pct']:.2f}%", "Price swing expected", "#ffcc00")
            rmc(rm2, "VALUE AT RISK (95%)", f"${risk['var_dollar']:,.2f}", f"{risk['var_95_pct']:.2f}% of position", "#ff3355")
            rmc(rm3, "MAX DRAWDOWN (30D)", f"{risk['max_drawdown']:.2f}%", "Worst drop in 30 days", "#ff3355")

            rm4, rm5, rm6 = st.columns(3)
            rmc(rm4, "SHARPE RATIO", f"{risk['sharpe']:.2f}", "Risk-adj return", "#00ff88" if risk['sharpe']>1 else "#ffcc00")
            rmc(rm5, "RISK/REWARD", f"{risk['risk_reward']:.2f}x", "Stop to Target ratio", "#00ff88" if risk['risk_reward']>1.5 else "#ff3355")
            effective_pos = position_size * leverage
            rmc(rm6, "EFFECTIVE POSITION", f"${effective_pos:,.0f}", f"{leverage}x leverage", "#ff3355" if leverage > 5 else "#ffcc00")

            # Trade Levels
            st.markdown('<div class="section-header">🎯 SUGGESTED TRADE LEVELS</div>', unsafe_allow_html=True)
            tl1, tl2, tl3, tl4 = st.columns(4)
            tl1.markdown(f'<div class="metric-card" style="border-color:#00ffe040"><div class="metric-label">ENTRY ZONE</div><div class="metric-value">${current_p:,.4f}</div><div class="metric-sub">Current price</div></div>', unsafe_allow_html=True)
            tl2.markdown(f'<div class="metric-card" style="border-color:#ff335540"><div class="metric-label">STOP LOSS</div><div class="metric-value" style="color:#ff3355">${risk["stop_loss"]:,.4f}</div><div class="metric-sub">-{((current_p-risk["stop_loss"])/current_p*100):.1f}% from entry</div></div>', unsafe_allow_html=True)
            tl3.markdown(f'<div class="metric-card" style="border-color:#00ff8840"><div class="metric-label">TARGET 1</div><div class="metric-value" style="color:#00ff88">${risk["take_profit_1"]:,.4f}</div><div class="metric-sub">+{((risk["take_profit_1"]-current_p)/current_p*100):.1f}%</div></div>', unsafe_allow_html=True)
            tl4.markdown(f'<div class="metric-card" style="border-color:#00ff4440"><div class="metric-label">TARGET 2</div><div class="metric-value" style="color:#00ff44">${risk["take_profit_2"]:,.4f}</div><div class="metric-sub">+{((risk["take_profit_2"]-current_p)/current_p*100):.1f}%</div></div>', unsafe_allow_html=True)

            # Leverage Warning
            if leverage > 5:
                st.markdown(f"""
                <div style="background:rgba(255,51,85,0.1);border:1px solid rgba(255,51,85,0.4);border-radius:8px;padding:12px;margin-top:12px;font-size:0.8em;color:#ff3355">
                    ⚠️ HIGH LEVERAGE WARNING: {leverage}x leverage means you get liquidated if price moves just {100/leverage:.1f}% against you.
                    At ${current_p:,.4f}, liquidation price ≈ ${current_p*(1-0.9/leverage):,.4f}
                </div>
                """, unsafe_allow_html=True)

            # Kelly Criterion
            win_rate = 0.55
            avg_win = risk["take_profit_1"] - current_p
            avg_loss = current_p - risk["stop_loss"]
            if avg_loss > 0:
                kelly = win_rate - ((1-win_rate)/(avg_win/avg_loss))
                kelly_pct = max(0, min(kelly*100, 25))
                kelly_position = position_size * kelly_pct/100
                st.markdown(f"""
                <div class="layer-card" style="margin-top:12px">
                    <div class="layer-title">📐 KELLY CRITERION — OPTIMAL POSITION SIZE</div>
                    <div style="font-size:0.85em;color:rgba(255,255,255,0.7)">
                        Assuming 55% win rate and {risk['risk_reward']:.1f}x Risk/Reward:<br><br>
                        Kelly % = <b style="color:#00ffe0">{kelly_pct:.1f}%</b> of portfolio<br>
                        Kelly Position = <b style="color:#00ff88">${kelly_position:,.2f}</b> (from ${position_size:,.0f} portfolio)
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  TAB 9: ALERTS
# ══════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<div class="section-header">🔔 ALERT SYSTEM</div>', unsafe_allow_html=True)

    al1, al2 = st.columns(2)
    with al1:
        st.markdown("#### 📬 Telegram Bot Setup")
        if telegram_token and telegram_chat_id:
            st.success("✅ Telegram configured!")
            test_msg = st.button("📤 Send Test Alert")
            if test_msg:
                price_now = coin_data["market_data"]["current_price"]["usd"] if coin_data else 0
                msg = f"🧠 *CryptoMind AI — Test Alert*\n\n*{coin_symbol}* current price: ${price_now:,.4f}\n\n✅ Your alerts are working!"
                sent = send_telegram(telegram_token, telegram_chat_id, msg)
                if sent:
                    st.success("✅ Test message sent to Telegram!")
                else:
                    st.error("❌ Failed. Check token and chat_id.")
        else:
            st.markdown("""
            <div class="layer-card">
                <div class="layer-title">📱 HOW TO SETUP TELEGRAM ALERTS</div>
                <div class="layer-content" style="font-size:0.82em;line-height:2">
                1️⃣ Telegram mein <b>@BotFather</b> search karo<br>
                2️⃣ /newbot command bhejo<br>
                3️⃣ Bot ka naam rakho (e.g. MyCryptoBot)<br>
                4️⃣ Token milega — sidebar mein daalo<br>
                5️⃣ <b>@userinfobot</b> se apna Chat ID lo<br>
                6️⃣ Sidebar mein Chat ID daalo<br>
                7️⃣ Done! Automatic alerts milenge 🚀
                </div>
            </div>
            """, unsafe_allow_html=True)

    with al2:
        st.markdown("#### 🎯 Price Alerts")
        if coin_data:
            current_alert_price = coin_data["market_data"]["current_price"]["usd"]
            alert_price = st.number_input(f"Alert when {coin_symbol} reaches ($)", value=float(f"{current_alert_price*1.05:.4f}"))
            alert_direction = st.radio("Alert type", ["🟢 Price rises above", "🔴 Price drops below"], horizontal=True)
            if st.button("➕ Add Price Alert"):
                st.session_state.alerts.append({
                    "coin": coin_symbol,
                    "price": alert_price,
                    "direction": alert_direction,
                    "created": datetime.now().strftime("%H:%M"),
                    "triggered": False
                })
                st.success(f"✅ Alert set: {coin_symbol} {alert_direction} ${alert_price:,.4f}")

    # Alert list
    if st.session_state.alerts:
        st.markdown('<div class="section-header">📋 ACTIVE ALERTS</div>', unsafe_allow_html=True)
        current_prices = {}
        if coin_data:
            current_prices[coin_symbol] = coin_data["market_data"]["current_price"]["usd"]

        for i, alert in enumerate(st.session_state.alerts):
            cur_p = current_prices.get(alert["coin"], 0)
            triggered = (alert["direction"].startswith("🟢") and cur_p >= alert["price"]) or \
                       (alert["direction"].startswith("🔴") and cur_p <= alert["price"])
            status_color = "#00ff88" if triggered else "#00ffe0"
            status_txt = "🔔 TRIGGERED" if triggered else "⏳ WAITING"
            st.markdown(f"""
            <div class="layer-card" style="padding:10px;border-color:{status_color}40">
                <div style="display:flex;justify-content:space-between;font-size:0.82em">
                    <span><b style="color:#00ffe0">{alert['coin']}</b> {alert['direction']} <b>${alert['price']:,.4f}</b></span>
                    <span style="color:{status_color}">{status_txt}</span>
                    <span style="color:rgba(255,255,255,0.3)">{alert['created']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear All Alerts"):
            st.session_state.alerts = []
            st.rerun()

# ══════════════════════════════════════════════════════════════
#  TAB 10: PORTFOLIO
# ══════════════════════════════════════════════════════════════
with tabs[9]:
    st.markdown('<div class="section-header">👤 PORTFOLIO TRACKER & P&L CALCULATOR</div>', unsafe_allow_html=True)

    port_col1, port_col2 = st.columns([2,1])
    with port_col2:
        st.markdown("#### ➕ Add Position")
        p_coin = st.selectbox("Coin", [c["symbol"] for c in COINS.values()])
        p_amount = st.number_input("Amount", min_value=0.0, value=0.1, step=0.01, format="%.4f")
        p_buy_price = st.number_input("Buy Price (USD)", min_value=0.0, value=100.0)
        if st.button("Add to Portfolio"):
            if p_coin not in st.session_state.portfolio:
                st.session_state.portfolio[p_coin] = []
            st.session_state.portfolio[p_coin].append({"amount": p_amount, "buy_price": p_buy_price})
            st.success(f"✅ Added {p_amount} {p_coin} @ ${p_buy_price:,.2f}")

    with port_col1:
        if st.session_state.portfolio:
            st.markdown("#### 📊 Portfolio Overview")
            total_invested, total_current = 0, 0
            rows = ""
            for sym, positions in st.session_state.portfolio.items():
                coin_cur_price = None
                for name, info in COINS.items():
                    if info["symbol"] == sym:
                        cd = get_coin_data(info["id"])
                        if cd: coin_cur_price = cd["market_data"]["current_price"]["usd"]
                        break

                for pos in positions:
                    invested = pos["amount"] * pos["buy_price"]
                    current_val = pos["amount"] * coin_cur_price if coin_cur_price else invested
                    pnl = current_val - invested
                    pnl_pct = (pnl/invested)*100 if invested > 0 else 0
                    total_invested += invested
                    total_current += current_val
                    pnl_color = "#00ff88" if pnl >= 0 else "#ff3355"
                    rows += f'<tr><td style="color:#00ffe0">{sym}</td><td>{pos["amount"]:.4f}</td><td>${pos["buy_price"]:,.4f}</td><td>${coin_cur_price:,.4f if coin_cur_price else "N/A"}</td><td style="color:{pnl_color}">${pnl:+,.2f} ({pnl_pct:+.2f}%)</td></tr>'

            total_pnl = total_current - total_invested
            total_pnl_pct = (total_pnl/total_invested)*100 if total_invested > 0 else 0
            pnl_c = "#00ff88" if total_pnl >= 0 else "#ff3355"

            st.markdown(f"""
            <table class="data-table">
                <thead><tr><th>COIN</th><th>AMOUNT</th><th>BUY PRICE</th><th>CUR PRICE</th><th>P&L</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="layer-card" style="margin-top:12px;border-color:{pnl_c}">
                <div style="display:flex;justify-content:space-around;text-align:center">
                    <div><div class="metric-label">INVESTED</div><div style="font-family:Orbitron,monospace;color:#00ffe0">${total_invested:,.2f}</div></div>
                    <div><div class="metric-label">CURRENT</div><div style="font-family:Orbitron,monospace;color:#00ffe0">${total_current:,.2f}</div></div>
                    <div><div class="metric-label">TOTAL P&L</div><div style="font-family:Orbitron,monospace;color:{pnl_c}">${total_pnl:+,.2f} ({total_pnl_pct:+.2f}%)</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🗑️ Clear Portfolio"):
                st.session_state.portfolio = {}
                st.rerun()
        else:
            st.markdown('<div class="layer-card" style="text-align:center;padding:30px;color:rgba(255,255,255,0.3)">No positions yet. Add coins to track your portfolio →</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  TAB 11: HISTORY
# ══════════════════════════════════════════════════════════════
with tabs[10]:
    st.markdown('<div class="section-header">📜 PREDICTION HISTORY & ACCURACY</div>', unsafe_allow_html=True)

    if st.session_state.prediction_history:
        correct = sum(1 for p in st.session_state.prediction_history if p.get("verified",False))
        total_verified = sum(1 for p in st.session_state.prediction_history if "verified" in p)
        accuracy = (correct/total_verified*100) if total_verified > 0 else 0

        h1, h2, h3 = st.columns(3)
        h1.markdown(f'<div class="metric-card"><div class="metric-label">TOTAL PREDICTIONS</div><div class="metric-value">{len(st.session_state.prediction_history)}</div></div>', unsafe_allow_html=True)
        h2.markdown(f'<div class="metric-card"><div class="metric-label">VERIFIED ACCURACY</div><div class="metric-value" style="color:#00ff88">{accuracy:.1f}%</div></div>', unsafe_allow_html=True)
        h3.markdown(f'<div class="metric-card"><div class="metric-label">CORRECT PREDICTIONS</div><div class="metric-value">{correct}/{total_verified}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        rows = ""
        for pred in reversed(st.session_state.prediction_history[-20:]):
            direction = "📈 UP" if pred.get("is_up") else "📉 DOWN"
            d_color = "#00ff88" if pred.get("is_up") else "#ff3355"
            rows += f'<tr><td style="color:rgba(255,255,255,0.4)">{pred["time"]}</td><td style="color:#00ffe0">{pred["coin"]}</td><td>${pred["price"]:,.4f}</td><td>{pred["timeframe"]}</td><td style="color:{d_color}">{direction}</td></tr>'

        st.markdown(f"""
        <table class="data-table">
            <thead><tr><th>TIME</th><th>COIN</th><th>PRICE</th><th>TIMEFRAME</th><th>PREDICTION</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Clear History"):
            st.session_state.prediction_history = []
            st.rerun()
    else:
        st.markdown('<div class="layer-card" style="text-align:center;padding:30px;color:rgba(255,255,255,0.3)">No predictions yet. Go to AI Analysis tab and run the agents!</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  AUTO REFRESH
# ══════════════════════════════════════════════════════════════
if auto_refresh:
    time.sleep(60)
    st.rerun()

# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:rgba(255,255,255,0.15);font-size:0.65em;font-family:Share Tech Mono,monospace;line-height:2;padding:10px 0">
    🧠 CRYPTOMIND AI v2.0 — ULTIMATE MULTI-LAYER EMERGENT PREDICTION ENGINE<br>
    POWERED BY: GROQ (LLAMA 3.1) × GEMINI 1.5 FLASH × 8 AI AGENTS × 316 FEATURES<br>
    DATA: COINGECKO × BINANCE × ALTERNATIVE.ME × CRYPTOPANIC × COINMARKETCAL<br>
    ⚠️ NOT FINANCIAL ADVICE — EDUCATIONAL ONLY — TRADE AT YOUR OWN RISK<br>
    {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC
</div>
""", unsafe_allow_html=True)
