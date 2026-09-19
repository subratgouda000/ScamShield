import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from analyzer import analyze_message
import random
import string
from datetime import datetime, timezone

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ScamShield | AI Security Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# DEMO MESSAGES
# =========================================================

DEMO_MESSAGES = {
    "scam": """URGENT! Your bank account will be blocked today.
Verify your account immediately by clicking this link and entering your OTP:
http://example.com""",
    "legitimate": """Your Amazon order #402-7812345-6789012 has been shipped.
It will arrive on September 22.
Track your package through the Amazon app.""",
    "url": "http://secure-bank-login.example.com/verify",
}

# =========================================================
# SESSION STATE
# =========================================================

if "message_box" not in st.session_state:
    st.session_state.message_box = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "is_analyzing" not in st.session_state:
    st.session_state.is_analyzing = False
if "scan_id" not in st.session_state:
    st.session_state.scan_id = None
if "scan_time" not in st.session_state:
    st.session_state.scan_time = None
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0
if "last_scan_time" not in st.session_state:
    st.session_state.last_scan_time = None

# =========================================================
# CALLBACKS
# =========================================================

def select_demo(name):
    st.session_state.message_box = DEMO_MESSAGES[name]
    st.session_state.analysis_result = None
    st.session_state.is_analyzing = False
    st.session_state.scan_id = None
    st.session_state.scan_time = None

def reset_all():
    st.session_state.message_box = ""
    st.session_state.analysis_result = None
    st.session_state.is_analyzing = False
    st.session_state.scan_id = None
    st.session_state.scan_time = None
    st.session_state.scan_count = 0
    st.session_state.last_scan_time = None

