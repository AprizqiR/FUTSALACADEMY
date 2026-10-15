"""
==========================================
BIAENERGI FUTSAL ACADEMY — v5.0 (Fase 1)
==========================================
Menu: Home | Team | Team Generator (placeholder) | Match History (placeholder) | About
Data: JSON lokal (mudah dimigrasi ke Google Sheets di Fase 4)
"""
import streamlit as st
import pandas as pd
import json
import os
import base64
from pathlib import Path
from html import escape as esc

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="BIAENERGI Futsal Academy",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 🎨 CSS BIAENERGI THEME
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Orbitron:wght@700;900&display=swap');

:root {
  --bng-navy:#0a1a3a;
  --bng-navy-2:#0d2350;
  --bng-blue:#1e3a8a;
  --bng-blue-light:#3b82f6;
  --bng-yellow:#fbbf24;
  --bng-yellow-dark:#f59e0b;
  --bng-cyan:#20d9e8;
  --bng-white:#f8fafc;
  --bng-text-dim:#94a3b8;
  --bng-glass:rgba(13,35,80,.6);
  --bng-glass-border:rgba(96,165,250,.25);
}

html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* ============ BACKGROUND ============ */
.stApp {
  background:
    radial-gradient(circle at 10% 10%, rgba(59,130,246,.15), transparent 45%),
    radial-gradient(circle at 90% 90%, rgba(251,191,36,.08), transparent 50%),
    linear-gradient(160deg, #0a1a3a 0%, #0d2350 55%, #0a1a3a 100%);
  background-attachment: fixed;
  min-height: 100vh;
  color: var(--bng-white);
}
.stApp::before {
  content:'';
  position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(rgba(96,165,250,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(96,165,250,.04) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 85%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 85%);
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }

.block-container {
  padding-top: 1rem !important;
  padding-bottom: 3rem;
  max-width: 1400px;
  position: relative; z-index: 1;
}

/* ============ TYPOGRAPHY ============ */
h1, h2, h3 { letter-spacing: -.03em; font-weight: 800; color: #fff; }
p, li { color: #d1dce8; }
label { color: #cbd5e1 !important; }

/* ============ NAVBAR CUSTOM ============ */
.bng-navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 24px;
  background: linear-gradient(90deg, rgba(10,26,58,.95), rgba(13,35,80,.9));
  border-radius: 20px;
  border: 1px solid rgba(96,165,250,.25);
  backdrop-filter: blur(14px);
  box-shadow: 0 10px 40px rgba(0,0,0,.35);
  margin-bottom: 22px;
}
.bng-logo {
  display: flex; align-items: center; gap: 14px;
}
.bng-logo-badge {
  width: 52px; height: 52px; border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #ffffff, #dbeafe 60%, #93c5fd);
  display: flex; align-items: center; justify-content: center;
  font-size: 30px;
  box-shadow: 0 0 0 3px rgba(251,191,36,.35), 0 8px 20px rgba(0,0,0,.4);
  position: relative;
}
.bng-logo-badge::after {
  content: '👑'; position: absolute; top: -12px; font-size: 16px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,.4));
}
.bng-logo-text { display: flex; flex-direction: column; line-height: 1.05; }
.bng-logo-title {
  font-weight: 900; font-size: 22px; letter-spacing: .02em; color: #ffffff;
  font-family: 'Orbitron', sans-serif;
}
.bng-logo-sub {
  font-weight: 800; font-size: 12px; letter-spacing: .32em;
  color: var(--bng-yellow); text-transform: uppercase;
}
.bng-slogan {
  text-align: right; font-style: italic;
  font-family: 'Orbitron', sans-serif;
  font-size: 14px; font-weight: 700;
  color: var(--bng-yellow);
  line-height: 1.1;
  text-shadow: 0 2px 8px rgba(251,191,36,.4);
}
.bng-slogan small {
  display: block; font-size: 9px; letter-spacing: .3em;
  color: #cbd5e1; margin-top: 4px; font-style: normal;
}

/* ============ HERO BANNER ============ */
.bng-hero {
  position: relative; overflow: hidden;
  border-radius: 26px;
  padding: 46px 50px;
  margin-bottom: 26px;
  min-height: 380px;
  border: 1px solid rgba(96,165,250,.3);
  background:
    linear-gradient(120deg, rgba(10,26,58,.92) 0%, rgba(13,35,80,.7) 60%, rgba(30,58,138,.5) 100%);
  box-shadow: 0 24px 60px rgba(0,0,0,.45);
}
.bng-hero-img {
  position: absolute; inset: 0;
  background-size: cover; background-position: center right;
  opacity: .35;
  z-index: 0;
}
.bng-hero-content {
  position: relative; z-index: 2;
  max-width: 580px;
}
.bng-hero-kicker {
  display: inline-block;
  padding: 6px 16px;
  background: var(--bng-yellow);
  color: var(--bng-navy);
  font-weight: 900; font-size: 13px;
  font-style: italic;
  letter-spacing: .04em;
  transform: rotate(-2deg);
  border-radius: 4px;
  margin-bottom: 18px;
  box-shadow: 0 4px 14px rgba(251,191,36,.35);
}
.bng-hero h1 {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(2.2rem, 4.5vw, 3.6rem);
  font-weight: 900;
  line-height: 1.02;
  color: #fff;
  margin: 0 0 16px 0;
  text-shadow: 0 6px 24px rgba(0,0,0,.5);
  letter-spacing: -.02em;
}
.bng-hero h1 .hl {
  color: var(--bng-yellow);
  display: block;
}
.bng-hero-quote {
  font-style: italic;
  font-size: 1.05rem;
  color: #e0ecf8;
  border-left: 4px solid var(--bng-yellow);
  padding-left: 14px;
  margin: 16px 0;
  line-height: 1.5;
}
.bng-hero-sub {
  font-size: .88rem;
  color: #b8c8dd;
  margin-top: 12px;
}
.bng-hero-tag {
  position: absolute; right: 40px; top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  text-align: center;
  font-family: 'Orbitron', sans-serif;
}
.bng-hero-tag .t1, .bng-hero-tag .t2, .bng-hero-tag .t3 {
  display: block;
  font-style: italic;
  font-weight: 900;
  color: var(--bng-yellow);
  line-height: 1.1;
  text-shadow: 0 4px 16px rgba(0,0,0,.6);
}
.bng-hero-tag .t1 { font-size: 42px; }
.bng-hero-tag .t2 { font-size: 42px; }
.bng-hero-tag .t3 { font-size: 42px; }

/* ============ SECTION TITLE ============ */
.bng-section {
  display: flex; align-items: center; gap: 12px;
  margin: 28px 0 16px 0;
}
.bng-section .icon { font-size: 24px; }
.bng-section h2 {
  margin: 0; font-size: 1.3rem; font-weight: 800;
  color: #fff;
}
.bng-section .sub {
  color: var(--bng-text-dim); font-size: .85rem;
  margin-top: 2px;
}

/* ============ STAT CARDS ============ */
.bng-stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
.bng-stat-card {
  background: var(--bng-glass);
  border: 1px solid var(--bng-glass-border);
  border-radius: 18px;
  padding: 20px 18px;
  backdrop-filter: blur(12px);
  transition: transform .2s, border-color .2s, box-shadow .2s;
  position: relative;
  overflow: hidden;
}
.bng-stat-card::before {
  content:''; position: absolute; top: 0; left: 0;
  width: 100%; height: 3px;
  background: linear-gradient(90deg, var(--bng-cyan), var(--bng-blue-light));
  opacity: .8;
}
.bng-stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(251,191,36,.5);
  box-shadow: 0 14px 34px rgba(251,191,36,.15);
}
.bng-stat-icon {
  font-size: 28px; margin-bottom: 10px; display: inline-block;
}
.bng-stat-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 34px; font-weight: 900;
  color: var(--bng-yellow);
  line-height: 1;
  margin: 6px 0 4px 0;
}
.bng-stat-label {
  font-size: .82rem; color: #cbd5e1;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .05em;
}

