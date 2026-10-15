"""
============================================================
BIAENERGI FUTSAL ACADEMY — v5.0 (Fase 1 + 2 + 3)
============================================================
Menu : Home | Team | Team Generator | Match History | About
Data : JSON lokal (mudah migrasi ke Google Sheets di Fase 4)
Fitur:
  - Fase 1: Redesign BIAENERGI + Home dashboard + Team roster + Admin login
  - Fase 2: Team Generator (Selection, Rules 2-tab, Config, Generate + PNG)
  - Fase 3: Match History (simpan hasil, input skor & tanggal, list riwayat)
"""
import streamlit as st
import pandas as pd
import json
import os
import io
import random
import base64
import hashlib
from pathlib import Path
from html import escape as esc
from collections import defaultdict
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

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

h1, h2, h3 { letter-spacing: -.03em; font-weight: 800; color: #fff; }
p, li { color: #d1dce8; }
label { color: #cbd5e1 !important; }

/* ============ NAVBAR ============ */
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
.bng-logo { display: flex; align-items: center; gap: 14px; }
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

/* ============ HERO ============ */
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
  opacity: .35; z-index: 0;
}
.bng-hero-content { position: relative; z-index: 2; max-width: 580px; }
.bng-hero-kicker {
  display: inline-block; padding: 6px 16px;
  background: var(--bng-yellow); color: var(--bng-navy);
  font-weight: 900; font-size: 13px; font-style: italic;
  letter-spacing: .04em; transform: rotate(-2deg);
  border-radius: 4px; margin-bottom: 18px;
  box-shadow: 0 4px 14px rgba(251,191,36,.35);
}
.bng-hero h1 {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(2.2rem, 4.5vw, 3.6rem);
  font-weight: 900; line-height: 1.02; color: #fff;
  margin: 0 0 16px 0;
  text-shadow: 0 6px 24px rgba(0,0,0,.5);
  letter-spacing: -.02em;
}
.bng-hero h1 .hl { color: var(--bng-yellow); display: block; }
.bng-hero-quote {
  font-style: italic; font-size: 1.05rem; color: #e0ecf8;
  border-left: 4px solid var(--bng-yellow);
  padding-left: 14px; margin: 16px 0; line-height: 1.5;
}
.bng-hero-sub { font-size: .88rem; color: #b8c8dd; margin-top: 12px; }
.bng-hero-tag {
  position: absolute; right: 40px; top: 50%;
  transform: translateY(-50%); z-index: 2;
  text-align: center; font-family: 'Orbitron', sans-serif;
}
.bng-hero-tag .t1, .bng-hero-tag .t2, .bng-hero-tag .t3 {
  display: block; font-style: italic; font-weight: 900;
  color: var(--bng-yellow); line-height: 1.1;
  text-shadow: 0 4px 16px rgba(0,0,0,.6);
  font-size: 42px;
}

/* ============ SECTION ============ */
.bng-section {
  display: flex; align-items: center; gap: 12px;
  margin: 28px 0 16px 0;
}
.bng-section .icon { font-size: 24px; }
.bng-section h2 { margin: 0; font-size: 1.3rem; font-weight: 800; color: #fff; }
.bng-section .sub { color: var(--bng-text-dim); font-size: .85rem; margin-top: 2px; }

/* ============ STAT CARDS ============ */
.bng-stat-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
}
.bng-stat-card {
  background: var(--bng-glass);
  border: 1px solid var(--bng-glass-border);
  border-radius: 18px; padding: 20px 18px;
  backdrop-filter: blur(12px);
  transition: transform .2s, border-color .2s, box-shadow .2s;
  position: relative; overflow: hidden;
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
.bng-stat-icon { font-size: 28px; margin-bottom: 10px; display: inline-block; }
.bng-stat-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 34px; font-weight: 900;
  color: var(--bng-yellow);
  line-height: 1; margin: 6px 0 4px 0;
}
.bng-stat-label {
  font-size: .82rem; color: #cbd5e1; font-weight: 600;
  text-transform: uppercase; letter-spacing: .05em;
}

/* ============ ATTR BARS ============ */
.bng-attr-grid {
  display: grid; grid-template-columns: repeat(6, 1fr);
  gap: 12px; margin-top: 10px;
}
.bng-attr-card {
  background: var(--bng-glass);
  border: 1px solid var(--bng-glass-border);
  border-radius: 14px; padding: 14px;
  text-align: center; backdrop-filter: blur(12px);
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
  color: #fff; margin-bottom: 8px;
}
.bng-attr-bar {
  height: 5px; border-radius: 3px;
  background: rgba(255,255,255,.08); overflow: hidden;
}
.bng-attr-bar-fill {
  height: 100%; border-radius: 3px;
  transition: width .8s cubic-bezier(.2,.8,.2,1);
}

/* ============ MORE BOX ============ */
.bng-more-box {
  background:
    radial-gradient(circle at 100% 0%, rgba(251,191,36,.15), transparent 55%),
    linear-gradient(135deg, rgba(13,35,80,.85), rgba(10,26,58,.9));
  border: 1px solid rgba(251,191,36,.35);
  border-radius: 22px; padding: 26px 24px;
  backdrop-filter: blur(14px);
  position: relative; overflow: hidden;
}
.bng-more-title {
  font-family: 'Orbitron', sans-serif;
  font-style: italic; font-size: 24px; font-weight: 900;
  color: var(--bng-yellow); line-height: 1.1;
  margin-bottom: 20px;
  text-shadow: 0 4px 14px rgba(251,191,36,.3);
}
.bng-more-title small {
  display: block; font-size: 12px; font-style: normal;
  letter-spacing: .3em; color: #cbd5e1;
  margin-top: 6px; font-family: 'Inter', sans-serif; font-weight: 700;
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
.bng-more-item .txt span { color: #94a3b8; font-size: .8rem; }
.bng-more-tag {
  margin-top: 18px; display: inline-block;
  padding: 8px 18px;
  background: linear-gradient(90deg, var(--bng-yellow-dark), var(--bng-yellow));
  color: var(--bng-navy);
  font-family: 'Orbitron', sans-serif;
  font-weight: 900; font-size: 13px;
  letter-spacing: .08em; border-radius: 6px;
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
  border-radius: 16px; padding: 14px;
  backdrop-filter: blur(12px);
  display: flex; gap: 12px; align-items: center;
  transition: transform .22s cubic-bezier(.2,.8,.2,1), border-color .22s, box-shadow .22s;
  position: relative; overflow: hidden;
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
  width: 56px; height: 56px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 18px; color: #fff;
  flex-shrink: 0;
  border: 2px solid rgba(255,255,255,.2);
  box-shadow: 0 4px 12px rgba(0,0,0,.3);
  overflow: hidden; position: relative;
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
  display: inline-block; padding: 2px 8px;
  border-radius: 6px;
  font-size: 10px; font-weight: 800;
  letter-spacing: .04em;
}
.bng-role-chip.gk { background: rgba(251,191,36,.2); border: 1px solid rgba(251,191,36,.5); color: #fde68a; }
.bng-role-chip.a  { background: rgba(59,130,246,.25); border: 1px solid rgba(96,165,250,.5); color: #bfdbfe; }
.bng-role-chip.f  { background: rgba(34,197,94,.2); border: 1px solid rgba(34,197,94,.5); color: #bbf7d0; }
.bng-role-chip.p  { background: rgba(239,68,68,.2); border: 1px solid rgba(239,68,68,.5); color: #fecaca; }

.bng-ovr-badge {
  position: absolute; top: 10px; right: 10px;
  background: linear-gradient(135deg, var(--bng-yellow-dark), var(--bng-yellow));
  color: var(--bng-navy);
  font-family: 'Orbitron', sans-serif;
  font-weight: 900; font-size: 13px;
  padding: 3px 9px; border-radius: 8px;
  box-shadow: 0 4px 10px rgba(251,191,36,.4);
}

/* ============ BUTTONS ============ */
.stButton > button {
  border: 1px solid rgba(251,191,36,.4) !important;
  border-radius: 12px !important;
  font-weight: 800 !important;
  background: linear-gradient(110deg, var(--bng-yellow-dark), var(--bng-yellow)) !important;
  color: var(--bng-navy) !important;
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

[data-testid="stDownloadButton"] button {
  background: linear-gradient(110deg, #16a34a, #22c55e) !important;
  color: #fff !important;
  border-color: rgba(34,197,94,.5) !important;
}
[data-testid="stDownloadButton"] button * { color: #fff !important; }

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

/* ============ PLACEHOLDER ============ */
.bng-placeholder {
  text-align: center; padding: 60px 30px;
  border-radius: 22px;
  background: var(--bng-glass);
  border: 2px dashed rgba(96,165,250,.3);
  backdrop-filter: blur(12px);
  margin: 16px 0;
}
.bng-placeholder .emoji {
  font-size: 64px; margin-bottom: 16px;
  filter: drop-shadow(0 6px 20px rgba(251,191,36,.3));
}
.bng-placeholder h3 { color: var(--bng-yellow); margin: 0 0 8px 0; }
.bng-placeholder p { color: #94a3b8; margin: 0; }

/* ============ GENERATED TEAM CARD ============ */
.bng-team-card {
  border-radius: 18px; padding: 18px;
  background: rgba(13,35,80,.65);
  border: 2px solid rgba(96,165,250,.3);
  backdrop-filter: blur(12px);
  margin: 14px 0;
  box-shadow: 0 12px 32px rgba(0,0,0,.3);
}
.bng-team-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 12px;
  flex-wrap: wrap; gap: 10px;
}
.bng-team-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 20px; font-weight: 900;
  color: #fff;
  display: flex; align-items: center; gap: 10px;
}
.bng-team-uniform {
  padding: 5px 14px; border-radius: 20px;
  font-size: 12px; font-weight: 800;
  border: 1px solid rgba(255,255,255,.3);
}
.bng-team-rating {
  padding: 5px 14px; border-radius: 20px;
  font-size: 12px; font-weight: 800;
  background: linear-gradient(110deg, #0d47a1, #20d9e8);
  color: #fff;
}
.bng-team-meta {
  font-size: 13px; color: #cbd5e1;
  margin: 6px 0;
  line-height: 1.5;
}

/* ============ MATCH CARD ============ */
.bng-match-card {
  background: var(--bng-glass);
  border: 1px solid var(--bng-glass-border);
  border-radius: 16px;
  padding: 18px;
  margin: 12px 0;
  backdrop-filter: blur(12px);
}
.bng-match-header {
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 10px;
  margin-bottom: 12px;
}
.bng-match-id {
  font-family: 'Orbitron', sans-serif;
  font-weight: 900; color: var(--bng-yellow);
  font-size: 14px;
}
.bng-match-date {
  font-size: 12px; color: #94a3b8;
}
.bng-match-score {
  display: flex; align-items: center; justify-content: center;
  gap: 20px; margin: 12px 0;
}
.bng-match-team {
  flex: 1; text-align: center;
}
.bng-match-team .name {
  font-weight: 800; color: #fff;
  font-size: 15px; margin-bottom: 4px;
}
.bng-match-team .uniform {
  font-size: 11px; color: #94a3b8;
}
.bng-match-score-num {
  font-family: 'Orbitron', sans-serif;
  font-size: 36px; font-weight: 900;
  color: var(--bng-yellow);
  min-width: 90px;
  text-align: center;
}

/* ============ FOOTER ============ */
.bng-footer {
  margin-top: 40px; padding: 24px;
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

/* ============ ANIMATION ============ */
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
    "GK": {"nama": "Kiper",  "emoji": "🧤", "css": "gk"},
    "A":  {"nama": "Anchor", "emoji": "⚓", "css": "a"},
    "F":  {"nama": "Flank",  "emoji": "🪽", "css": "f"},
    "P":  {"nama": "Pivot",  "emoji": "🔥", "css": "p"},
}
ROLE_KEYS = ["GK", "A", "F", "P"]

PHY_COLS = ["STA", "AKS", "SPR", "AGI", "BAL", "STR"]
TEC_COLS = ["CON", "DRI", "PAS", "SHA", "SHP", "TAC"]
MTC_COLS = ["VIS", "OFB", "COM", "AGR", "TMW"]
GKS_COLS = ["DEC", "REF", "POS", "THR", "KIC", "BRV"]
ALL_ATTRS = PHY_COLS + TEC_COLS + MTC_COLS + GKS_COLS

UNIFORM_OPTIONS = ["Biru", "Putih", "Merah", "Kuning", "Ungu", "Hitam", "Hijau"]
COLOR_MAP = {
    "Biru": "#1976d2", "Putih": "#ffffff", "Merah": "#d32f2f",
    "Kuning": "#fbc02d", "Ungu": "#7b1fa2", "Hitam": "#212121",
    "Hijau": "#388e3c", "Abu-abu": "#757575",
}
DARK_UNIFORMS = ["Hitam", "Biru", "Merah", "Ungu", "Hijau"]

FORMATIONS = {
    "Diamond (1-2-1)": {
        "pola": "1 Anchor • 2 Flank • 1 Pivot",
        "karakter": "Seimbang antara bertahan & menyerang. Formasi paling populer.",
        "sketsa": "[Pivot] [Flank] [Flank] [Anchor]",
        "positions": [{"label": "GK", "x": 8, "y": 50}, {"label": "A", "x": 28, "y": 50},
                      {"label": "F", "x": 52, "y": 22}, {"label": "F", "x": 52, "y": 78},
                      {"label": "P", "x": 78, "y": 50}],
    },
    "Pyramid / Wall (2-1-1)": {
        "pola": "2 Defender • 1 Midfielder • 1 Pivot",
        "karakter": "Defensif kokoh. Cocok untuk counter attack.",
        "sketsa": "[Pivot] [Midfielder] [Def] [Def]",
        "positions": [{"label": "GK", "x": 8, "y": 50}, {"label": "A", "x": 28, "y": 32},
                      {"label": "A", "x": 28, "y": 68}, {"label": "F", "x": 55, "y": 50},
                      {"label": "P", "x": 80, "y": 50}],
    },
    "The Box / Square (2-2)": {
        "pola": "2 Belakang • 2 Depan (sejajar)",
        "karakter": "Fleksibel & simetris. Butuh komunikasi intens.",
        "sketsa": "[Pivot] [Pivot] [Def] [Def]",
        "positions": [{"label": "GK", "x": 8, "y": 50}, {"label": "A", "x": 32, "y": 30},
                      {"label": "A", "x": 32, "y": 70}, {"label": "P", "x": 72, "y": 30},
                      {"label": "P", "x": 72, "y": 70}],
    },
    "Formasi Y (1-1-2)": {
        "pola": "1 Anchor • 1 Midfielder • 2 Pivot",
        "karakter": "Agresif. High pressing dengan 2 penyerang.",
        "sketsa": "[Pivot] [Pivot] [Midfielder] [Anchor]",
        "positions": [{"label": "GK", "x": 8, "y": 50}, {"label": "A", "x": 28, "y": 50},
                      {"label": "F", "x": 52, "y": 50}, {"label": "P", "x": 78, "y": 30},
                      {"label": "P", "x": 78, "y": 70}],
    },
    "Park the Bus (3-1)": {
        "pola": "3 Defender • 1 Pivot",
        "karakter": "Defensif total. Untuk mempertahankan skor.",
        "sketsa": "[Pivot] [Def][Def][Def]",
        "positions": [{"label": "GK", "x": 8, "y": 50}, {"label": "A", "x": 30, "y": 22},
                      {"label": "A", "x": 30, "y": 50}, {"label": "A", "x": 30, "y": 78},
                      {"label": "P", "x": 72, "y": 50}],
    },
    "Total / Flat (4-0)": {
        "pola": "4 Pemain Sejajar (dinamis)",
        "karakter": "Rotasi dinamis tanpa pivot murni.",
        "sketsa": "[P1] [P2] [P3] [P4] (Sejajar)",
        "positions": [{"label": "GK", "x": 8, "y": 50}, {"label": "F", "x": 48, "y": 18},
                      {"label": "F", "x": 48, "y": 40}, {"label": "F", "x": 48, "y": 60},
                      {"label": "F", "x": 48, "y": 82}],
    },
}

AVATAR_COLORS = ["#3b82f6", "#22c55e", "#ef4444", "#a855f7",
                 "#f59e0b", "#06b6d4", "#ec4899", "#6366f1"]

MAX_LOGIN_ATTEMPTS = 5
DEFAULT_ADMIN_PASSWORD = "BIAFUTSAL"
PAY_OPTIONS = ["Belum", "Cicil", "Done"]

# ==========================================
# SEED DATA
# ==========================================
SEED_PLAYERS = [
    {"id": "P001", "nama": "Ade Suryadana",     "alias": "Ade",     "overall": 100, "positions": ["F", "GK", "P", "A"], "attributes": {"STA": 97, "AKS": 99, "SPR": 98, "AGI": 99, "BAL": 94, "STR": 96, "CON": 95, "DRI": 98, "PAS": 94, "SHA": 99, "SHP": 99, "TAC": 88, "VIS": 90, "OFB": 93, "COM": 91, "AGR": 94, "TMW": 92, "DEC": 78, "REF": 76, "POS": 77, "THR": 74, "KIC": 76, "BRV": 79}},
    {"id": "P002", "nama": "Aldo S.",           "alias": "Aldo",    "overall": 95,  "positions": ["A", "P", "GK", "F"], "attributes": {"STA": 92, "AKS": 90, "SPR": 88, "AGI": 94, "BAL": 96, "STR": 93, "CON": 91, "DRI": 93, "PAS": 95, "SHA": 89, "SHP": 90, "TAC": 97, "VIS": 96, "OFB": 95, "COM": 94, "AGR": 92, "TMW": 93, "DEC": 85, "REF": 82, "POS": 84, "THR": 80, "KIC": 83, "BRV": 86}},
    {"id": "P003", "nama": "Aprizqi R",         "alias": "AP",      "overall": 95,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 92, "AKS": 90, "SPR": 88, "AGI": 94, "BAL": 96, "STR": 93, "CON": 91, "DRI": 93, "PAS": 95, "SHA": 89, "SHP": 90, "TAC": 97, "VIS": 96, "OFB": 95, "COM": 94, "AGR": 92, "TMW": 93, "DEC": 85, "REF": 82, "POS": 84, "THR": 80, "KIC": 83, "BRV": 86}},
    {"id": "P004", "nama": "Arby R",            "alias": "Byrus",   "overall": 100, "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 97, "AKS": 95, "SPR": 93, "AGI": 99, "BAL": 99, "STR": 98, "CON": 96, "DRI": 98, "PAS": 99, "SHA": 94, "SHP": 95, "TAC": 99, "VIS": 99, "OFB": 99, "COM": 98, "AGR": 97, "TMW": 98, "DEC": 90, "REF": 87, "POS": 89, "THR": 85, "KIC": 88, "BRV": 91}},
    {"id": "P005", "nama": "Fadhli D. Ikram",   "alias": "Dzil",    "overall": 95,  "positions": ["A", "P", "GK", "F"], "attributes": {"STA": 92, "AKS": 90, "SPR": 88, "AGI": 94, "BAL": 96, "STR": 93, "CON": 91, "DRI": 93, "PAS": 95, "SHA": 89, "SHP": 90, "TAC": 97, "VIS": 96, "OFB": 95, "COM": 94, "AGR": 92, "TMW": 93, "DEC": 85, "REF": 82, "POS": 84, "THR": 80, "KIC": 83, "BRV": 86}},
    {"id": "P006", "nama": "Farhan I. A.",      "alias": "Han",     "overall": 70,  "positions": ["P", "A", "F", "GK"], "attributes": {"STA": 75, "AKS": 73, "SPR": 70, "AGI": 74, "BAL": 78, "STR": 76, "CON": 74, "DRI": 76, "PAS": 73, "SHA": 79, "SHP": 80, "TAC": 71, "VIS": 72, "OFB": 74, "COM": 72, "AGR": 75, "TMW": 73, "DEC": 64, "REF": 62, "POS": 63, "THR": 60, "KIC": 62, "BRV": 65}},
    {"id": "P007", "nama": "Geraldo H.",        "alias": "Geraldo", "overall": 80,  "positions": ["A", "GK", "P", "F"], "attributes": {"STA": 82, "AKS": 80, "SPR": 78, "AGI": 84, "BAL": 86, "STR": 83, "CON": 81, "DRI": 83, "PAS": 85, "SHA": 79, "SHP": 80, "TAC": 87, "VIS": 86, "OFB": 85, "COM": 84, "AGR": 82, "TMW": 83, "DEC": 75, "REF": 72, "POS": 74, "THR": 70, "KIC": 73, "BRV": 76}},
    {"id": "P008", "nama": "Hanz Seca",         "alias": "Hanz",    "overall": 60,  "positions": ["GK", "A", "P", "F"], "attributes": {"STA": 61, "AKS": 59, "SPR": 57, "AGI": 60, "BAL": 62, "STR": 63, "CON": 58, "DRI": 60, "PAS": 58, "SHA": 56, "SHP": 57, "TAC": 62, "VIS": 65, "OFB": 68, "COM": 67, "AGR": 66, "TMW": 68, "DEC": 70, "REF": 72, "POS": 71, "THR": 69, "KIC": 70, "BRV": 73}},
    {"id": "P009", "nama": "Ibrahim",           "alias": "Bacing",  "overall": 90,  "positions": ["F", "P", "A", "GK"], "attributes": {"STA": 88, "AKS": 85, "SPR": 92, "AGI": 87, "BAL": 89, "STR": 86, "CON": 85, "DRI": 88, "PAS": 84, "SHA": 90, "SHP": 91, "TAC": 82, "VIS": 84, "OFB": 86, "COM": 83, "AGR": 87, "TMW": 85, "DEC": 72, "REF": 70, "POS": 71, "THR": 68, "KIC": 70, "BRV": 73}},
    {"id": "P010", "nama": "Jehua Kusuma Dewa", "alias": "Jeje",    "overall": 70,  "positions": ["A", "F", "P", "GK"], "attributes": {"STA": 72, "AKS": 70, "SPR": 68, "AGI": 74, "BAL": 76, "STR": 73, "CON": 71, "DRI": 73, "PAS": 75, "SHA": 69, "SHP": 70, "TAC": 77, "VIS": 76, "OFB": 75, "COM": 74, "AGR": 72, "TMW": 73, "DEC": 65, "REF": 62, "POS": 64, "THR": 60, "KIC": 63, "BRV": 66}},
    {"id": "P011", "nama": "M. Ardhana W. N.",  "alias": "Ardha",   "overall": 60,  "positions": ["GK", "A", "P", "F"], "attributes": {"STA": 61, "AKS": 59, "SPR": 57, "AGI": 60, "BAL": 62, "STR": 63, "CON": 58, "DRI": 60, "PAS": 58, "SHA": 56, "SHP": 57, "TAC": 62, "VIS": 65, "OFB": 68, "COM": 67, "AGR": 66, "TMW": 68, "DEC": 70, "REF": 72, "POS": 71, "THR": 69, "KIC": 70, "BRV": 73}},
    {"id": "P012", "nama": "M. Daffa A.",       "alias": "Daffa",   "overall": 95,  "positions": ["F", "A", "P", "GK"], "attributes": {"STA": 94, "AKS": 92, "SPR": 96, "AGI": 92, "BAL": 94, "STR": 91, "CON": 90, "DRI": 93, "PAS": 89, "SHA": 95, "SHP": 96, "TAC": 87, "VIS": 88, "OFB": 90, "COM": 88, "AGR": 91, "TMW": 89, "DEC": 72, "REF": 70, "POS": 71, "THR": 68, "KIC": 70, "BRV": 73}},
    {"id": "P013", "nama": "M. Zidan G.",       "alias": "Zidan",   "overall": 100, "positions": ["F", "P", "A", "GK"], "attributes": {"STA": 97, "AKS": 95, "SPR": 98, "AGI": 99, "BAL": 97, "STR": 99, "CON": 96, "DRI": 98, "PAS": 95, "SHA": 99, "SHP": 99, "TAC": 89, "VIS": 90, "OFB": 92, "COM": 90, "AGR": 93, "TMW": 91, "DEC": 74, "REF": 72, "POS": 73, "THR": 70, "KIC": 72, "BRV": 75}},
    {"id": "P014", "nama": "Mahardhyka P.",     "alias": "Dhyka",   "overall": 90,  "positions": ["P", "F", "A", "GK"], "attributes": {"STA": 92, "AKS": 90, "SPR": 88, "AGI": 89, "BAL": 94, "STR": 91, "CON": 90, "DRI": 92, "PAS": 94, "SHA": 88, "SHP": 89, "TAC": 96, "VIS": 95, "OFB": 94, "COM": 93, "AGR": 91, "TMW": 92, "DEC": 72, "REF": 70, "POS": 71, "THR": 68, "KIC": 70, "BRV": 73}},
    {"id": "P015", "nama": "Martin Koko",       "alias": "Martin",  "overall": 90,  "positions": ["A", "GK", "P", "F"], "attributes": {"STA": 88, "AKS": 85, "SPR": 82, "AGI": 89, "BAL": 91, "STR": 88, "CON": 86, "DRI": 88, "PAS": 90, "SHA": 84, "SHP": 85, "TAC": 92, "VIS": 91, "OFB": 90, "COM": 89, "AGR": 87, "TMW": 88, "DEC": 80, "REF": 77, "POS": 79, "THR": 75, "KIC": 78, "BRV": 81}},
    {"id": "P016", "nama": "Musyaffa C. M.",    "alias": "Mus",     "overall": 75,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 77, "AKS": 75, "SPR": 73, "AGI": 79, "BAL": 81, "STR": 78, "CON": 76, "DRI": 78, "PAS": 80, "SHA": 74, "SHP": 75, "TAC": 82, "VIS": 81, "OFB": 80, "COM": 79, "AGR": 77, "TMW": 78, "DEC": 70, "REF": 67, "POS": 69, "THR": 65, "KIC": 68, "BRV": 71}},
    {"id": "P017", "nama": "Naufal Y.",         "alias": "Naufal",  "overall": 70,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 72, "AKS": 70, "SPR": 68, "AGI": 74, "BAL": 76, "STR": 73, "CON": 71, "DRI": 73, "PAS": 75, "SHA": 69, "SHP": 70, "TAC": 77, "VIS": 76, "OFB": 75, "COM": 74, "AGR": 72, "TMW": 73, "DEC": 65, "REF": 62, "POS": 64, "THR": 60, "KIC": 63, "BRV": 66}},
    {"id": "P018", "nama": "Nur Sahrul",        "alias": "Aloenk",  "overall": 95,  "positions": ["F", "P", "A", "GK"], "attributes": {"STA": 94, "AKS": 92, "SPR": 96, "AGI": 92, "BAL": 94, "STR": 91, "CON": 90, "DRI": 93, "PAS": 89, "SHA": 95, "SHP": 96, "TAC": 87, "VIS": 88, "OFB": 90, "COM": 88, "AGR": 91, "TMW": 89, "DEC": 72, "REF": 70, "POS": 71, "THR": 68, "KIC": 70, "BRV": 73}},
    {"id": "P019", "nama": "R. Hafis M.",       "alias": "Fis",     "overall": 90,  "positions": ["F", "GK", "A", "P"], "attributes": {"STA": 88, "AKS": 85, "SPR": 92, "AGI": 87, "BAL": 89, "STR": 86, "CON": 85, "DRI": 88, "PAS": 84, "SHA": 90, "SHP": 91, "TAC": 82, "VIS": 84, "OFB": 86, "COM": 83, "AGR": 87, "TMW": 85, "DEC": 78, "REF": 80, "POS": 79, "THR": 77, "KIC": 78, "BRV": 81}},
    {"id": "P020", "nama": "Rafi M. A.",        "alias": "Rafi",    "overall": 80,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 82, "AKS": 80, "SPR": 78, "AGI": 84, "BAL": 86, "STR": 83, "CON": 81, "DRI": 83, "PAS": 85, "SHA": 79, "SHP": 80, "TAC": 87, "VIS": 86, "OFB": 85, "COM": 84, "AGR": 82, "TMW": 83, "DEC": 75, "REF": 72, "POS": 74, "THR": 70, "KIC": 73, "BRV": 76}},
    {"id": "P021", "nama": "Rafif Kusuma",      "alias": "RaKus",   "overall": 70,  "positions": ["A", "P", "F", "GK"], "attributes": {"STA": 72, "AKS": 70, "SPR": 68, "AGI": 74, "BAL": 76, "STR": 73, "CON": 71, "DRI": 73, "PAS": 75, "SHA": 69, "SHP": 70, "TAC": 77, "VIS": 76, "OFB": 75, "COM": 74, "AGR": 72, "TMW": 73, "DEC": 65, "REF": 62, "POS": 64, "THR": 60, "KIC": 63, "BRV": 66}},
    {"id": "P022", "nama": "Teguh A. R.",       "alias": "PapiKai", "overall": 80,  "positions": ["GK", "A", "P", "F"], "attributes": {"STA": 82, "AKS": 80, "SPR": 78, "AGI": 84, "BAL": 86, "STR": 83, "CON": 81, "DRI": 83, "PAS": 85, "SHA": 79, "SHP": 80, "TAC": 87, "VIS": 86, "OFB": 85, "COM": 84, "AGR": 82, "TMW": 83, "DEC": 78, "REF": 80, "POS": 79, "THR": 77, "KIC": 78, "BRV": 81}},
    {"id": "P023", "nama": "Yadhit P.",         "alias": "Yadhit",  "overall": 75,  "positions": ["A", "GK", "P", "F"], "attributes": {"STA": 77, "AKS": 75, "SPR": 73, "AGI": 79, "BAL": 81, "STR": 78, "CON": 76, "DRI": 78, "PAS": 80, "SHA": 74, "SHP": 75, "TAC": 82, "VIS": 81, "OFB": 80, "COM": 79, "AGR": 77, "TMW": 78, "DEC": 73, "REF": 75, "POS": 74, "THR": 72, "KIC": 73, "BRV": 76}},
]


def seed_players():
    result = []
    for p in SEED_PLAYERS:
        roles = list(dict.fromkeys(p["positions"]))
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
            "photo_url": "",
        })
    return result


# ==========================================
# DATA STORE LAYER (abstraksi untuk migrasi ke Sheets)
# ==========================================
class JSONStore:
    def __init__(self, players_path: Path, match_path: Path):
        self.players_path = players_path
        self.match_path = match_path

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

    @staticmethod
    def _write_json(path: Path, data) -> bool:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False


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


def image_to_base64(path: Path) -> str | None:
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
    pid = player.get("id", "")
    # 1) File lokal
    for ext in ("png", "jpg", "jpeg", "webp"):
        img_path = AVATARS_DIR / f"{pid}.{ext}"
        b64 = image_to_base64(img_path)
        if b64:
            return (f"<div class='bng-avatar' style='background:{color_for(player['nama'])}'>"
                    f"<img src='{b64}' alt='{esc(player['nama'])}'></div>")
    # 2) URL
    url = (player.get("photo_url") or "").strip()
    if url:
        return (f"<div class='bng-avatar' style='background:{color_for(player['nama'])}'>"
                f"<img src='{esc(url)}' alt='{esc(player['nama'])}' "
                f"onerror=\"this.style.display='none'\"></div>")
    # 3) Inisial
    return (f"<div class='bng-avatar' style='background:{color_for(player['nama'])}'>"
            f"{esc(initials(player['nama']))}</div>")


def role_chip_html(role: str) -> str:
    info = ROLE_INFO.get(role, {})
    return f"<span class='bng-role-chip {info.get('css', '')}'>{role}</span>"


def hero_background_css() -> str:
    b64 = image_to_base64(HERO_IMG)
    return f"background-image: url('{b64}');" if b64 else ""


def flat_html(s: str) -> str:
    return " ".join(line.strip() for line in s.splitlines() if line.strip())


# ==========================================
# SESSION STATE
# ==========================================
_defaults = {
    "page": "Home",
    "is_admin": False,
    "login_open": False,
    "login_attempts": 0,
    "players_cache": None,
    "show_add_player": False,
    "flash": None,
    # Fase 2
    "gen_selected": None,
    "gen_rules": [],
    "gen_uniform_rules": {},
    "gen_num_teams": 2,
    "gen_team_uniforms": [],
    "gen_result": None,
    "gen_show_uniform_login": False,
    # Fase 3
    "match_edit_id": None,
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
    st.session_state.flash = ("info", "🔒 Logout. Mode admin nonaktif.")


# ==========================================
# TEAM GENERATOR ENGINE
# ==========================================
def generate_teams(players, ratings, rules, num_teams, team_uniforms_in, uniform_rules):
    """Generate balanced teams based on overall rating."""
    players = players[:]

    def get_rating(p):
        return ratings.get(p, 50)

    # Conflict map
    conflicts = defaultdict(set)
    for p1, p2 in rules:
        conflicts[p1].add(p2)
        conflicts[p2].add(p1)

    # Split GK vs non-GK
    gks = [p for p in players if "GK" in ratings.get(p + "__roles", [])]
    # Karena ratings tidak menyimpan roles, kita ambil roles dari argument roles_map
    # Sebenarnya kita perlu parameter roles. Ubah signature fungsi.
    return None  # Placeholder — akan digantikan oleh versi lengkap di bawah


def generate_teams_v2(players, roles_map, ratings, rules, num_teams, team_uniforms_in, uniform_rules):
    """Versi lengkap dengan roles_map."""
    players = players[:]

    def get_rating(p):
        return ratings.get(p, 50)

    conflicts = defaultdict(set)
    for p1, p2 in rules:
        conflicts[p1].add(p2)
        conflicts[p2].add(p1)

    gks = [p for p in players if "GK" in roles_map.get(p, [])]
    non_gks = [p for p in players if "GK" not in roles_map.get(p, [])]
    teams = [[] for _ in range(num_teams)]

    def team_rating(i):
        return sum(get_rating(p) for p in teams[i])

    def team_size(i):
        return len(teams[i])

    def conflict_with_team(player, tidx):
        return any(t in conflicts.get(player, set()) for t in teams[tidx])

    def valid_teams(player):
        v = [i for i in range(num_teams) if not conflict_with_team(player, i)]
        return v if v else list(range(num_teams))

    # Assign GK dulu
    gks_sorted = sorted(gks, key=get_rating, reverse=True)
    random.shuffle(gks_sorted)
    gks_sorted = sorted(gks_sorted, key=get_rating, reverse=True)
    for gk in gks_sorted[:num_teams]:
        candidates = valid_teams(gk)
        best = min(candidates, key=lambda i: (team_rating(i), team_size(i)))
        teams[best].append(gk)

    remaining_gks = gks_sorted[num_teams:]
    remaining = non_gks + remaining_gks
    random.shuffle(remaining)
    remaining.sort(key=get_rating, reverse=True)

    for player in remaining:
        candidates = valid_teams(player)
        def score(i, player=player):
            team_roles = [r for p in teams[i] for r in roles_map.get(p, [])]
            plist = roles_map.get(player, [])
            role_need = sum(1 for r in plist if team_roles.count(r) < 2)
            return (team_rating(i), team_size(i), -role_need)
        best = min(candidates, key=score)
        teams[best].append(player)

    # Balance swaps
    def try_balance(max_rounds=40):
        for _ in range(max_rounds):
            totals = [team_rating(i) for i in range(num_teams)]
            strongest = max(range(num_teams), key=lambda i: totals[i])
            weakest = min(range(num_teams), key=lambda i: totals[i])
            gap = totals[strongest] - totals[weakest]
            if gap <= 3:
                break
            improved = False
            for p_s in list(teams[strongest]):
                if conflict_with_team(p_s, weakest):
                    continue
                for p_w in list(teams[weakest]):
                    if conflict_with_team(p_w, strongest):
                        continue
                    new_s = totals[strongest] - get_rating(p_s) + get_rating(p_w)
                    new_w = totals[weakest] - get_rating(p_w) + get_rating(p_s)
                    if abs(new_s - new_w) < gap:
                        teams[strongest].remove(p_s)
                        teams[weakest].remove(p_w)
                        teams[strongest].append(p_w)
                        teams[weakest].append(p_s)
                        improved = True
                        break
                if improved:
                    break
            if not improved:
                break
    try_balance()

    # Assign formations & uniforms
    formation_names = list(FORMATIONS.keys())
    team_formations = {i: random.choice(formation_names) for i in range(num_teams)}
    team_uniforms = {
        i: (team_uniforms_in[i] if i < len(team_uniforms_in) and team_uniforms_in[i]
            else UNIFORM_OPTIONS[i % len(UNIFORM_OPTIONS)])
        for i in range(num_teams)
    }

    # Apply uniform rules by swapping team uniforms
    if uniform_rules:
        for _ in range(60):
            broken = []
            for tidx, team in enumerate(teams):
                for player in team:
                    allowed = uniform_rules.get(player)
                    if allowed and team_uniforms[tidx] not in allowed:
                        broken.append((tidx, player, allowed))
            if not broken:
                break
            fixed = False
            for tidx, player, allowed in broken:
                candidates = [j for j in range(num_teams)
                              if j != tidx and team_uniforms[j] in allowed]
                def safety(j):
                    new_uni = team_uniforms[tidx]
                    old_uni = team_uniforms[j]
                    for p in teams[j]:
                        a = uniform_rules.get(p)
                        if a and new_uni not in a:
                            return 1
                    for p in teams[tidx]:
                        if p == player:
                            continue
                        a = uniform_rules.get(p)
                        if a and old_uni not in a:
                            return 1
                    return 0
                candidates.sort(key=safety)
                if candidates and safety(candidates[0]) == 0:
                    j = candidates[0]
                    team_uniforms[tidx], team_uniforms[j] = team_uniforms[j], team_uniforms[tidx]
                    fixed = True
                    break
            if not fixed:
                break

    return teams, team_formations, team_uniforms


# ==========================================
# SVG PITCH
# ==========================================
def formation_svg(formation_name, width=320, height=200):
    form = FORMATIONS.get(formation_name, {})
    positions = form.get("positions", [])
    W, H = 400, 250
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {W} {H}" style="border-radius:12px;display:block;margin:8px 0">',
        f'<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="#c62828"/>',
        f'<rect x="12" y="12" width="{W-24}" height="{H-24}" rx="6" fill="#1565c0"/>',
        f'<circle cx="{W/2}" cy="{H/2}" r="28" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>',
        f'<circle cx="{W/2}" cy="{H/2}" r="3" fill="rgba(255,255,255,0.8)"/>',
        f'<line x1="{W/2}" y1="12" x2="{W/2}" y2="{H-12}" stroke="rgba(255,255,255,0.6)" stroke-width="2"/>',
        f'<rect x="12" y="{H/2-45}" width="40" height="90" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>',
        f'<rect x="{W-52}" y="{H/2-45}" width="40" height="90" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>',
        f'<text x="{W/2}" y="32" text-anchor="middle" fill="white" font-size="14" font-weight="bold" font-family="Arial,sans-serif">{formation_name}</text>',
    ]
    for pos in positions:
        px = 12 + (pos["x"] / 100) * (W - 24)
        py = 12 + (pos["y"] / 100) * (H - 24)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="14" fill="#c62828" stroke="white" stroke-width="2"/>')
        parts.append(f'<text x="{px:.1f}" y="{py+4:.1f}" text-anchor="middle" fill="white" font-size="10" font-weight="bold" font-family="Arial,sans-serif">{pos["label"]}</text>')
    parts.append("</svg>")
    return " ".join(parts)


# ==========================================
# PNG RENDERER
# ==========================================
def _load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def render_teams_png(teams, team_formations, team_uniforms, roles_map, ratings, match_info=None):
    def get_rating(p):
        return ratings.get(p, 50)

    def draw_pitch(draw, x, y, w, h, formation_name):
        form = FORMATIONS.get(formation_name, {})
        positions = form.get("positions", [])
        draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill="#c62828")
        pad = 8
        px0, py0 = x + pad, y + pad
        pw, ph = w - 2 * pad, h - 2 * pad
        draw.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=5, fill="#1565c0")
        cx, cy = px0 + pw // 2, py0 + ph // 2
        draw.line([(cx, py0), (cx, py0 + ph)], fill="#8fb3e0", width=2)
        r = max(10, min(pw, ph) // 7)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline="#b9d0ee", width=2)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill="white")
        bw, bh = max(14, pw // 10), max(28, ph // 2)
        draw.rectangle([px0, cy - bh // 2, px0 + bw, cy + bh // 2], outline="#8fb3e0", width=1)
        draw.rectangle([px0 + pw - bw, cy - bh // 2, px0 + pw, cy + bh // 2], outline="#8fb3e0", width=1)
        gw, gh = 5, max(12, ph // 5)
        draw.rectangle([x + 2, cy - gh // 2, x + 2 + gw, cy + gh // 2], outline="white", width=2)
        draw.rectangle([x + w - 2 - gw, cy - gh // 2, x + w - 2, cy + gh // 2], outline="white", width=2)
        title_font = _load_font(11, bold=True)
        title = formation_name if len(formation_name) <= 22 else formation_name[:20] + ".."
        try:
            bbox = draw.textbbox((0, 0), title, font=title_font)
            tw = bbox[2] - bbox[0]
        except Exception:
            tw = len(title) * 6
        draw.text((cx - tw // 2, py0 + 4), title, fill="white", font=title_font)
        dot_r = max(8, min(pw, ph) // 14)
        label_font = _load_font(9, bold=True)
        for pos in positions:
            dx = px0 + int(pos["x"] / 100 * pw)
            dy = py0 + int(pos["y"] / 100 * ph)
            draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r],
                         fill="#c62828", outline="white", width=2)
            lab = pos["label"]
            try:
                bb = draw.textbbox((0, 0), lab, font=label_font)
                lw = bb[2] - bb[0]
            except Exception:
                lw = len(lab) * 5
            draw.text((dx - lw // 2, dy - 5), lab, fill="white", font=label_font)

    margin, card_pad = 24, 16
    col_w, row_h, pitch_h = 540, 28, 150
    pitch_w = col_w - 28
    header_block = 52 + 40 + pitch_h + 12
    gap = 20
    card_heights = [header_block + (len(t) + 1) * row_h + card_pad + 8 for t in teams]
    n = len(teams)
    cols = 1 if n == 1 else 2
    rows_cards = (n + cols - 1) // cols
    row_heights = []
    for r in range(rows_cards):
        hs = [card_heights[r * cols + c] for c in range(cols) if r * cols + c < n]
        row_heights.append(max(hs) if hs else 0)

    top_banner, balance_h = 80, 50
    img_w = margin * 2 + cols * col_w + (cols - 1) * gap
    img_h = margin + top_banner + sum(row_heights) + (rows_cards - 1) * gap + balance_h + margin
    img = Image.new("RGB", (img_w, img_h), "#0a1a3a")
    draw = ImageDraw.Draw(img)

    font_title = _load_font(26, bold=True)
    font_sub = _load_font(13)
    font_h = _load_font(18, bold=True)
    font_row = _load_font(13)
    font_row_b = _load_font(13, bold=True)
    font_small = _load_font(11)

    # Top banner
    draw.rectangle([0, 0, img_w, top_banner], fill="#0d2350")
    draw.rectangle([0, 0, img_w, 4], fill="#fbbf24")
    draw.text((margin, 16), "BIAENERGI FUTSAL ACADEMY", fill="#fbbf24", font=font_title)
    subtitle = "Hasil Pembagian Tim"
    if match_info:
        subtitle += f"  •  {match_info.get('tanggal', '')}  •  {match_info.get('lokasi', '')}"
    draw.text((margin, 50), subtitle, fill="#94a3b8", font=font_sub)

    totals = []
    y_base = margin + top_banner - 8
    for idx, team in enumerate(teams):
        r, c = divmod(idx, cols)
        x0 = margin + c * (col_w + gap)
        y0 = y_base + sum(row_heights[:r]) + r * gap
        ch = card_heights[idx]
        uniform = team_uniforms[idx]
        formation = team_formations[idx]
        form_info = FORMATIONS.get(formation, {})
        team_rating = sum(get_rating(p) for p in team)
        totals.append(team_rating)
        bg = COLOR_MAP.get(uniform, "#757575")
        text_color = "white" if uniform in DARK_UNIFORMS else "black"

        draw.rounded_rectangle([x0, y0, x0 + col_w, y0 + ch], radius=12, fill="white", outline=bg, width=3)
        draw.rounded_rectangle([x0, y0, x0 + col_w, y0 + 44], radius=12, fill=bg)
        draw.rectangle([x0, y0 + 28, x0 + col_w, y0 + 44], fill=bg)
        draw.text((x0 + 14, y0 + 10), f"TEAM {idx+1}  ·  {uniform}", fill=text_color, font=font_h)

        badge = f"Σ {team_rating}"
        bw = 60
        draw.rounded_rectangle([x0 + col_w - bw - 12, y0 + 10, x0 + col_w - 12, y0 + 34],
                               radius=10, fill="#37474f")
        draw.text((x0 + col_w - bw - 4, y0 + 13), badge, fill="white", font=font_small)

        y = y0 + 52
        draw.text((x0 + 14, y), f"Formasi: {formation}", fill="#222", font=font_row_b)
        y += 18
        pola = form_info.get("pola", "")
        if len(pola) > 72:
            pola = pola[:69] + "..."
        draw.text((x0 + 14, y), pola, fill="#555", font=font_small)
        y += 20
        draw_pitch(draw, x0 + 14, y, pitch_w, pitch_h, formation)
        y += pitch_h + 10

        # Table header
        draw.rectangle([x0 + 10, y, x0 + col_w - 10, y + row_h], fill=bg)
        draw.text((x0 + 18, y + 6), "No", fill=text_color, font=font_small)
        draw.text((x0 + 50, y + 6), "Nama Pemain", fill=text_color, font=font_small)
        draw.text((x0 + 320, y + 6), "Role", fill=text_color, font=font_small)
        draw.text((x0 + 420, y + 6), "OVR", fill=text_color, font=font_small)
        y += row_h

        for j, player in enumerate(team, 1):
            if j % 2 == 0:
                draw.rectangle([x0 + 10, y, x0 + col_w - 10, y + row_h], fill="#f0f4f8")
            pr = roles_map.get(player, [])
            role_str = ", ".join(pr) if pr else "-"
            if len(role_str) > 22:
                role_str = role_str[:20] + ".."
            draw.text((x0 + 18, y + 6), str(j), fill="#333", font=font_row)
            draw.text((x0 + 50, y + 6), player, fill="#111", font=font_row_b)
            draw.text((x0 + 320, y + 6), role_str, fill="#444", font=font_row)
            draw.text((x0 + 425, y + 6), str(get_rating(player)), fill="#0d47a1", font=font_row_b)
            y += row_h

    if totals:
        mx, mn = max(totals), min(totals)
        gap_v = mx - mn
        if gap_v <= 3:
            status, color = "Imbang", "#22c55e"
        elif gap_v <= 6:
            status, color = "Cukup imbang", "#f59e0b"
        else:
            status, color = "Kurang imbang", "#ef4444"
        summary = "  |  ".join(f"Team {i+1}: {t}" for i, t in enumerate(totals))
        fy = img_h - margin - 36
        draw.rounded_rectangle([margin, fy, img_w - margin, fy + 36], radius=8, fill="#1e293b")
        draw.rectangle([margin, fy, margin + 6, fy + 36], fill=color)
        draw.text((margin + 16, fy + 9),
                  f"Keseimbangan: {summary}   →  Selisih {gap_v}  ({status})",
                  fill="#f8fafc", font=font_sub)

    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


# ==========================================
# UI COMPONENTS
# ==========================================
def render_navbar():
    st.markdown("""
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
    """, unsafe_allow_html=True)


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
        <div class='bng-hero-quote'>"Pantang menyerah meski skor tidak berpihak."</div>
        <div class='bng-hero-sub'>Never give up, even when the score isn't on our side.</div>
      </div>
      <div class='bng-hero-tag'>
        <span class='t1'>Play</span>
        <span class='t2'>Learn</span>
        <span class='t3'>Grow</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(icon, title, subtitle=""):
    sub = f"<div class='sub'>{subtitle}</div>" if subtitle else ""
    st.markdown(f"""
    <div class='bng-section'>
      <span class='icon'>{icon}</span>
      <div><h2>{title}</h2>{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(icon, value, label):
    return f"""
    <div class='bng-stat-card'>
      <div class='bng-stat-icon'>{icon}</div>
      <div class='bng-stat-value'>{value}</div>
      <div class='bng-stat-label'>{label}</div>
    </div>
    """


def attribute_card(icon, name, value, color):
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


def player_card(player):
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


def placeholder_box(emoji, title, desc):
    st.markdown(f"""
    <div class='bng-placeholder bng-animate'>
      <div class='emoji'>{emoji}</div>
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE: HOME
# ==========================================
def page_home():
    render_hero()
    players = load_players()
    total_players = len(players)
    total_roles = sum(len(p.get("roles", [])) for p in players)
    highest_ovr = max((p.get("overall", 0) for p in players), default=0)
    matches = store.get_match_history()
    total_matches = len(matches)

    section_header("👥", "Our Team at a Glance", "Statistik singkat tim BIAENERGI")
    stats = [
        stat_card("👥", total_players, "Total Players"),
        stat_card("🎯", "GK·A·F·P", "Player Positions"),
        stat_card("⭐", highest_ovr, "Highest Overall Rating"),
        stat_card("🏆", total_matches, "Match Played"),
    ]
    st.markdown(f"<div class='bng-stat-grid bng-animate'>{''.join(stats)}</div>",
                unsafe_allow_html=True)

    section_header("📊", "Player Attributes",
                   f"Average Team Stats — Berdasarkan {total_players} pemain")
    if players:
        def avg_of(cols):
            total, count = 0, 0
            for p in players:
                for c in cols:
                    v = p.get("attributes", {}).get(c)
                    if isinstance(v, (int, float)):
                        total += v
                        count += 1
            return total / count if count else 0

        attr_groups = [
            ("Speed",    "🏃", ["STA", "AKS", "SPR", "AGI"], "#3b82f6"),
            ("Shooting", "🎯", ["SHA", "SHP"],               "#ef4444"),
            ("Defense",  "🛡️", ["TAC", "STR", "BAL"],        "#22c55e"),
            ("Tactics",  "🧠", ["VIS", "OFB", "DEC"],        "#a855f7"),
            ("Teamwork", "🤝", ["TMW", "COM"],               "#f59e0b"),
            ("Mood",     "😊", ["BRV", "AGR"],               "#fbbf24"),
        ]
        cards = [attribute_card(icon, name, avg_of(cols), color)
                 for name, icon, cols, color in attr_groups]
        st.markdown(f"<div class='bng-attr-grid bng-animate'>{''.join(cards)}</div>",
                    unsafe_allow_html=True)
        st.caption(f"Berdasarkan {total_players} pemain  •  Player attributes are from our team data.")
    else:
        placeholder_box("📊", "Belum Ada Data Pemain",
                        "Tambahkan pemain di menu Team untuk melihat statistik.")


# ==========================================
# PAGE: TEAM
# ==========================================
def page_team():
    players = load_players()
    is_admin = st.session_state.is_admin

    section_header("👥", "Team Roster",
                   f"{len(players)} pemain terdaftar di database BIAENERGI")

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("🔍 Cari pemain", placeholder="Ketik nama atau alias...",
                               label_visibility="collapsed")
    with col2:
        if is_admin:
            if st.button("➕ Tambah Pemain", width="stretch", key="btn_add_player"):
                st.session_state.show_add_player = True
        else:
            if st.button("🔐 Login Admin", width="stretch", key="btn_open_login"):
                st.session_state.login_open = True
    with col3:
        if is_admin:
            if st.button("🔒 Logout", width="stretch", key="btn_logout"):
                do_logout()
                st.rerun()

    if st.session_state.flash:
        kind, msg = st.session_state.flash
        getattr(st, kind)(msg)
        st.session_state.flash = None

    if st.session_state.login_open and not is_admin:
        with st.container(border=True):
            st.markdown("#### 🔐 Login Admin")
            if st.session_state.login_attempts >= MAX_LOGIN_ATTEMPTS:
                st.error("⛔ Terlalu banyak percobaan. Refresh halaman.")
            else:
                st.text_input("Password", type="password", key="login_pw")
                c1, c2, _ = st.columns([1, 1, 3])
                if c1.button("Masuk", key="btn_do_login", type="primary", width="stretch"):
                    do_login()
                    st.rerun()
                if c2.button("Batal", key="btn_cancel_login", width="stretch"):
                    st.session_state.login_open = False
                    st.rerun()

    shown = players
    if search:
        s = search.lower()
        shown = [p for p in players if s in p["nama"].lower() or s in p.get("alias", "").lower()]

    if shown:
        cards_html = "".join(player_card(p) for p in shown)
        st.markdown(f"<div class='bng-player-grid bng-animate'>{cards_html}</div>",
                    unsafe_allow_html=True)
    else:
        placeholder_box("🔍", "Tidak Ada Pemain Ditemukan", "Coba ubah kata kunci pencarian.")

    if is_admin:
        st.markdown("---")
        section_header("✏️", "Kelola Database Pemain",
                       "Edit atribut, tambah pemain baru, atau hapus pemain")
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
                            if role_cols[i].checkbox(
                                f"{ROLE_INFO[r]['emoji']} {r} ({ROLE_INFO[r]['nama']})",
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
                                    key=f"edit_attr_{pid}_{attr}")

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

                st.markdown("**Attributes (default 50)**")
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


# ==========================================
# PAGE: TEAM GENERATOR (FASE 2)
# ==========================================
def page_team_generator():
    section_header("⚽", "Team Generator",
                   "Bagi tim secara otomatis dengan keseimbangan Overall Rating & aturan.")

    players = load_players()
    if not players:
        placeholder_box("👥", "Belum Ada Pemain",
                        "Tambahkan pemain di menu Team terlebih dahulu.")
        return

    # Stepper visual
    step_map = ["1️⃣ Pemain", "2️⃣ Rules", "3️⃣ Konfigurasi", "4️⃣ Generate", "5️⃣ Simpan"]
    st.markdown(f"""
    <div style='display:flex;gap:6px;margin:14px 0 20px 0;padding:6px;
                background:rgba(10,26,58,.6);border-radius:14px;
                border:1px solid rgba(96,165,250,.2)'>
      {''.join(f"<div style='flex:1;text-align:center;padding:8px 6px;border-radius:8px;background:rgba(251,191,36,.1);color:#fbbf24;font-weight:700;font-size:12px'>{s}</div>" for s in step_map)}
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["1️⃣ Pemain", "2️⃣ Rules", "3️⃣ Konfigurasi",
                                             "4️⃣ Generate", "5️⃣ Simpan ke History"])

    # ========== TAB 1: PILIH PEMAIN ==========
    with tab1:
        section_header("📋", "Player Selection",
                       "Pilih pemain dari database atau tambahkan pemain luar untuk sesi ini")

        all_names = [p["nama"] for p in players]
        if st.session_state.gen_selected is None:
            st.session_state.gen_selected = all_names[:]

        # Filter nama yang masih valid
        st.session_state.gen_selected = [n for n in st.session_state.gen_selected if n in all_names]

        col_a, col_b = st.columns([4, 1])
        with col_a:
            selected = st.multiselect(
                "Pilih pemain yang akan dibagi:",
                options=all_names,
                default=st.session_state.gen_selected,
                key="gen_ms_players"
            )
            st.session_state.gen_selected = list(selected)
        with col_b:
            st.write("")
            st.write("")
            if st.button("Pilih Semua", width="stretch", key="gen_sel_all"):
                st.session_state.gen_selected = all_names[:]
                st.rerun()

        st.metric("Total Pemain Terpilih", len(st.session_state.gen_selected))

        if st.session_state.gen_selected:
            sel_players = [p for p in players if p["nama"] in st.session_state.gen_selected]
            cards_html = "".join(player_card(p) for p in sel_players)
            st.markdown(f"<div class='bng-player-grid bng-animate'>{cards_html}</div>",
                        unsafe_allow_html=True)

    # ========== TAB 2: RULES ==========
    with tab2:
        section_header("⚖️", "Rules",
                       "Aturan Conflict & Uniform yang harus dipatuhi saat generate")

        rtab1, rtab2 = st.tabs(["⚔️ Separating Players", "👕 Uniform"])

        with rtab1:
            st.caption("Tentukan pasangan pemain yang **tidak boleh** berada di tim yang sama.")
            sel_names = st.session_state.gen_selected or all_names
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                p1 = st.selectbox("Pemain 1", sel_names, key="gen_rule_p1")
            with c2:
                p2 = st.selectbox("Pemain 2", sel_names, key="gen_rule_p2")
            with c3:
                st.write("")
                st.write("")
                if st.button("➕ Tambah", key="gen_add_rule", width="stretch"):
                    if p1 == p2:
                        st.error("⚠️ Pemain harus berbeda!")
                    else:
                        pair = tuple(sorted([p1, p2]))
                        if pair not in st.session_state.gen_rules:
                            st.session_state.gen_rules.append(pair)
                            st.rerun()
                        else:
                            st.warning("Rule sudah ada!")

            st.markdown(f"**Rules Conflict Aktif ({len(st.session_state.gen_rules)})**")
            if st.session_state.gen_rules:
                for i, (a, b) in enumerate(list(st.session_state.gen_rules)):
                    c1, c2 = st.columns([5, 1])
                    c1.markdown(f"**{i+1}.** {a} ⚔️ {b}")
                    if c2.button("🗑️", key=f"gen_del_rule_{i}"):
                        st.session_state.gen_rules.remove((a, b))
                        st.rerun()
            else:
                st.info("Belum ada aturan conflict.")

        with rtab2:
            st.caption("Tentukan pemain yang **hanya boleh** memakai uniform tertentu. "
                       "Jika kosong, pemain bebas memakai seragam apa pun.")
            sel_names = st.session_state.gen_selected or all_names

            c1, c2 = st.columns([3, 2])
            with c1:
                sel_player = st.selectbox("Pemain", sel_names, key="gen_uni_player")
            with c2:
                current = st.session_state.gen_uniform_rules.get(sel_player, [])
                allowed = st.multiselect("Uniform yang diizinkan", UNIFORM_OPTIONS,
                                         default=current, key="gen_uni_allowed")
            cbtn1, cbtn2 = st.columns([1, 1])
            with cbtn1:
                if st.button("💾 Simpan Aturan", width="stretch", key="gen_save_uni"):
                    if allowed:
                        st.session_state.gen_uniform_rules[sel_player] = list(allowed)
                        st.success(f"✅ Aturan uniform untuk {sel_player} disimpan.")
                    else:
                        st.session_state.gen_uniform_rules.pop(sel_player, None)
                        st.info(f"ℹ️ Aturan {sel_player} dihapus (bebas).")
                    st.rerun()
            with cbtn2:
                if st.button("🗑️ Hapus Aturan", width="stretch", key="gen_del_uni"):
                    if sel_player in st.session_state.gen_uniform_rules:
                        del st.session_state.gen_uniform_rules[sel_player]
                        st.success(f"✅ Aturan {sel_player} dihapus.")
                        st.rerun()
                    else:
                        st.warning("Tidak ada aturan untuk pemain ini.")

            st.markdown(f"**Aturan Uniform Aktif ({len(st.session_state.gen_uniform_rules)})**")
            if st.session_state.gen_uniform_rules:
                for player, unis in list(st.session_state.gen_uniform_rules.items()):
                    c1, c2, c3 = st.columns([3, 4, 1])
                    c1.markdown(f"**{player}**")
                    badges = " ".join(
                        f"<span style='display:inline-block;padding:2px 10px;margin:2px;"
                        f"border-radius:6px;font-size:11px;font-weight:700;"
                        f"background:{COLOR_MAP.get(u, '#757575')};"
                        f"color:{'white' if u in DARK_UNIFORMS else 'black'}'>{u}</span>"
                        for u in unis
                    )
                    c2.markdown(badges, unsafe_allow_html=True)
                    if c3.button("🗑️", key=f"gen_del_uni_{player}"):
                        del st.session_state.gen_uniform_rules[player]
                        st.rerun()
            else:
                st.info("Belum ada aturan uniform.")

    # ========== TAB 3: KONFIGURASI ==========
    with tab3:
        section_header("⚙️", "Team Configuration",
                       "Atur jumlah tim dan warna seragam tiap tim")

        num_teams = st.slider("Jumlah Tim", 2, 6, int(st.session_state.gen_num_teams), step=1)
        st.session_state.gen_num_teams = num_teams

        st.markdown("**🎨 Pilih Seragam tiap Tim**")
        saved = st.session_state.gen_team_uniforms
        new_uniforms = []
        cols = st.columns(min(num_teams, 3))
        for i in range(num_teams):
            default = (saved[i] if i < len(saved) and saved[i] in UNIFORM_OPTIONS
                       else UNIFORM_OPTIONS[i % len(UNIFORM_OPTIONS)])
            with cols[i % len(cols)]:
                uni = st.selectbox(f"Team {i+1}", UNIFORM_OPTIONS,
                                   index=UNIFORM_OPTIONS.index(default),
                                   key=f"gen_uni_{i}")
                new_uniforms.append(uni)
        st.session_state.gen_team_uniforms = new_uniforms

        if len(set(new_uniforms)) < len(new_uniforms):
            st.warning("⚠️ Ada tim dengan warna seragam yang sama.")

        # Validasi uniform rules
        uni_rules = st.session_state.gen_uniform_rules
        if uni_rules:
            conflicts = []
            for player, allowed in uni_rules.items():
                if player in (st.session_state.gen_selected or []):
                    if not any(u in allowed for u in new_uniforms):
                        conflicts.append(player)
            if conflicts:
                st.error(f"⚠️ **Aturan Uniform Tidak Terpenuhi:** {', '.join(conflicts)}. "
                         f"Pastikan salah satu tim menggunakan uniform yang diizinkan.")
            else:
                st.success("✅ Semua aturan uniform dapat dipenuhi konfigurasi tim ini.")

        num_sel = len(st.session_state.gen_selected or [])
        per_team = num_sel // num_teams if num_teams else 0
        sisa = num_sel % num_teams if num_teams else 0
        st.info(f"📊 **Total Pemain:** {num_sel} | **Rata-rata per Tim:** ~{per_team} | **Sisa:** {sisa}")

    # ========== TAB 4: GENERATE ==========
    with tab4:
        section_header("🎲", "Generate Team",
                       "Bagi tim otomatis dengan balancing Overall Rating")

        sel = st.session_state.gen_selected or []
        if not sel:
            placeholder_box("👥", "Belum Ada Pemain Terpilih",
                            "Pilih pemain di tab 1 terlebih dahulu.")
        elif len(sel) < st.session_state.gen_num_teams:
            st.error(f"⚠️ Jumlah pemain ({len(sel)}) kurang dari jumlah tim "
                     f"({st.session_state.gen_num_teams}). Ubah di tab 3.")
        else:
            roles_map = {}
            ratings_map = {}
            for p in players:
                if p["nama"] in sel:
                    roles_map[p["nama"]] = p["roles"]
                    ratings_map[p["nama"]] = p["overall"]

            gk_count = sum(1 for p in players
                           if p["nama"] in sel and "GK" in p["roles"])
            if gk_count == 0:
                st.warning("⚠️ Belum ada pemain berole GK di daftar terpilih.")
            elif gk_count < st.session_state.gen_num_teams:
                st.info(f"ℹ️ GK ({gk_count}) lebih sedikit dari jumlah tim "
                        f"({st.session_state.gen_num_teams}).")

            if st.button("🎲 GENERATE TIM SEKARANG", type="primary", width="stretch",
                         key="gen_do"):
                with st.spinner("Sedang mengacak & menyeimbangkan tim..."):
                    teams, team_formations, team_uniforms = generate_teams_v2(
                        sel, roles_map, ratings_map,
                        st.session_state.gen_rules,
                        st.session_state.gen_num_teams,
                        st.session_state.gen_team_uniforms,
                        st.session_state.gen_uniform_rules,
                    )
                    png_bytes = render_teams_png(
                        teams, team_formations, team_uniforms,
                        roles_map, ratings_map
                    )
                    st.session_state.gen_result = {
                        "teams": teams,
                        "formations": team_formations,
                        "uniforms": team_uniforms,
                        "roles_map": roles_map,
                        "ratings_map": ratings_map,
                        "png": png_bytes,
                        "timestamp": datetime.now().isoformat(),
                    }
                st.balloons()
                st.toast("✅ Tim berhasil dibagi!", icon="🏆")

            # Tampilkan hasil
            if st.session_state.gen_result:
                res = st.session_state.gen_result
                st.markdown("---")
                for i, team in enumerate(res["teams"]):
                    uni = res["uniforms"][i]
                    form = res["formations"][i]
                    bg = COLOR_MAP.get(uni, "#757575")
                    txt = "white" if uni in DARK_UNIFORMS else "black"
                    team_rating = sum(res["ratings_map"].get(p, 50) for p in team)
                    form_info = FORMATIONS.get(form, {})

                    st.markdown(f"""
                    <div class='bng-team-card' style='border-color:{bg}'>
                      <div class='bng-team-header'>
                        <div class='bng-team-title'>
                          🏅 TEAM {i+1}
                          <span class='bng-team-uniform'
                                style='background:{bg};color:{txt}'>{uni}</span>
                        </div>
                        <span class='bng-team-rating'>Σ Rating: {team_rating}</span>
                      </div>
                      <div class='bng-team-meta'>
                        <b>📐 Formasi:</b> {form} — <i>{form_info.get('pola', '')}</i><br>
                        <span style='color:#94a3b8;font-size:12px'>{form_info.get('karakter', '')}</span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Pitch SVG
                    st.markdown(formation_svg(form, width=340, height=200),
                                unsafe_allow_html=True)

                    # Tabel pemain
                    df_rows = []
                    for j, pl in enumerate(team, 1):
                        pr = res["roles_map"].get(pl, [])
                        df_rows.append({
                            "No": j,
                            "Pemain": pl,
                            "Role": ", ".join(pr) if pr else "-",
                            "Overall": res["ratings_map"].get(pl, 50),
                        })
                    st.dataframe(pd.DataFrame(df_rows), hide_index=True, width="stretch")

                # Summary
                totals = [sum(res["ratings_map"].get(p, 50) for p in t) for t in res["teams"]]
                mx, mn = max(totals), min(totals)
                gap = mx - mn
                color = "#22c55e" if gap <= 3 else ("#f59e0b" if gap <= 6 else "#ef4444")
                status = ("✅ Imbang" if gap <= 3 else
                          "⚠️ Cukup imbang" if gap <= 6 else "❌ Kurang imbang")
                summary = " | ".join(f"Team {i+1}: {t}" for i, t in enumerate(totals))
                st.markdown(f"""
                <div style='padding:14px 18px;border-radius:14px;margin-top:16px;
                            background:rgba(10,26,58,.6);border-left:5px solid {color}'>
                  <b>⚖️ Keseimbangan:</b> {summary} → Selisih: <b style='color:{color}'>{gap}</b> {status}
                </div>
                """, unsafe_allow_html=True)

                st.download_button(
                    label="⬇️ Download PNG Hasil Generate",
                    data=res["png"],
                    file_name=f"pembagian_tim_{datetime.now().strftime('%Y%m%d_%H%M')}.png",
                    mime="image/png",
                    width="stretch",
                    key="gen_dl_png",
                )

    # ========== TAB 5: SIMPAN KE MATCH HISTORY ==========
    with tab5:
        section_header("💾", "Simpan ke Match History",
                       "Simpan hasil generate sebagai riwayat pertandingan")

        if not st.session_state.gen_result:
            placeholder_box("🎲", "Belum Ada Hasil Generate",
                            "Generate tim di tab 4 terlebih dahulu.")
        else:
            with st.form("form_save_match"):
                c1, c2 = st.columns(2)
                with c1:
                    tanggal = st.date_input("Tanggal Match", value=datetime.now().date())
                    lokasi = st.text_input("Lokasi", placeholder="Contoh: Lapangan XYZ")
                with c2:
                    waktu = st.time_input("Waktu", value=datetime.now().time())
                    catatan = st.text_input("Catatan (opsional)", placeholder="Contoh: Friendly match")

                submitted = st.form_submit_button("💾 Simpan ke Match History",
                                                  type="primary", width="stretch")
                if submitted:
                    res = st.session_state.gen_result
                    matches = store.get_match_history()
                    mid = f"M{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    match_record = {
                        "match_id": mid,
                        "tanggal": tanggal.isoformat(),
                        "waktu": waktu.strftime("%H:%M"),
                        "lokasi": lokasi,
                        "catatan": catatan,
                        "teams": [
                            {
                                "nama": f"Team {i+1}",
                                "uniform": res["uniforms"][i],
                                "formasi": res["formations"][i],
                                "players": list(res["teams"][i]),
                                "rating_total": sum(res["ratings_map"].get(p, 50)
                                                    for p in res["teams"][i]),
                            }
                            for i in range(len(res["teams"]))
                        ],
                        "skor": {f"team{i+1}": 0 for i in range(len(res["teams"]))},
                        "created_at": datetime.now().isoformat(),
                    }
                    matches.append(match_record)
                    if store.save_match_history(matches):
                        st.success(f"✅ Match {mid} berhasil disimpan ke Match History.")
                        st.session_state.gen_result = None
                        st.session_state.flash = ("success",
                            f"✅ Match {mid} tersimpan. Buka tab Match History untuk mengisi skor.")
                        st.rerun()
                    else:
                        st.error("⚠️ Gagal menyimpan match.")


# ==========================================
# PAGE: MATCH HISTORY (FASE 3)
# ==========================================
def page_match_history():
    section_header("📜", "Match History",
                   "Riwayat pertandingan yang sudah digenerate & disimpan")

    matches = store.get_match_history()

    if not matches:
        placeholder_box("📭", "Belum Ada Riwayat Match",
                        "Generate tim di menu Team Generator, lalu simpan hasilnya ke Match History.")
        return

    st.metric("Total Match Tersimpan", len(matches))

    # Sort terbaru di atas
    matches_sorted = sorted(matches, key=lambda m: m.get("created_at", ""), reverse=True)

    for idx, match in enumerate(matches_sorted):
        mid = match["match_id"]
        tanggal = match.get("tanggal", "-")
        waktu = match.get("waktu", "")
        lokasi = match.get("lokasi", "-")
        catatan = match.get("catatan", "")
        teams = match.get("teams", [])
        skor = match.get("skor", {})

        # Header match
        st.markdown(f"""
        <div class='bng-match-card bng-animate'>
          <div class='bng-match-header'>
            <div>
              <span class='bng-match-id'>🏆 {mid}</span>
              <span class='bng-match-date' style='margin-left:10px'>
                📅 {tanggal} {waktu} · 📍 {lokasi}
              </span>
            </div>
            <span style='color:#94a3b8;font-size:12px'>{catatan}</span>
          </div>
        """, unsafe_allow_html=True)

        # Score display
        if len(teams) >= 2:
            t1 = teams[0]
            t2 = teams[1]
            s1 = skor.get("team1", 0)
            s2 = skor.get("team2", 0)
            bg1 = COLOR_MAP.get(t1["uniform"], "#757575")
            bg2 = COLOR_MAP.get(t2["uniform"], "#757575")
            st.markdown(f"""
            <div class='bng-match-score'>
              <div class='bng-match-team'>
                <div class='name'>{t1['nama']}</div>
                <div class='uniform'>
                  <span style='display:inline-block;width:12px;height:12px;border-radius:50%;
                               background:{bg1};vertical-align:middle;margin-right:4px'></span>
                  {t1['uniform']} · {t1['formasi']}
                </div>
              </div>
              <div class='bng-match-score-num'>{s1} — {s2}</div>
              <div class='bng-match-team'>
                <div class='name'>{t2['nama']}</div>
                <div class='uniform'>
                  <span style='display:inline-block;width:12px;height:12px;border-radius:50%;
                               background:{bg2};vertical-align:middle;margin-right:4px'></span>
                  {t2['uniform']} · {t2['formasi']}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Form input skor & detail
        with st.expander(f"📝 Input Skor & Detail — {mid}", expanded=False):
            with st.form(f"form_match_{mid}"):
                st.markdown("**Input Skor:**")
                score_cols = st.columns(len(teams))
                new_skor = {}
                for i, team in enumerate(teams):
                    with score_cols[i]:
                        val = st.number_input(
                            f"{team['nama']} ({team['uniform']})",
                            min_value=0, max_value=99,
                            value=int(skor.get(f"team{i+1}", 0)),
                            key=f"score_{mid}_t{i+1}"
                        )
                        new_skor[f"team{i+1}"] = val

                st.markdown("**Info Match:**")
                c1, c2 = st.columns(2)
                with c1:
                    new_tanggal = st.date_input(
                        "Tanggal",
                        value=datetime.fromisoformat(match["tanggal"]).date()
                        if match.get("tanggal") else datetime.now().date(),
                        key=f"date_{mid}"
                    )
                    new_lokasi = st.text_input("Lokasi", value=lokasi, key=f"lok_{mid}")
                with c2:
                    try:
                        default_time = datetime.strptime(waktu, "%H:%M").time()
                    except Exception:
                        default_time = datetime.now().time()
                    new_waktu = st.time_input("Waktu", value=default_time, key=f"time_{mid}")
                    new_catatan = st.text_input("Catatan", value=catatan, key=f"cat_{mid}")

                cbtn1, cbtn2 = st.columns([1, 1])
                save_score = cbtn1.form_submit_button("💾 Simpan Skor", type="primary",
                                                       width="stretch")
                delete_match = cbtn2.form_submit_button("🗑️ Hapus Match", width="stretch")

                if save_score:
                    for m in matches:
                        if m["match_id"] == mid:
                            m["skor"] = new_skor
                            m["tanggal"] = new_tanggal.isoformat()
                            m["waktu"] = new_waktu.strftime("%H:%M")
                            m["lokasi"] = new_lokasi
                            m["catatan"] = new_catatan
                            break
                    if store.save_match_history(matches):
                        st.success("✅ Skor & info match diperbarui.")
                        st.rerun()

                if delete_match:
                    matches = [m for m in matches if m["match_id"] != mid]
                    if store.save_match_history(matches):
                        st.warning(f"🗑️ Match {mid} dihapus.")
                        st.rerun()

            # Detail tim
            st.markdown("**Detail Tim:**")
            for i, team in enumerate(teams):
                with st.container(border=True):
                    st.markdown(f"**{team['nama']}** — Uniform: {team['uniform']} · "
                                f"Formasi: {team['formasi']} · Σ Rating: {team.get('rating_total', 0)}")
                    players_list = team.get("players", [])
                    roles_map_local = {}
                    for pl_name in players_list:
                        pl_obj = next((p for p in load_players() if p["nama"] == pl_name), None)
                        roles_map_local[pl_name] = pl_obj["roles"] if pl_obj else []
                    df_rows = []
                    for j, pl_name in enumerate(players_list, 1):
                        df_rows.append({
                            "No": j,
                            "Pemain": pl_name,
                            "Role": ", ".join(roles_map_local.get(pl_name, [])) or "-",
                        })
                    st.dataframe(pd.DataFrame(df_rows), hide_index=True, width="stretch")


# ==========================================
# PAGE: ABOUT
# ==========================================
def page_about():
    section_header("ℹ️", "Tentang BIAENERGI Futsal Academy",
                   "One Team, One Spirit — Play, Learn, Grow Together")

    col1, col2 = st.columns([1, 1])
    with col1:
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
    with col2:
        st.markdown("""
        ### 🎯 Visi
        Menjadi akademi futsal yang membangun karakter, sportivitas,
        dan skill pemain melalui pendekatan seimbang antara **Play, Learn, Grow**.

        ### 🧭 Misi
        - Mengembangkan skill teknis & taktik setiap pemain
        - Membangun kekompakan tim melalui latihan rutin
        - Menjunjung tinggi sportivitas di setiap pertandingan
        - Menciptakan lingkungan positif & menyenangkan

        ### 💬 Filosofi
        > *"Pantang menyerah meski skor tidak berpihak."*
        >
        > — Never give up, even when the score isn't on our side.
        """)


# ==========================================
# MAIN
# ==========================================
def main():
    render_navbar()

    tabs = st.tabs([
        "🏠 Home",
        "👥 Team",
        "⚽ Team Generator",
        "📜 Match History",
        "ℹ️ About",
    ])

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