def generate_scan_id():
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"#{part1}-{part2}"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* =====================================================
       KILL STREAMLIT'S DEFAULT TOP PADDING
    ===================================================== */
    [data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
    [data-testid="stHeader"] { display: none !important; height: 0 !important; }
    section.main > div { padding-top: 0 !important; }
    .stApp > header { display: none !important; }

    /* =====================================================
       MAIN BACKGROUND
    ===================================================== */
    .stApp {
        background-color: #0B0F19;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59, 130, 246, 0.15), transparent),
            radial-gradient(ellipse 60% 50% at 80% 100%, rgba(139, 92, 246, 0.08), transparent);
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 0.25rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .main {
        background-image:
            linear-gradient(rgba(59, 130, 246, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59, 130, 246, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* =====================================================
       NAVBAR
    ===================================================== */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(55, 65, 81, 0.5);
        margin-bottom: 0.75rem;
    }
    .brand {
        font-size: 1.3rem;
        font-weight: 800;
        color: #F9FAFB;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: -0.03em;
    }
    .brand-icon { filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.8)); }
    .badge {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        color: #60A5FA;
        background: rgba(59, 130, 246, 0.08);
        padding: 0.35rem 0.85rem;
        border-radius: 6px;
        border: 1px solid rgba(59, 130, 246, 0.25);
        font-family: 'JetBrains Mono', monospace;
        white-space: nowrap;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .live-dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #10B981; box-shadow: 0 0 8px #10B981;
        animation: pulseGlow 1.5s ease-in-out infinite;
    }

    /* =====================================================
       SESSION STATS TICKER (single line, no wrap)
    ===================================================== */
    .ticker-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.75rem;
        flex-wrap: nowrap;
        margin: 0.5rem auto 1rem auto;
        padding: 0.55rem 1.25rem;
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(55, 65, 81, 0.6);
        border-radius: 999px;
        width: fit-content;
        max-width: 100%;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.08em;
        animation: fadeIn 0.8s ease;
        white-space: nowrap;
        overflow-x: auto;
        scrollbar-width: none;
    }
    .ticker-wrap::-webkit-scrollbar { display: none; }
    .ticker-item {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        color: #9CA3AF;
        white-space: nowrap;
        flex-shrink: 0;
    }
    .ticker-item .num {
        color: #F87171;
        font-weight: 700;
        text-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
    }
    .ticker-item .num.green {
        color: #34D399;
        text-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
    }
    .ticker-divider { color: #374151; }

    /* =====================================================
       HERO
    ===================================================== */
    .hero {
        text-align: center;
        margin-bottom: 1.25rem;
    }
    .hero h1 {
        font-size: 2.35rem;
        font-weight: 900;
        color: #F9FAFB;
        letter-spacing: -0.04em;
        margin-bottom: 0.4rem;
        line-height: 1.1;
    }
    .hero p {
        font-size: 0.88rem;
        color: #9CA3AF;
        max-width: 640px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* =====================================================
       PANEL HEADERS
    ===================================================== */
    .panel-label {
        font-size: 0.7rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.2em;
        color: #60A5FA;
        text-transform: uppercase;
        margin-bottom: 0.65rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(59, 130, 246, 0.2);
    }
    .panel-label .dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #3B82F6; box-shadow: 0 0 8px #3B82F6;
    }

    /* =====================================================
       SAMPLE BUTTONS
    ===================================================== */
    .sample-label {
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        color: #6B7280;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }

    div[data-testid="stHorizontalBlock"] .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.72rem !important;
        padding: 0.5rem 0.35rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid rgba(55, 65, 81, 0.6) !important;
        background: rgba(17, 24, 39, 0.6) !important;
        color: #9CA3AF !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button {
        color: #F87171 !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
        background: rgba(239, 68, 68, 0.05) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button:hover {
        background: rgba(239, 68, 68, 0.12) !important;
        border-color: rgba(239, 68, 68, 0.6) !important;
        color: #FCA5A5 !important;
        transform: translateY(-2px) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button {
        color: #34D399 !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
        background: rgba(16, 185, 129, 0.05) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button:hover {
        background: rgba(16, 185, 129, 0.12) !important;
        border-color: rgba(16, 185, 129, 0.6) !important;
        color: #6EE7B7 !important;
        transform: translateY(-2px) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton button {
        color: #FBBF24 !important;
        border-color: rgba(245, 158, 11, 0.3) !important;
        background: rgba(245, 158, 11, 0.05) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton button:hover {
        background: rgba(245, 158, 11, 0.12) !important;
        border-color: rgba(245, 158, 11, 0.6) !important;
        color: #FCD34D !important;
        transform: translateY(-2px) !important;
    }

    /* =====================================================
       TEXT AREA
    ===================================================== */
    div[data-testid="stTextArea"] textarea {
        min-height: 190px !important;
        border: 1px solid rgba(55, 65, 81, 0.7) !important;
        border-radius: 12px !important;
        background: rgba(11, 15, 25, 0.7) !important;
        color: #E2E8F0 !important;
        font-size: 0.88rem !important;
        line-height: 1.65 !important;
        padding: 1rem 1.1rem !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02), 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease;
        font-family: 'JetBrains Mono', monospace;
    }
    div[data-testid="stTextArea"] textarea::placeholder {
        color: #4B5563 !important;
        font-style: italic;
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: rgba(59, 130, 246, 0.7) !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        background: rgba(11, 15, 25, 0.9) !important;
    }

    /* =====================================================
       CHARACTER COUNTER
    ===================================================== */
    .char-counter {
        text-align: right;
        font-size: 0.65rem;
        color: #4B5563;
        margin-top: 0.35rem;
        margin-bottom: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .kbd-hint {
        font-size: 0.62rem;
        color: #4B5563;
        font-family: 'JetBrains Mono', monospace;
    }

    /* =====================================================
       ANALYZE BUTTON
    ===================================================== */
    div[data-testid="stHorizontalBlock"] .analyze-btn button,
    .analyze-btn button,
    div[data-testid="column"]:nth-of-type(1) .stButton:last-of-type button {
        width: 100% !important;
        min-height: 52px !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        border: 1px solid rgba(96, 165, 250, 0.5) !important;
        color: #FFFFFF !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3) !important;
        text-transform: uppercase;
    }
    div[data-testid="stHorizontalBlock"] .analyze-btn button:hover,
    .analyze-btn button:hover,
    div[data-testid="column"]:nth-of-type(1) .stButton:last-of-type button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 40px rgba(59, 130, 246, 0.55), 0 15px 40px rgba(59, 130, 246, 0.35) !important;
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
    }

    /* =====================================================
       RESET BUTTON
    ===================================================== */
    .reset-btn button {
        width: 100% !important;
        min-height: 40px !important;
        border-radius: 10px !important;
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid rgba(55, 65, 81, 0.8) !important;
        color: #9CA3AF !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        transition: all 0.25s ease !important;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    .reset-btn button:hover {
        border-color: rgba(96, 165, 250, 0.5) !important;
        color: #60A5FA !important;
        background: rgba(59, 130, 246, 0.08) !important;
    }

    /* =====================================================
       COPY REPORT BUTTON
    ===================================================== */
    .copy-btn button {
        width: 100% !important;
        min-height: 40px !important;
        border-radius: 10px !important;
        background: rgba(16, 185, 129, 0.08) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: #6EE7B7 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        transition: all 0.25s ease !important;
        text-transform: uppercase;
        margin-top: 1rem;
    }
    .copy-btn button:hover {
        background: rgba(16, 185, 129, 0.15) !important;
        border-color: rgba(16, 185, 129, 0.6) !important;
        color: #A7F3D0 !important;
        transform: translateY(-1px) !important;
    }

    /* =====================================================
       ANIMATIONS
    ===================================================== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(59, 130, 246, 0.6); }
        50% { opacity: 0.6; box-shadow: 0 0 16px rgba(59, 130, 246, 0.9); }
    }
    @keyframes ringDraw { from { stroke-dashoffset: 440; } }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes barGrow {
        from { transform: scaleX(0); }
        to { transform: scaleX(1); }
    }

    /* =====================================================
       SCAN META BAR
    ===================================================== */
    .scan-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.85rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #6B7280;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        padding: 0.45rem 0;
        border-top: 1px dashed rgba(55, 65, 81, 0.5);
        border-bottom: 1px dashed rgba(55, 65, 81, 0.5);
        animation: fadeIn 0.5s ease;
    }
    .scan-meta .key { color: #4B5563; }
    .scan-meta .val { color: #93C5FD; font-weight: 700; }

    /* =====================================================
       VERDICT CARD
    ===================================================== */
    .verdict-card {
        padding: 1.25rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid #374151;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
        animation: fadeIn 0.5s ease;
    }
    .verdict-card.safe { border-color: rgba(16, 185, 129, 0.3); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(16, 185, 129, 0.08); }
    .verdict-card.suspicious { border-color: rgba(245, 158, 11, 0.3); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(245, 158, 11, 0.08); }
    .verdict-card.danger { border-color: rgba(239, 68, 68, 0.3); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(239, 68, 68, 0.1); }

    .verdict-icon { font-size: 2rem; line-height: 1; flex-shrink: 0; }
    .verdict-content { flex: 1; }
    .verdict-content h3 {
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.01em;
    }
    .verdict-content p {
        font-size: 0.85rem;
        margin: 0;
        color: #E2E8F0;
        line-height: 1.6;
    }
    .safe .verdict-content h3 { color: #34D399; }
    .suspicious .verdict-content h3 { color: #FBBF24; }
    .danger .verdict-content h3 { color: #F87171; }

    /* =====================================================
       SCORE RING
    ===================================================== */
    .score-ring-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0.5rem 0;
        animation: fadeIn 0.7s ease;
    }
    .score-ring {
        position: relative;
        width: 140px;
        height: 140px;
    }
    .score-ring svg { transform: rotate(-90deg); }
    .score-ring-inner {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    .score-ring-value {
        font-size: 2.25rem;
        font-weight: 900;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.03em;
    }
    .score-ring.safe .score-ring-value { color: #10B981; }
    .score-ring.suspicious .score-ring-value { color: #F59E0B; }
    .score-ring.danger .score-ring-value { color: #EF4444; }
    .score-ring-label {
        font-size: 0.55rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        color: #6B7280;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 0.3rem;
        text-transform: uppercase;
    }

    /* =====================================================
       METRICS GRID
    ===================================================== */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.6s ease;
    }
    .metric-card {
        background: rgba(17, 24, 39, 0.8);
        padding: 1rem 0.5rem;
        border-radius: 12px;
        border: 1px solid #374151;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-height: 90px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-2px); border-color: rgba(96, 165, 250, 0.4); }
    .metric-label {
        font-size: 0.55rem;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin: 0 0 0.5rem 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #F9FAFB;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.02em;
        line-height: 1;
    }
    .metric-value.risk-high { color: #EF4444; }
    .metric-value.risk-med { color: #F59E0B; }
    .metric-value.risk-low { color: #10B981; }

    .metric-card:has(.risk-high) {
        background: rgba(239, 68, 68, 0.1);
        border-color: rgba(239, 68, 68, 0.4);
    }
    .metric-card:has(.risk-med) { background: rgba(245, 158, 11, 0.08); border-color: rgba(245, 158, 11, 0.35); }
    .metric-card:has(.risk-low) { background: rgba(16, 185, 129, 0.08); border-color: rgba(16, 185, 129, 0.35); }

    /* =====================================================
       CONFIDENCE + SIGNAL BARS
    ===================================================== */
    .bars-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.7s ease;
    }
    .bar-card {
        background: rgba(17, 24, 39, 0.8);
        padding: 0.85rem 1rem;
        border-radius: 12px;
        border: 1px solid #374151;
    }
    .bar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .bar-title {
        font-size: 0.55rem;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-family: 'JetBrains Mono', monospace;
    }
    .bar-value {
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #93C5FD;
    }
    .bar-track {
        height: 5px;
        background: rgba(55, 65, 81, 0.4);
        border-radius: 3px;
        overflow: hidden;
    }
    .bar-fill {
        height: 100%;
        border-radius: 3px;
        animation: barGrow 1.2s cubic-bezier(0.4, 0, 0.2, 1);
        transform-origin: left;
    }
    .bar-fill.blue { background: linear-gradient(90deg, #3B82F6, #60A5FA); }
    .bar-fill.red { background: linear-gradient(90deg, #DC2626, #EF4444); }
    .bar-fill.amber { background: linear-gradient(90deg, #D97706, #F59E0B); }
    .bar-fill.green { background: linear-gradient(90deg, #059669, #10B981); }

    /* =====================================================
       SEVERITY TAGS
    ===================================================== */
    .tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.8s ease;
    }
    .tag {
        font-size: 0.6rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.08em;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        text-transform: uppercase;
        border: 1px solid;
        white-space: nowrap;
    }
    .tag.danger { color: #F87171; border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.08); }
    .tag.warn { color: #FBBF24; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.08); }
    .tag.safe { color: #34D399; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.08); }
    .tag.info { color: #60A5FA; border-color: rgba(59, 130, 246, 0.4); background: rgba(59, 130, 246, 0.08); }

    /* =====================================================
       SECTION TITLES
    ===================================================== */
    .section-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #F9FAFB;
        margin-bottom: 0.6rem;
        margin-top: 1.25rem;
        animation: fadeIn 0.7s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: 0.02em;
    }

    /* =====================================================
       WARNING + ACTION ITEMS
    ===================================================== */
    .warning-item {
        background: rgba(239, 68, 68, 0.06);
        border-left: 3px solid #EF4444;
        padding: 0.65rem 0.9rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.82rem;
        color: #FECACA;
        line-height: 1.55;
        animation: fadeIn 0.7s ease;
    }
    .action-item {
        background: rgba(16, 185, 129, 0.06);
        border-left: 3px solid #10B981;
        padding: 0.65rem 0.9rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.82rem;
        color: #A7F3D0;
        line-height: 1.55;
        animation: fadeIn 0.8s ease;
    }

    /* =====================================================
       EMPTY STATE
    ===================================================== */
    .empty-state {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 3rem 1rem;
        background: rgba(17, 24, 39, 0.4);
        border: 1px dashed rgba(55, 65, 81, 0.6);
        border-radius: 16px;
        min-height: 500px;
    }
    .empty-icon {
        font-size: 3rem;
        opacity: 0.3;
        margin-bottom: 1rem;
        animation: pulseGlow 3s ease-in-out infinite;
    }
    .empty-title {
        font-size: 1rem;
        font-weight: 700;
        color: #6B7280;
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.1em;
    }
    .empty-desc {
        font-size: 0.8rem;
        color: #4B5563;
        max-width: 320px;
        line-height: 1.6;
    }

    /* =====================================================
       SCANNER
    ===================================================== */
    .scanner {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 4rem 2rem;
        min-height: 500px;
    }
    .scanner-circle {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        border: 2px solid rgba(55, 65, 81, 0.4);
        border-top-color: #3B82F6;
        border-right-color: #60A5FA;
        animation: spin 0.9s linear infinite;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
    }
    .scanner-text {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.8rem;
        margin-top: 1.25rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
    }

    /* =====================================================
       FOOTER
    ===================================================== */
    .footer {
        text-align: center;
        font-size: 0.72rem;
        color: #E2E8F0;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(55, 65, 81, 0.4);
        line-height: 1.7;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.02em;
    }

    /* =====================================================
       MOBILE
    ===================================================== */
    @media (max-width: 900px) {
        .hero h1 { font-size: 1.75rem; }
        .metrics-grid { grid-template-columns: 1fr; }
        .bars-container { grid-template-columns: 1fr; }
        .navbar { flex-direction: column; gap: 0.5rem; align-items: flex-start; }
        .verdict-card { flex-direction: column; }
        .ticker-wrap { font-size: 0.58rem; padding: 0.4rem 0.75rem; gap: 0.5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# NAVBAR
# =========================================================

st.markdown(
    '<div class="navbar">'
    '<div class="brand"><span class="brand-icon">🛡️</span> ScamShield</div>'
    '<div class="badge"><span class="live-dot"></span> AI SECURITY ENGINE</div>'
    '</div>',
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATS TICKER (real data)
# =========================================================

if st.session_state.scan_count > 0:
    st.markdown(
        f'<div class="ticker-wrap">'
        f'<div class="ticker-item">📊 <span class="num green">{st.session_state.scan_count}</span> scans this session</div>'
        f'<span class="ticker-divider">|</span>'
        f'<div class="ticker-item">🕐 Last scan: <span class="num green">{st.session_state.last_scan_time}</span></div>'
        f'<span class="ticker-divider">|</span>'
        f'<div class="ticker-item">🔒 <span class="num green">LIVE</span> engine</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="ticker-wrap">'
        '<div class="ticker-item">🔒 <span class="num green">LIVE</span> AI engine ready</div>'
        '<span class="ticker-divider">|</span>'
        '<div class="ticker-item">📡 Awaiting first scan</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="hero">'
    '<h1>Check Before You Click</h1>'
    '<p>Analyze suspicious messages, links, and emails with AI. '
    'Understand the warning signs before taking action.</p>'
    '</div>',
    unsafe_allow_html=True,
)

# =========================================================
# TWO COLUMN LAYOUT
# =========================================================

left_col, right_col = st.columns([1, 1.4], gap="large")

# ---------------------------------------------------------
# LEFT COLUMN: INPUT
# ---------------------------------------------------------
with left_col:
    st.markdown(
        '<div class="panel-label"><span class="dot"></span> INPUT MESSAGE</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sample-label">▶ TRY A SAMPLE</div>', unsafe_allow_html=True)

    demo1, demo2, demo3 = st.columns(3)
    with demo1:
        st.button("🚨 Scam SMS", key="scam_demo", use_container_width=True, on_click=select_demo, args=("scam",))
    with demo2:
        st.button("✅ Legit", key="legitimate_demo", use_container_width=True, on_click=select_demo, args=("legitimate",))
    with demo3:
        st.button("🔗 URL", key="url_demo", use_container_width=True, on_click=select_demo, args=("url",))

    message = st.text_area(
        "Suspicious message",
        height=200,
        placeholder="Paste suspicious link, SMS, or email contents here for analysis...",
        label_visibility="collapsed",
        key="message_box",
    )

    st.markdown(
        f'<div class="char-counter">'
        f'<span class="kbd-hint">💡 Tip: Use the sample buttons above</span>'
        f'<span>{len(message)} CHARS</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="analyze-btn">', unsafe_allow_html=True)
    analyze_clicked = st.button(
        "⚡ Analyze Message" if not st.session_state.is_analyzing else "Analyzing...",
        key="analyze_button",
        use_container_width=True,
        disabled=st.session_state.is_analyzing
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    st.button("🔄 New Scan", key="reset_button", use_container_width=True, on_click=reset_all)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# RIGHT COLUMN: RESULTS
# ---------------------------------------------------------
with right_col:
    st.markdown(
        '<div class="panel-label"><span class="dot"></span> THREAT ANALYSIS</div>',
        unsafe_allow_html=True,
    )

    if analyze_clicked:
        if not message.strip():
            st.warning("Please enter a message, email, or URL to analyze.")
        else:
            st.session_state.is_analyzing = True
            st.session_state.analysis_result = None
            st.session_state.scan_id = generate_scan_id()
            st.session_state.scan_time = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
            st.rerun()

    if st.session_state.is_analyzing:
        st.markdown(
            '<div class="scanner">'
            '<div class="scanner-circle"></div>'
            '</div>'
            '<p class="scanner-text">SCANNING FOR SCAM SIGNALS...</p>',
            unsafe_allow_html=True,
        )
        try:
            result = analyze_message(message)
            st.session_state.analysis_result = result
            st.session_state.is_analyzing = False
            # Update REAL session stats
            st.session_state.scan_count += 1
            st.session_state.last_scan_time = datetime.now(timezone.utc).strftime("%H:%M UTC")
            st.rerun()
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.session_state.is_analyzing = False

    elif not st.session_state.analysis_result:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-icon">🔍</div>'
            '<div class="empty-title">AWAITING INPUT</div>'
            '<div class="empty-desc">Paste a suspicious message on the left and click <strong>Analyze Message</strong> to begin AI-powered threat detection.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    else:
        result = st.session_state.analysis_result

        risk_score = result.get("risk_score", 0)
        risk_level = result.get("risk_level", "UNKNOWN")
        classification = result.get("classification", "Unknown")
        warning_signs = result.get("warning_signs", [])
        explanation = result.get("explanation", "No explanation provided.")
        safe_actions = result.get("safe_actions", [])

        risk_class = "safe"
        risk_icon = "✅"
        risk_title = "Low Risk"
        risk_color_class = "risk-low"
        bar_color = "green"

        if risk_score > 70:
            risk_class = "danger"
            risk_icon = "🚨"
            risk_title = "High Risk"
            risk_color_class = "risk-high"
            bar_color = "red"
        elif risk_score > 30:
            risk_class = "suspicious"
            risk_icon = "⚠️"
            risk_title = "Suspicious"
            risk_color_class = "risk-med"
            bar_color = "amber"

        confidence = min(99, 70 + abs(risk_score - 50) // 2)

        st.markdown(
            f'<div class="scan-meta">'
            f'<span><span class="key">ID:</span> <span class="val">{st.session_state.scan_id}</span></span>'
            f'<span><span class="key">TIME:</span> <span class="val">{st.session_state.scan_time}</span></span>'
            f'<span><span class="key">ENGINE:</span> <span class="val">v2.4.1</span></span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="verdict-card {risk_class}">'
            f'<div class="verdict-icon">{risk_icon}</div>'
            f'<div class="verdict-content">'
            f'<h3>{risk_title} — {classification}</h3>'
            f'<p>{explanation}</p>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        ring_col, metrics_col = st.columns([1, 1.6], gap="medium")

        with ring_col:
            circumference = 2 * 3.14159 * 55
            ring_color = "#10B981"
            if risk_score > 70:
                ring_color = "#EF4444"
            elif risk_score > 30:
                ring_color = "#F59E0B"

            st.markdown(
                f'<div class="score-ring-wrap">'
                f'<div class="score-ring {risk_class}">'
                f'<svg width="140" height="140" viewBox="0 0 140 140">'
                f'<circle cx="70" cy="70" r="55" fill="none" stroke="rgba(55, 65, 81, 0.4)" stroke-width="8"/>'
                f'<circle cx="70" cy="70" r="55" fill="none" stroke="{ring_color}" stroke-width="8" '
                f'stroke-linecap="round" stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}" '
                f'style="animation: ringDraw 1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards; animation-delay: 0.2s;"/>'
                f'</svg>'
                f'<div class="score-ring-inner">'
                f'<div class="score-ring-value">{risk_score}</div>'
                f'<div class="score-ring-label">RISK SCORE</div>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with metrics_col:
            st.markdown(
                f'<div class="metrics-grid">'
                f'<div class="metric-card">'
                f'<div class="metric-label">RISK</div>'
                f'<div class="metric-value {risk_color_class}">{risk_score}</div>'
                f'</div>'
                f'<div class="metric-card">'
                f'<div class="metric-label">LEVEL</div>'
                f'<div class="metric-value">{risk_level}</div>'
                f'</div>'
                f'<div class="metric-card">'
                f'<div class="metric-label">CLASS</div>'
                f'<div class="metric-value">{classification}</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="bars-container">'
            f'<div class="bar-card">'
            f'<div class="bar-header">'
            f'<span class="bar-title">AI CONFIDENCE</span>'
            f'<span class="bar-value">{confidence}%</span>'
            f'</div>'
            f'<div class="bar-track"><div class="bar-fill blue" style="width:{confidence}%;"></div></div>'
            f'</div>'
            f'<div class="bar-card">'
            f'<div class="bar-header">'
            f'<span class="bar-title">THREAT SIGNAL</span>'
            f'<span class="bar-value">{risk_score}%</span>'
            f'</div>'
            f'<div class="bar-track"><div class="bar-fill {bar_color}" style="width:{risk_score}%;"></div></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        tags_html = ""
        if risk_score > 70:
            tags_html += '<span class="tag danger">⚡ HIGH SEVERITY</span>'
        elif risk_score > 30:
            tags_html += '<span class="tag warn">⚠ MEDIUM SEVERITY</span>'
        else:
            tags_html += '<span class="tag safe">✓ LOW SEVERITY</span>'

        msg_lower = message.lower()
        if any(k in msg_lower for k in ["urgent", "immediately", "today", "blocked", "verify"]):
            tags_html += '<span class="tag warn">⏱ URGENCY</span>'
        if any(k in msg_lower for k in ["http://", "https://", "click", "link"]):
            tags_html += '<span class="tag danger">🔗 EXT LINK</span>'
        if any(k in msg_lower for k in ["otp", "password", "pin", "credential", "bank"]):
            tags_html += '<span class="tag danger">🔐 CREDENTIAL REQ</span>'

        st.markdown(f'<div class="tag-row">{tags_html}</div>', unsafe_allow_html=True)

        warn_col, act_col = st.columns(2, gap="medium")

        with warn_col:
            if warning_signs:
                st.markdown(
                    '<div class="section-title">⚠️ WARNING SIGNS</div>',
                    unsafe_allow_html=True,
                )
                for warning in warning_signs:
                    st.markdown(f'<div class="warning-item">{warning}</div>', unsafe_allow_html=True)

        with act_col:
            if safe_actions:
                st.markdown(
                    '<div class="section-title">🛡️ RECOMMENDED ACTIONS</div>',
                    unsafe_allow_html=True,
                )
                for action in safe_actions:
                    st.markdown(f'<div class="action-item">{action}</div>', unsafe_allow_html=True)

        st.markdown('<div class="copy-btn">', unsafe_allow_html=True)
        if st.button("📋 Copy Full Report", key="copy_report", use_container_width=True):
            st.toast("Report ready! In a real deployment this would copy to clipboard.", icon="📋")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'ScamShield provides AI-based guidance and does not guarantee that a message is safe or malicious. '
    'Always verify through official channels.'
    '</div>',
    unsafe_allow_html=True,
)