/* ============ ATTRIBUTE BARS ============ */
.bng-attr-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  margin-top: 10px;
}
.bng-attr-card {
  background: var(--bng-glass);
  border: 1px solid var(--bng-glass-border);
  border-radius: 14px;
  padding: 14px;
  text-align: center;
  backdrop-filter: blur(12px);
}
.bng-attr-icon { font-size: 22px; margin-bottom: 6px; display: inline-block; }
.bng-attr-name {
  font-size: .78rem; font-weight: 700;
  color: #cbd5e1; margin-bottom: 6px;
  text-transform: uppercase; letter-spacing: .04em;
}
.bng-attr-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 22px; font-weight: 900;
  color: #fff;
  margin-bottom: 8px;
}
.bng-attr-bar {
  height: 5px; border-radius: 3px;
  background: rgba(255,255,255,.08);
  overflow: hidden;
}
.bng-attr-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width .8s cubic-bezier(.2,.8,.2,1);
}

/* ============ MORE THAN JUST A GAME ============ */
.bng-more-box {
  background:
    radial-gradient(circle at 100% 0%, rgba(251,191,36,.15), transparent 55%),
    linear-gradient(135deg, rgba(13,35,80,.85), rgba(10,26,58,.9));
  border: 1px solid rgba(251,191,36,.35);
  border-radius: 22px;
  padding: 26px 24px;
  backdrop-filter: blur(14px);
  position: relative;
  overflow: hidden;
}
.bng-more-title {
  font-family: 'Orbitron', sans-serif;
  font-style: italic;
  font-size: 24px; font-weight: 900;
  color: var(--bng-yellow);
  line-height: 1.1;
  margin-bottom: 20px;
  text-shadow: 0 4px 14px rgba(251,191,36,.3);
}
.bng-more-title small {
  display: block; font-size: 12px; font-style: normal;
  letter-spacing: .3em; color: #cbd5e1;
  margin-top: 6px;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
}
.bng-more-item {
  display: flex; align-items: flex-start; gap: 14px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(96,165,250,.15);
}
.bng-more-item:last-child { border-bottom: none; }
.bng-more-item .icon {
  width: 40px; height: 40px; border-radius: 50%;
  background: rgba(251,191,36,.15);
  border: 1px solid rgba(251,191,36,.4);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
}
.bng-more-item .txt strong {
  display: block; color: #fff; font-size: .95rem;
  font-weight: 700; margin-bottom: 2px;
}
.bng-more-item .txt span {
  color: #94a3b8; font-size: .8rem;
}
.bng-more-tag {
  margin-top: 18px;
  display: inline-block;
  padding: 8px 18px;
  background: linear-gradient(90deg, var(--bng-yellow-dark), var(--bng-yellow));
  color: var(--bng-navy);
  font-family: 'Orbitron', sans-serif;
  font-weight: 900; font-size: 13px;
  letter-spacing: .08em;
  border-radius: 6px;
  transform: skewX(-8deg);
  box-shadow: 0 4px 14px rgba(251,191,36,.4);
}
.bng-more-tag span { display: inline-block; transform: skewX(8deg); }

/* ============ PLAYER CARD ============ */
.bng-player-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 14px;
}
.bng-player-card {
  background: var(--bng-glass);
  border: 1px solid var(--bng-glass-border);
  border-radius: 16px;
  padding: 14px;
  backdrop-filter: blur(12px);
  display: flex; gap: 12px; align-items: center;
  transition: transform .22s cubic-bezier(.2,.8,.2,1), border-color .22s, box-shadow .22s;
  position: relative;
  overflow: hidden;
}
.bng-player-card::before {
  content:''; position: absolute; left: 0; top: 0;
  width: 3px; height: 100%;
  background: linear-gradient(180deg, var(--bng-yellow), var(--bng-yellow-dark));
  opacity: 0; transition: opacity .2s;
}
.bng-player-card:hover {
  transform: translateY(-4px);
  border-color: rgba(251,191,36,.6);
  box-shadow: 0 14px 34px rgba(251,191,36,.15);
}
.bng-player-card:hover::before { opacity: 1; }

.bng-avatar {
  width: 56px; height: 56px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 18px;
  color: #fff;
  flex-shrink: 0;
  border: 2px solid rgba(255,255,255,.2);
  box-shadow: 0 4px 12px rgba(0,0,0,.3);
  overflow: hidden;
  position: relative;
}
.bng-avatar img { width: 100%; height: 100%; object-fit: cover; }

.bng-player-info { min-width: 0; flex: 1; }
.bng-player-name {
  font-weight: 700; color: #fff;
  font-size: .95rem; line-height: 1.2;
  margin-bottom: 3px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.bng-player-alias {
  font-size: .72rem; color: var(--bng-text-dim);
  margin-bottom: 6px;
}
.bng-player-roles { display: flex; gap: 4px; flex-wrap: wrap; }
.bng-role-chip {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 10px; font-weight: 800;
  letter-spacing: .04em;
  background: rgba(59,130,246,.25);
  border: 1px solid rgba(96,165,250,.5);
  color: #d6ecff;
}
.bng-role-chip.gk { background: rgba(251,191,36,.2); border-color: rgba(251,191,36,.5); color: #fde68a; }
.bng-role-chip.a  { background: rgba(59,130,246,.25); border-color: rgba(96,165,250,.5); color: #bfdbfe; }
.bng-role-chip.f  { background: rgba(34,197,94,.2); border-color: rgba(34,197,94,.5); color: #bbf7d0; }
.bng-role-chip.p  { background: rgba(239,68,68,.2); border-color: rgba(239,68,68,.5); color: #fecaca; }

.bng-ovr-badge {
  position: absolute; top: 10px; right: 10px;
  background: linear-gradient(135deg, var(--bng-yellow-dark), var(--bng-yellow));
  color: var(--bng-navy);
  font-family: 'Orbitron', sans-serif;
  font-weight: 900; font-size: 13px;
  padding: 3px 9px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(251,191,36,.4);
}

/* ============ BUTTONS ============ */
.stButton > button {
  border: 1px solid rgba(251,191,36,.4) !important;
  border-radius: 12px !important;
  font-weight: 800 !important;
  letter-spacing: .02em;
  background: linear-gradient(110deg, var(--bng-yellow-dark), var(--bng-yellow)) !important;
  color: var(--bng-navy) !important;
  text-shadow: none;
  box-shadow: 0 6px 18px rgba(251,191,36,.3) !important;
  transition: transform .16s, filter .16s, box-shadow .16s !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  filter: brightness(1.1) !important;
  box-shadow: 0 10px 24px rgba(251,191,36,.5) !important;
}
.stButton > button * { color: var(--bng-navy) !important; font-weight: 800 !important; }

.stButton > button[kind="secondary"] {
  background: linear-gradient(110deg, rgba(30,58,138,.8), rgba(59,130,246,.8)) !important;
  color: #fff !important;
  border-color: rgba(96,165,250,.6) !important;
}
.stButton > button[kind="secondary"] * { color: #fff !important; }

/* ============ FORM INPUTS ============ */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div,
[data-baseweb="textarea"] > div {
  background: rgba(10,26,58,.85) !important;
  border-color: rgba(96,165,250,.3) !important;
  border-radius: 10px !important;
  color: #fff !important;
}
[data-baseweb="input"] input,
[data-baseweb="select"] span,
[data-baseweb="textarea"] textarea { color: #fff !important; }

[data-baseweb="tag"] {
  background: linear-gradient(110deg, var(--bng-yellow-dark), var(--bng-yellow)) !important;
  color: var(--bng-navy) !important;
  font-weight: 700 !important;
  border-radius: 6px !important;
}
[data-baseweb="tag"] * { color: var(--bng-navy) !important; }

/* ============ TABS ============ */
[data-baseweb="tab-list"] {
  background: rgba(10,26,58,.5);
  border-radius: 12px;
  padding: 5px;
  border: 1px solid rgba(96,165,250,.2);
}
[data-baseweb="tab"] {
  font-weight: 700 !important;
  border-radius: 8px !important;
  color: #94a3b8 !important;
  padding: 8px 18px !important;
}
[data-baseweb="tab"][aria-selected="true"] {
  background: linear-gradient(110deg, var(--bng-yellow-dark), var(--bng-yellow)) !important;
  color: var(--bng-navy) !important;
}
[data-baseweb="tab"][aria-selected="true"] * { color: var(--bng-navy) !important; }

/* ============ METRIC ============ */
[data-testid="stMetric"] {
  background: var(--bng-glass);
  border: 1px solid var(--bng-glass-border);
  border-radius: 14px;
  padding: 14px 18px;
  backdrop-filter: blur(12px);
}
[data-testid="stMetricValue"] {
  color: var(--bng-yellow) !important;
  font-family: 'Orbitron', sans-serif !important;
  font-weight: 900 !important;
}
[data-testid="stMetricLabel"] { color: #cbd5e1 !important; }

/* ============ PLACEHOLDER / EMPTY ============ */
.bng-placeholder {
  text-align: center;
  padding: 60px 30px;
  border-radius: 22px;
  background: var(--bng-glass);
  border: 2px dashed rgba(96,165,250,.3);
  backdrop-filter: blur(12px);
  margin: 16px 0;
}
.bng-placeholder .emoji {
  font-size: 64px;
  margin-bottom: 16px;
  filter: drop-shadow(0 6px 20px rgba(251,191,36,.3));
}
.bng-placeholder h3 {
  color: var(--bng-yellow);
  margin: 0 0 8px 0;
}
.bng-placeholder p {
  color: #94a3b8; margin: 0;
}

/* ============ FOOTER ============ */
.bng-footer {
  margin-top: 40px;
  padding: 24px;
  border-radius: 18px;
  background: var(--bng-glass);
  border: 1px solid var(--bng-glass-border);
  text-align: center;
  backdrop-filter: blur(12px);
}
.bng-footer .brand {
  font-family: 'Orbitron', sans-serif;
  font-weight: 900;
  background: linear-gradient(110deg, var(--bng-yellow), #fde68a);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: .06em;
}
.bng-footer small { color: #64748b; }

/* ============ ANIMATIONS ============ */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
.bng-animate { animation: fadeInUp .5s cubic-bezier(.2,.8,.2,1) both; }

/* ============ RESPONSIVE ============ */
@media (max-width: 900px) {
  .bng-stat-grid { grid-template-columns: repeat(2, 1fr); }
  .bng-attr-grid { grid-template-columns: repeat(3, 1fr); }
  .bng-hero-tag { display: none; }
  .bng-hero { padding: 30px 24px; }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# PATH & KONSTANTA
# ==========================================
BASE_DIR = Path(__file__).parent.resolve()
PLAYERS_DB = BASE_DIR / "players_db.json"
MATCH_HISTORY = BASE_DIR / "match_history.json"
AVATARS_DIR = BASE_DIR / "assets" / "avatars"
HERO_IMG = BASE_DIR / "assets" / "hero.png"

ROLE_INFO = {
    "GK": {"nama": "Kiper",   "emoji": "🧤", "color": "#fbbf24", "css": "gk"},
    "A":  {"nama": "Anchor",  "emoji": "⚓", "color": "#3b82f6", "css": "a"},
    "F":  {"nama": "Flank",   "emoji": "🪽", "color": "#22c55e", "css": "f"},
    "P":  {"nama": "Pivot",   "emoji": "🔥", "color": "#ef4444", "css": "p"},
}
ROLE_KEYS = ["GK", "A", "F", "P"]

PHY_COLS = ["STA", "AKS", "SPR", "AGI", "BAL", "STR"]
TEC_COLS = ["CON", "DRI", "PAS", "SHA", "SHP", "TAC"]
MTC_COLS = ["VIS", "OFB", "COM", "AGR", "TMW"]
GKS_COLS = ["DEC", "REF", "POS", "THR", "KIC", "BRV"]
ALL_ATTRS = PHY_COLS + TEC_COLS + MTC_COLS + GKS_COLS

AVATAR_COLORS = [
    "#3b82f6", "#22c55e", "#ef4444", "#a855f7",
    "#f59e0b", "#06b6d4", "#ec4899", "#6366f1",
]

MAX_LOGIN_ATTEMPTS = 5
DEFAULT_ADMIN_PASSWORD = "BIAFUTSAL"

# ==========================================
# SEED DATA (dari Excel — 23 pemain)
# ==========================================
SEED_PLAYERS = [
    {"id": "P001", "nama": "Ade Suryadana",      "alias": "Ade",     "overall": 100, "positions": ["F", "GK", "P", "A"], "attributes": {"STA": 97, "AKS": 99, "SPR": 98, "AGI": 99, "BAL": 94, "STR": 96, "CON": 95, "DRI": 98, "PAS": 94, "SHA": 99, "SHP": 99, "TAC": 88, "VIS": 90, "OFB": 93, "COM": 91, "AGR": 94, "TMW": 92, "DEC": 78, "REF": 76, "POS": 77, "THR": 74, "KIC": 76, "BRV": 79}},
    {"id": "P002", "nama": "Aldo S.",            "alias": "Aldo",    "overall": 95,  "positions": ["A", "P", "GK", "F"], "attributes": {"STA": 92, "AKS": 90, "SPR": 88, "AGI": 94, "BAL": 96, "STR": 93, "CON": 91, "DRI": 93, "PAS": 95, "SHA": 89, "SHP": 90, "TAC": 97, "VIS": 96, "OFB": 95, "COM": 94, "AGR": 92, "TMW": 93, "DEC": 85, "REF": 82, "POS": 84, "THR": 80, "KIC": 83, "BRV": 86}},
    {"id": "P003", "nama": "Aprizqi R",          "alias": "AP",      "overall": 95,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 92, "AKS": 90, "SPR": 88, "AGI": 94, "BAL": 96, "STR": 93, "CON": 91, "DRI": 93, "PAS": 95, "SHA": 89, "SHP": 90, "TAC": 97, "VIS": 96, "OFB": 95, "COM": 94, "AGR": 92, "TMW": 93, "DEC": 85, "REF": 82, "POS": 84, "THR": 80, "KIC": 83, "BRV": 86}},
    {"id": "P004", "nama": "Arby R",             "alias": "Byrus",   "overall": 100, "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 97, "AKS": 95, "SPR": 93, "AGI": 99, "BAL": 99, "STR": 98, "CON": 96, "DRI": 98, "PAS": 99, "SHA": 94, "SHP": 95, "TAC": 99, "VIS": 99, "OFB": 99, "COM": 98, "AGR": 97, "TMW": 98, "DEC": 90, "REF": 87, "POS": 89, "THR": 85, "KIC": 88, "BRV": 91}},
    {"id": "P005", "nama": "Fadhli D. Ikram",    "alias": "Dzil",    "overall": 95,  "positions": ["A", "P", "GK", "F"], "attributes": {"STA": 92, "AKS": 90, "SPR": 88, "AGI": 94, "BAL": 96, "STR": 93, "CON": 91, "DRI": 93, "PAS": 95, "SHA": 89, "SHP": 90, "TAC": 97, "VIS": 96, "OFB": 95, "COM": 94, "AGR": 92, "TMW": 93, "DEC": 85, "REF": 82, "POS": 84, "THR": 80, "KIC": 83, "BRV": 86}},
    {"id": "P006", "nama": "Farhan I. A.",       "alias": "Han",     "overall": 70,  "positions": ["P", "A", "F", "GK"], "attributes": {"STA": 75, "AKS": 73, "SPR": 70, "AGI": 74, "BAL": 78, "STR": 76, "CON": 74, "DRI": 76, "PAS": 73, "SHA": 79, "SHP": 80, "TAC": 71, "VIS": 72, "OFB": 74, "COM": 72, "AGR": 75, "TMW": 73, "DEC": 64, "REF": 62, "POS": 63, "THR": 60, "KIC": 62, "BRV": 65}},
    {"id": "P007", "nama": "Geraldo H.",         "alias": "Geraldo", "overall": 80,  "positions": ["A", "GK", "P", "F"], "attributes": {"STA": 82, "AKS": 80, "SPR": 78, "AGI": 84, "BAL": 86, "STR": 83, "CON": 81, "DRI": 83, "PAS": 85, "SHA": 79, "SHP": 80, "TAC": 87, "VIS": 86, "OFB": 85, "COM": 84, "AGR": 82, "TMW": 83, "DEC": 75, "REF": 72, "POS": 74, "THR": 70, "KIC": 73, "BRV": 76}},
    {"id": "P008", "nama": "Hanz Seca",          "alias": "Hanz",    "overall": 60,  "positions": ["GK", "A", "P", "F"], "attributes": {"STA": 61, "AKS": 59, "SPR": 57, "AGI": 60, "BAL": 62, "STR": 63, "CON": 58, "DRI": 60, "PAS": 58, "SHA": 56, "SHP": 57, "TAC": 62, "VIS": 65, "OFB": 68, "COM": 67, "AGR": 66, "TMW": 68, "DEC": 70, "REF": 72, "POS": 71, "THR": 69, "KIC": 70, "BRV": 73}},
    {"id": "P009", "nama": "Ibrahim",            "alias": "Bacing",  "overall": 90,  "positions": ["F", "P", "A", "GK"], "attributes": {"STA": 88, "AKS": 85, "SPR": 92, "AGI": 87, "BAL": 89, "STR": 86, "CON": 85, "DRI": 88, "PAS": 84, "SHA": 90, "SHP": 91, "TAC": 82, "VIS": 84, "OFB": 86, "COM": 83, "AGR": 87, "TMW": 85, "DEC": 72, "REF": 70, "POS": 71, "THR": 68, "KIC": 70, "BRV": 73}},
    {"id": "P010", "nama": "Jehua Kusuma Dewa",  "alias": "Jeje",    "overall": 70,  "positions": ["A", "F", "P", "GK"], "attributes": {"STA": 72, "AKS": 70, "SPR": 68, "AGI": 74, "BAL": 76, "STR": 73, "CON": 71, "DRI": 73, "PAS": 75, "SHA": 69, "SHP": 70, "TAC": 77, "VIS": 76, "OFB": 75, "COM": 74, "AGR": 72, "TMW": 73, "DEC": 65, "REF": 62, "POS": 64, "THR": 60, "KIC": 63, "BRV": 66}},
    {"id": "P011", "nama": "M. Ardhana W. N.",   "alias": "Ardha",   "overall": 60,  "positions": ["GK", "A", "P", "F"], "attributes": {"STA": 61, "AKS": 59, "SPR": 57, "AGI": 60, "BAL": 62, "STR": 63, "CON": 58, "DRI": 60, "PAS": 58, "SHA": 56, "SHP": 57, "TAC": 62, "VIS": 65, "OFB": 68, "COM": 67, "AGR": 66, "TMW": 68, "DEC": 70, "REF": 72, "POS": 71, "THR": 69, "KIC": 70, "BRV": 73}},
    {"id": "P012", "nama": "M. Daffa A.",        "alias": "Daffa",   "overall": 95,  "positions": ["F", "A", "P", "GK"], "attributes": {"STA": 94, "AKS": 92, "SPR": 96, "AGI": 92, "BAL": 94, "STR": 91, "CON": 90, "DRI": 93, "PAS": 89, "SHA": 95, "SHP": 96, "TAC": 87, "VIS": 88, "OFB": 90, "COM": 88, "AGR": 91, "TMW": 89, "DEC": 72, "REF": 70, "POS": 71, "THR": 68, "KIC": 70, "BRV": 73}},
    {"id": "P013", "nama": "M. Zidan G.",        "alias": "Zidan",   "overall": 100, "positions": ["F", "P", "A", "GK"], "attributes": {"STA": 97, "AKS": 95, "SPR": 98, "AGI": 99, "BAL": 97, "STR": 99, "CON": 96, "DRI": 98, "PAS": 95, "SHA": 99, "SHP": 99, "TAC": 89, "VIS": 90, "OFB": 92, "COM": 90, "AGR": 93, "TMW": 91, "DEC": 74, "REF": 72, "POS": 73, "THR": 70, "KIC": 72, "BRV": 75}},
    {"id": "P014", "nama": "Mahardhyka P.",      "alias": "Dhyka",   "overall": 90,  "positions": ["P", "F", "A", "GK"], "attributes": {"STA": 92, "AKS": 90, "SPR": 88, "AGI": 89, "BAL": 94, "STR": 91, "CON": 90, "DRI": 92, "PAS": 94, "SHA": 88, "SHP": 89, "TAC": 96, "VIS": 95, "OFB": 94, "COM": 93, "AGR": 91, "TMW": 92, "DEC": 72, "REF": 70, "POS": 71, "THR": 68, "KIC": 70, "BRV": 73}},
    {"id": "P015", "nama": "Martin Koko",        "alias": "Martin",  "overall": 90,  "positions": ["A", "GK", "P", "F"], "attributes": {"STA": 88, "AKS": 85, "SPR": 82, "AGI": 89, "BAL": 91, "STR": 88, "CON": 86, "DRI": 88, "PAS": 90, "SHA": 84, "SHP": 85, "TAC": 92, "VIS": 91, "OFB": 90, "COM": 89, "AGR": 87, "TMW": 88, "DEC": 80, "REF": 77, "POS": 79, "THR": 75, "KIC": 78, "BRV": 81}},
    {"id": "P016", "nama": "Musyaffa C. M.",     "alias": "Mus",     "overall": 75,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 77, "AKS": 75, "SPR": 73, "AGI": 79, "BAL": 81, "STR": 78, "CON": 76, "DRI": 78, "PAS": 80, "SHA": 74, "SHP": 75, "TAC": 82, "VIS": 81, "OFB": 80, "COM": 79, "AGR": 77, "TMW": 78, "DEC": 70, "REF": 67, "POS": 69, "THR": 65, "KIC": 68, "BRV": 71}},
    {"id": "P017", "nama": "Naufal Y.",          "alias": "Naufal",  "overall": 70,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 72, "AKS": 70, "SPR": 68, "AGI": 74, "BAL": 76, "STR": 73, "CON": 71, "DRI": 73, "PAS": 75, "SHA": 69, "SHP": 70, "TAC": 77, "VIS": 76, "OFB": 75, "COM": 74, "AGR": 72, "TMW": 73, "DEC": 65, "REF": 62, "POS": 64, "THR": 60, "KIC": 63, "BRV": 66}},
    {"id": "P018", "nama": "Nur Sahrul",         "alias": "Aloenk",  "overall": 95,  "positions": ["F", "P", "A", "GK"], "attributes": {"STA": 94, "AKS": 92, "SPR": 96, "AGI": 92, "BAL": 94, "STR": 91, "CON": 90, "DRI": 93, "PAS": 89, "SHA": 95, "SHP": 96, "TAC": 87, "VIS": 88, "OFB": 90, "COM": 88, "AGR": 91, "TMW": 89, "DEC": 72, "REF": 70, "POS": 71, "THR": 68, "KIC": 70, "BRV": 73}},
    {"id": "P019", "nama": "R. Hafis M.",        "alias": "Fis",     "overall": 90,  "positions": ["F", "GK", "A", "P"], "attributes": {"STA": 88, "AKS": 85, "SPR": 92, "AGI": 87, "BAL": 89, "STR": 86, "CON": 85, "DRI": 88, "PAS": 84, "SHA": 90, "SHP": 91, "TAC": 82, "VIS": 84, "OFB": 86, "COM": 83, "AGR": 87, "TMW": 85, "DEC": 78, "REF": 80, "POS": 79, "THR": 77, "KIC": 78, "BRV": 81}},
    {"id": "P020", "nama": "Rafi M. A.",         "alias": "Rafi",    "overall": 80,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 82, "AKS": 80, "SPR": 78, "AGI": 84, "BAL": 86, "STR": 83, "CON": 81, "DRI": 83, "PAS": 85, "SHA": 79, "SHP": 80, "TAC": 87, "VIS": 86, "OFB": 85, "COM": 84, "AGR": 82, "TMW": 83, "DEC": 75, "REF": 72, "POS": 74, "THR": 70, "KIC": 73, "BRV": 76}},
    {"id": "P021", "nama": "Rafif Kusuma",       "alias": "RaKus",   "overall": 70,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 72, "AKS": 70, "SPR": 68, "AGI": 74, "BAL": 76, "STR": 73, "CON": 71, "DRI": 73, "PAS": 75, "SHA": 69, "SHP": 70, "TAC": 77, "VIS": 76, "OFB": 75, "COM": 74, "AGR": 72, "TMW": 73, "DEC": 65, "REF": 62, "POS": 64, "THR": 60, "KIC": 63, "BRV": 66}},
    {"id": "P022", "nama": "Teguh A. R.",        "alias": "PapiKai", "overall": 80,  "positions": ["GK", "A", "P", "F"], "attributes": {"STA": 82, "AKS": 80, "SPR": 78, "AGI": 84, "BAL": 86, "STR": 83, "CON": 81, "DRI": 83, "PAS": 85, "SHA": 79, "SHP": 80, "TAC": 87, "VIS": 86, "OFB": 85, "COM": 84, "AGR": 82, "TMW": 83, "DEC": 78, "REF": 80, "POS": 79, "THR": 77, "KIC": 78, "BRV": 81}},
    {"id": "P023", "nama": "Yadhit P.",          "alias": "Yadhit",  "overall": 75,  "positions": ["A", "GK", "P", "F"], "attributes": {"STA": 77, "AKS": 75, "SPR": 73, "AGI": 79, "BAL": 81, "STR": 78, "CON": 76, "DRI": 78, "PAS": 80, "SHA": 74, "SHP": 75, "TAC": 82, "VIS": 81, "OFB": 80, "COM": 79, "AGR": 77, "TMW": 78, "DEC": 73, "REF": 75, "POS": 74, "THR": 72, "KIC": 73, "BRV": 76}},
]


def seed_players():
    """Konversi SEED_PLAYERS ke format database (roles + photo_url)."""
    result = []
    for p in SEED_PLAYERS:
        roles = list(dict.fromkeys(p["positions"]))  # unique, urut
        result.append({
            "id": p["id"],
            "nama": p["nama"],
            "alias": p["alias"],
            "overall": p["overall"],
            "roles": roles,
            "main_position": p["positions"][0],
            "positions": {
                "1st": p["positions"][0],
                "2nd": p["positions"][1],
                "3rd": p["positions"][2],
                "4th": p["positions"][3],
            },
            "attributes": p["attributes"],
            "photo_url": "",   # kosong dulu, nanti bisa diisi Google Drive URL
        })
    return result


# ==========================================
# DATA STORE ABSTRACTION LAYER
# (Fase 4: cukup ganti JSONStore() → GoogleSheetsStore())
# ==========================================
class JSONStore:
    """Implementasi penyimpanan berbasis file JSON lokal."""

    def __init__(self, players_path: Path, match_path: Path):
        self.players_path = players_path
        self.match_path = match_path

    # ---------- PLAYERS ----------
    def get_players(self) -> list:
        if not self.players_path.exists():
            data = seed_players()
            self._write_json(self.players_path, data)
            return data
        try:
            with open(self.players_path, encoding="utf-8") as f:
                data = json.load(f)
            if not data:
                data = seed_players()
                self._write_json(self.players_path, data)
            return data
        except (OSError, ValueError):
            data = seed_players()
            self._write_json(self.players_path, data)
            return data

    def save_players(self, players: list) -> bool:
        return self._write_json(self.players_path, players)

    # ---------- MATCH HISTORY ----------
    def get_match_history(self) -> list:
        if not self.match_path.exists():
            self._write_json(self.match_path, [])
            return []
        try:
            with open(self.match_path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return []

    def save_match_history(self, matches: list) -> bool:
        return self._write_json(self.match_path, matches)

    # ---------- INTERNAL ----------
    @staticmethod
    def _write_json(path: Path, data) -> bool:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False


# Inisialisasi store (nanti tinggal ganti ke GoogleSheetsStore)
store = JSONStore(PLAYERS_DB, MATCH_HISTORY)


# ==========================================
# UTILITAS
# ==========================================
def get_admin_password() -> str:
    try:
        pw = st.secrets.get("ADMIN_PASSWORD")
    except Exception:
        pw = None
    return str(pw) if pw else os.environ.get("ADMIN_PASSWORD") or DEFAULT_ADMIN_PASSWORD


def initials(name: str) -> str:
    words = [w.strip(".") for w in name.replace("-", " ").split() if w.strip(".")]
    if not words:
        return "?"
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[1][0]).upper()


def color_for(name: str) -> str:
    return AVATAR_COLORS[sum(ord(c) for c in name) % len(AVATAR_COLORS)]


def avatar_img_base64(path: Path) -> str | None:
    """Convert file gambar ke base64 data URI. Return None jika tidak ada."""
    try:
        if not path.exists():
            return None
        with open(path, "rb") as f:
            data = f.read()
        ext = path.suffix.lower().lstrip(".")
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "gif": "image/gif", "webp": "image/webp"}.get(ext, "image/png")
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    except Exception:
        return None


def resolve_avatar(player: dict, size: int = 56) -> str:
    """
    Resolusi avatar 3-tier:
    1. File lokal: assets/avatars/{id}.png
    2. URL: player['photo_url']
    3. Fallback: inisial warna
    """
    pid = player.get("id", "")
    # 1) File lokal
    for ext in ("png", "jpg", "jpeg", "webp"):
        img_path = AVATARS_DIR / f"{pid}.{ext}"
        b64 = avatar_img_base64(img_path)
        if b64:
            return f"<div class='bng-avatar' style='background:{color_for(player['nama'])}'><img src='{b64}' alt='{esc(player['nama'])}'></div>"
    # 2) URL
    url = (player.get("photo_url") or "").strip()
    if url:
        return f"<div class='bng-avatar' style='background:{color_for(player['nama'])}'><img src='{esc(url)}' alt='{esc(player['nama'])}' onerror=\"this.style.display='none'\"></div>"
    # 3) Inisial
    c = color_for(player["nama"])
    ini = esc(initials(player["nama"]))
    return f"<div class='bng-avatar' style='background:{c}'>{ini}</div>"


def role_chip_html(role: str) -> str:
    info = ROLE_INFO.get(role, {})
    css = info.get("css", "")
    return f"<span class='bng-role-chip {css}'>{role}</span>"


def hero_background_css() -> str:
    """Kalau ada hero.png, pakai sebagai background. Kalau tidak, gradient default."""
    b64 = avatar_img_base64(HERO_IMG)
    if b64:
        return f"background-image: url('{b64}');"
    return ""


# ==========================================
# SESSION STATE
# ==========================================
_defaults = {
    "page": "Home",
    "is_admin": False,
    "login_open": False,
    "login_attempts": 0,
    "players_cache": None,
    "edit_player_id": None,
    "show_add_player": False,
    "flash": None,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def load_players(force: bool = False) -> list:
    if st.session_state.players_cache is None or force:
        st.session_state.players_cache = store.get_players()
    return st.session_state.players_cache


def refresh_players():
    st.session_state.players_cache = store.get_players()


# ==========================================
# CALLBACKS
# ==========================================
def do_login():
    pw = st.session_state.get("login_pw", "")
    if pw == get_admin_password():
        st.session_state.is_admin = True
        st.session_state.login_attempts = 0
        st.session_state.login_open = False
        st.session_state.flash = ("success", "✅ Login berhasil. Mode admin aktif.")
    else:
        st.session_state.login_attempts += 1
        left = MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts
        if left <= 0:
            st.session_state.flash = ("error", "⛔ Terlalu banyak percobaan salah.")
            st.session_state.login_open = False
        else:
            st.session_state.flash = ("error", f"❌ Password salah. Sisa: {left}")


def do_logout():
    st.session_state.is_admin = False
    st.session_state.edit_player_id = None
    st.session_state.show_add_player = False
    st.session_state.flash = ("info", "🔒 Logout. Mode admin nonaktif.")


# ==========================================
# UI COMPONENTS
# ==========================================
def render_navbar():
    nav = st.session_state.page
    nav_html = f"""
    <div class='bng-navbar bng-animate'>
      <div class='bng-logo'>
        <div class='bng-logo-badge'>⚽</div>
        <div class='bng-logo-text'>
          <div class='bng-logo-title'>BIAENERGI</div>
          <div class='bng-logo-sub'>Futsal Academy</div>
        </div>
      </div>
      <div class='bng-slogan'>
        "One Team<br>One Spirit"
        <small>✦ PLAY · LEARN · GROW ✦</small>
      </div>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

    # Navigasi pakai st.tabs (paling kompatibel)
    tabs = st.tabs(["🏠 Home", "👥 Team", "⚽ Team Generator", "📜 Match History", "ℹ️ About"])
    return tabs


def render_footer():
    st.markdown("""
    <div class='bng-footer bng-animate'>
      <div class='brand'>BIAENERGI FUTSAL ACADEMY</div>
      <p style='margin:8px 0 0 0;color:#94a3b8;font-size:.82rem'>
        Pantang menyerah meski skor tidak berpihak — <i>Never give up, even when the score isn't on our side.</i>
      </p>
      <small>© 2026 BIAENERGI Futsal Academy · v5.0</small>
    </div>
    """, unsafe_allow_html=True)


def render_hero():
    bg = hero_background_css()
    bg_div = f"<div class='bng-hero-img' style='{bg}'></div>" if bg else ""
    st.markdown(f"""
    <div class='bng-hero bng-animate'>
      {bg_div}
      <div class='bng-hero-content'>
        <div class='bng-hero-kicker'>Welcome to the</div>
        <h1>BIAENERGI<span class='hl'>Futsal Academy</span></h1>
        <div class='bng-hero-quote'>
          "Pantang menyerah meski skor tidak berpihak."
        </div>
        <div class='bng-hero-sub'>
          Never give up, even when the score isn't on our side.
        </div>
      </div>
      <div class='bng-hero-tag'>
        <span class='t1'>Play</span>
        <span class='t2'>Learn</span>
        <span class='t3'>Grow</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(icon: str, title: str, subtitle: str = ""):
    sub = f"<div class='sub'>{subtitle}</div>" if subtitle else ""
    st.markdown(f"""
    <div class='bng-section'>
      <span class='icon'>{icon}</span>
      <div>
        <h2>{title}</h2>
        {sub}
      </div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(icon: str, value, label: str):
    return f"""
    <div class='bng-stat-card'>
      <div class='bng-stat-icon'>{icon}</div>
      <div class='bng-stat-value'>{value}</div>
      <div class='bng-stat-label'>{label}</div>
    </div>
    """


def attribute_card(icon: str, name: str, value: float, color: str):
    pct = max(0, min(100, value))
    return f"""
    <div class='bng-attr-card'>
      <div class='bng-attr-icon'>{icon}</div>
      <div class='bng-attr-name'>{name}</div>
      <div class='bng-attr-value'>{int(round(value))}</div>
      <div class='bng-attr-bar'>
        <div class='bng-attr-bar-fill' style='width:{pct}%;background:{color}'></div>
      </div>
    </div>
    """


def player_card(player: dict) -> str:
    avatar = resolve_avatar(player, size=56)
    roles_html = "".join(role_chip_html(r) for r in player.get("roles", [])[:4])
    alias = player.get("alias", "")
    alias_html = f"<div class='bng-player-alias'>“{esc(alias)}”</div>" if alias else ""
    ovr = player.get("overall", 0)
    return f"""
    <div class='bng-player-card'>
      <div class='bng-ovr-badge'>{ovr}</div>
      {avatar}
      <div class='bng-player-info'>
        <div class='bng-player-name'>{esc(player['nama'])}</div>
        {alias_html}
        <div class='bng-player-roles'>{roles_html}</div>
      </div>
    </div>
    """


def placeholder_box(emoji: str, title: str, desc: str):
    st.markdown(f"""
    <div class='bng-placeholder bng-animate'>
      <div class='emoji'>{emoji}</div>
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGES
# ==========================================
def page_home():
    render_hero()

    players = load_players()
    total_players = len(players)
    total_roles = sum(len(p.get("roles", [])) for p in players)
    highest_ovr = max((p.get("overall", 0) for p in players), default=0)
    total_teams = 1  # nanti di-update dari match history

    # --- OUR TEAM AT A GLANCE ---
    section_header("👥", "Our Team at a Glance", "Statistik singkat tim BIAENERGI")
    stats = [
        stat_card("👥", total_players, "Total Players"),
        stat_card("🎯", "GK·A·F·P", "Player Positions"),
        stat_card("⭐", highest_ovr, "Highest Overall Rating"),
        stat_card("🤝", total_teams, "Team Together We Grow"),
    ]
    st.markdown(f"<div class='bng-stat-grid bng-animate'>{''.join(stats)}</div>",
                unsafe_allow_html=True)

    # --- PLAYER ATTRIBUTES (AVG) ---
    section_header("📊", "Player Attributes",
                   f"Average Team Stats — Berdasarkan {total_players} pemain")

    if players:
        # Hitung rata-rata per kategori
        def avg_of(cols):
            total = 0
            count = 0
            for p in players:
                for c in cols:
                    v = p.get("attributes", {}).get(c)
                    if isinstance(v, (int, float)):
                        total += v
                        count += 1
            return total / count if count else 0

        # Mapping kategori ke ikon + warna
        attr_groups = [
            ("Speed",     "🏃", ["STA", "AKS", "SPR", "AGI"], "#3b82f6"),
            ("Shooting",  "🎯", ["SHA", "SHP"],               "#ef4444"),
            ("Defense",   "🛡️", ["TAC", "STR", "BAL"],        "#22c55e"),
            ("Tactics",   "🧠", ["VIS", "OFB", "DEC"],        "#a855f7"),
            ("Teamwork",  "🤝", ["TMW", "COM"],               "#f59e0b"),
            ("Mood",      "😊", ["BRV", "AGR"],               "#fbbf24"),
        ]

        cards = []
        for name, icon, cols, color in attr_groups:
            avg = avg_of(cols)
            cards.append(attribute_card(icon, name, avg, color))

        st.markdown(f"<div class='bng-attr-grid bng-animate'>{''.join(cards)}</div>",
                    unsafe_allow_html=True)
        st.caption(f"Berdasarkan {total_players} pemain  •  Player attributes are from our team data.")
    else:
        placeholder_box("📊", "Belum Ada Data Pemain",
                        "Tambahkan pemain di menu Team untuk melihat statistik.")


def page_team():
    players = load_players()
    is_admin = st.session_state.is_admin

    section_header("👥", "Team Roster",
                   f"{len(players)} pemain terdaftar di database BIAENERGI")

    # --- ADMIN BAR ---
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("🔍 Cari pemain", placeholder="Ketik nama atau alias...",
                               label_visibility="collapsed")
    with col2:
        if is_admin:
            if st.button("➕ Tambah Pemain", width="stretch", key="btn_add_player"):
                st.session_state.show_add_player = True
                st.session_state.edit_player_id = None
        else:
            if st.button("🔐 Login Admin", width="stretch", key="btn_open_login"):
                st.session_state.login_open = True
    with col3:
        if is_admin:
            if st.button("🔒 Logout", width="stretch", key="btn_logout"):
                do_logout()
                st.rerun()

    # --- FLASH ---
    if st.session_state.flash:
        kind, msg = st.session_state.flash
        getattr(st, kind)(msg)
        st.session_state.flash = None

    # --- LOGIN FORM ---
    if st.session_state.login_open and not is_admin:
        with st.container(border=True):
            st.markdown("#### 🔐 Login Admin")
            if st.session_state.login_attempts >= MAX_LOGIN_ATTEMPTS:
                st.error("⛔ Terlalu banyak percobaan. Refresh halaman untuk coba lagi.")
            else:
                st.text_input("Password", type="password", key="login_pw",
                              on_change=None)
                c1, c2, _ = st.columns([1, 1, 3])
                if c1.button("Masuk", key="btn_do_login", type="primary", width="stretch"):
                    do_login()
                    st.rerun()
                if c2.button("Batal", key="btn_cancel_login", width="stretch"):
                    st.session_state.login_open = False
                    st.rerun()

    # --- FILTER ---
    shown = players
    if search:
        s = search.lower()
        shown = [p for p in players if s in p["nama"].lower() or s in p.get("alias", "").lower()]

    # --- PLAYER GRID ---
    if shown:
        cards_html = "".join(player_card(p) for p in shown)
        st.markdown(f"<div class='bng-player-grid bng-animate'>{cards_html}</div>",
                    unsafe_allow_html=True)
    else:
        placeholder_box("🔍", "Tidak Ada Pemain Ditemukan",
                        "Coba ubah kata kunci pencarian.")

    # --- ADMIN EDIT PANEL ---
    if is_admin:
        st.markdown("---")
        section_header("✏️", "Kelola Database Pemain",
                       "Edit atribut, tambah pemain baru, atau hapus pemain")

        # TAB: Edit / Tambah
        tab_edit, tab_add = st.tabs(["📝 Edit Pemain", "➕ Tambah Pemain"])

        with tab_edit:
            if not players:
                st.info("Belum ada pemain.")
            else:
                options = {f"{p['id']} — {p['nama']}": p["id"] for p in players}
                selected_label = st.selectbox("Pilih pemain", list(options.keys()),
                                              key="edit_select")
                pid = options[selected_label]
                player = next((p for p in players if p["id"] == pid), None)

                if player:
                    with st.form(f"form_edit_{pid}"):
                        c1, c2 = st.columns(2)
                        with c1:
                            new_nama = st.text_input("Nama", value=player["nama"])
                            new_alias = st.text_input("Alias", value=player.get("alias", ""))
                        with c2:
                            new_overall = st.slider("Overall Rating (1-100)", 1, 100,
                                                    int(player.get("overall", 50)))
                            new_photo = st.text_input("Photo URL (opsional)",
                                                      value=player.get("photo_url", ""))

                        st.markdown("**Roles**")
                        role_cols = st.columns(4)
                        new_roles = []
                        for i, r in enumerate(ROLE_KEYS):
                            if role_cols[i].checkbox(f"{ROLE_INFO[r]['emoji']} {r} ({ROLE_INFO[r]['nama']})",
                                                     value=(r in player.get("roles", [])),
                                                     key=f"edit_role_{pid}_{r}"):
                                new_roles.append(r)

                        st.markdown("**Attributes (1-99)**")
                        attr_cols = st.columns(6)
                        new_attrs = {}
                        for i, attr in enumerate(ALL_ATTRS):
                            with attr_cols[i % 6]:
                                new_attrs[attr] = st.number_input(
                                    attr, 1, 99,
                                    int(player.get("attributes", {}).get(attr, 50)),
                                    key=f"edit_attr_{pid}_{attr}"
                                )

                        cbtn1, cbtn2 = st.columns([1, 1])
                        save = cbtn1.form_submit_button("💾 Simpan", type="primary", width="stretch")
                        delete = cbtn2.form_submit_button("🗑️ Hapus", width="stretch")

                        if save:
                            if not new_roles:
                                st.error("⚠️ Pilih minimal 1 role!")
                            else:
                                for p in players:
                                    if p["id"] == pid:
                                        p["nama"] = new_nama.strip() or p["nama"]
                                        p["alias"] = new_alias.strip()
                                        p["overall"] = int(new_overall)
                                        p["roles"] = new_roles
                                        p["photo_url"] = new_photo.strip()
                                        p["attributes"] = new_attrs
                                        p["main_position"] = new_roles[0]
                                        break
                                if store.save_players(players):
                                    refresh_players()
                                    st.session_state.flash = ("success", f"✅ Data '{new_nama}' tersimpan.")
                                    st.rerun()
                                else:
                                    st.error("⚠️ Gagal menyimpan ke file.")

                        if delete:
                            players = [p for p in players if p["id"] != pid]
                            if store.save_players(players):
                                refresh_players()
                                st.session_state.flash = ("warning", f"🗑️ '{player['nama']}' dihapus.")
                                st.rerun()

        with tab_add:
            with st.form("form_add_player", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    new_nama = st.text_input("Nama *", placeholder="Nama lengkap")
                    new_alias = st.text_input("Alias", placeholder="Nama panggilan")
                with c2:
                    new_overall = st.slider("Overall Rating (1-100)", 1, 100, 50)
                    new_photo = st.text_input("Photo URL (opsional)", placeholder="https://...")

                st.markdown("**Roles**")
                role_cols = st.columns(4)
                new_roles = []
                for i, r in enumerate(ROLE_KEYS):
                    if role_cols[i].checkbox(f"{ROLE_INFO[r]['emoji']} {r}",
                                             value=(r == "A"),
                                             key=f"add_role_{r}"):
                        new_roles.append(r)

                st.markdown("**Attributes (default 50, ubah jika perlu)**")
                attr_cols = st.columns(6)
                new_attrs = {}
                for i, attr in enumerate(ALL_ATTRS):
                    with attr_cols[i % 6]:
                        new_attrs[attr] = st.number_input(attr, 1, 99, 50, key=f"add_attr_{attr}")

                submitted = st.form_submit_button("➕ Tambah Pemain", type="primary", width="stretch")
                if submitted:
                    if not new_nama.strip():
                        st.error("⚠️ Nama wajib diisi!")
                    elif not new_roles:
                        st.error("⚠️ Pilih minimal 1 role!")
                    else:
                        # Generate ID baru
                        existing_ids = [p["id"] for p in players]
                        nums = [int(i[1:]) for i in existing_ids if i.startswith("P") and i[1:].isdigit()]
                        next_num = (max(nums) + 1) if nums else 1
                        new_id = f"P{next_num:03d}"

                        new_player = {
                            "id": new_id,
                            "nama": new_nama.strip(),
                            "alias": new_alias.strip(),
                            "overall": int(new_overall),
                            "roles": new_roles,
                            "main_position": new_roles[0],
                            "positions": {
                                "1st": new_roles[0],
                                "2nd": new_roles[1] if len(new_roles) > 1 else "",
                                "3rd": new_roles[2] if len(new_roles) > 2 else "",
                                "4th": new_roles[3] if len(new_roles) > 3 else "",
                            },
                            "attributes": new_attrs,
                            "photo_url": new_photo.strip(),
                        }
                        players.append(new_player)
                        if store.save_players(players):
                            refresh_players()
                            st.session_state.flash = ("success", f"✅ '{new_player['nama']}' ditambahkan.")
                            st.rerun()
                        else:
                            st.error("⚠️ Gagal menyimpan.")


def page_team_generator():
    section_header("⚽", "Team Generator",
                   "Bagi tim secara otomatis dengan keseimbangan Overall Rating & aturan conflict.")
    placeholder_box(
        "🚧",
        "Fitur Team Generator — Segera Hadir",
        "Fitur ini akan tersedia di Fase 2. Berisi: Player Selection, Rules (Separating + Uniform), "
        "Team Configuration, Generate Team (dengan download PNG), dan simpan ke Match History."
    )


def page_match_history():
    section_header("📜", "Match History",
                   "Riwayat pertandingan yang telah digenerate dan disimpan.")
    matches = store.get_match_history()
    if not matches:
        placeholder_box(
            "📭",
            "Belum Ada Riwayat Match",
            "Riwayat akan muncul setelah Anda menyimpan hasil Generate Team di Fase 3."
        )
    else:
        st.write(f"Total {len(matches)} match tersimpan.")


def page_about():
    section_header("ℹ️", "Tentang BIAENERGI Futsal Academy",
                   "One Team, One Spirit — Play, Learn, Grow Together")

    st.markdown("""
    <div class='bng-more-box bng-animate'>
      <div class='bng-more-title'>
        More Than<br>Just a Game
        <small>MORE THAN JUST A GAME</small>
      </div>
      <div class='bng-more-item'>
        <div class='icon'>👥</div>
        <div class='txt'>
          <strong>Friendship</strong>
          <span>Builds Stronger Team</span>
        </div>
      </div>
      <div class='bng-more-item'>
        <div class='icon'>🏆</div>
        <div class='txt'>
          <strong>Effort</strong>
          <span>Brings Progress</span>
        </div>
      </div>
      <div class='bng-more-item'>
        <div class='icon'>🤍</div>
        <div class='txt'>
          <strong>Together</strong>
          <span>We Are Stronger</span>
        </div>
      </div>
      <div class='bng-more-tag'><span>BIAENERGI FUTSAL ACADEMY 👑</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ### 🎯 Visi
    Menjadi akademi futsal yang membangun karakter, sportivitas, dan skill pemain
    melalui pendekatan yang seimbang antara **Play, Learn, dan Grow**.

    ### 🧭 Misi
    - Mengembangkan skill teknis & taktik setiap pemain
    - Membangun kekompakan tim melalui latihan rutin
    - Menjunjung tinggi sportivitas di setiap pertandingan
    - Menciptakan lingkungan yang positif dan menyenangkan

    ### 💬 Filosofi Kami
    > *"Pantang menyerah meski skor tidak berpihak."*
    > — Never give up, even when the score isn't on our side.
    """)


# ==========================================
# MAIN APP
# ==========================================
def main():
    render_navbar()
    tabs = st.tabs(["🏠 Home", "👥 Team", "⚽ Team Generator", "📜 Match History", "ℹ️ About"])

    with tabs[0]:
        page_home()
    with tabs[1]:
        page_team()
    with tabs[2]:
        page_team_generator()
    with tabs[3]:
        page_match_history()
    with tabs[4]:
        page_about()

    render_footer()


if __name__ == "__main__":
    main()
