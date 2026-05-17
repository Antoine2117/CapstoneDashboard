"""
Phi LinkedIn Intelligence — Home
Simple landing: the four numbers, navigation cards, that's it.
"""
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Phi LinkedIn Intelligence",
    page_icon="◉",
    layout="centered",
    initial_sidebar_state="auto",
)

# Palette inspired by phimanagement.com
CHARCOAL = "#2C2925"
GOLD = "#B8945D"
WARM = "#FBF9F5"
SOFT_BEIGE = "#F0EBE0"
MUTE = "#7A736B"
BORDER = "#E5DFD3"

st.markdown(f"""
<style>
.stApp {{ background: {WARM}; }}
.main .block-container {{ padding-top: 3rem; max-width: 880px; }}
h1 {{
    font-weight: 600 !important;
    color: {CHARCOAL} !important;
    letter-spacing: -0.015em !important;
}}
h2, h3 {{ color: {CHARCOAL} !important; font-weight: 600 !important; }}
.eyebrow {{
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: {GOLD};
    font-weight: 600;
    margin-bottom: 0.5rem;
}}
.stat {{
    font-size: 2.8rem;
    font-weight: 600;
    color: {CHARCOAL};
    line-height: 1;
    letter-spacing: -0.02em;
}}
.stat-label {{
    color: {MUTE};
    font-size: 0.85rem;
    margin-top: 0.5rem;
}}
.card {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 1.5rem;
    transition: border-color 0.15s ease;
    height: 100%;
}}
.card:hover {{ border-color: {GOLD}; }}
.card-title {{
    font-size: 1.05rem;
    font-weight: 600;
    color: {CHARCOAL};
    margin-bottom: 0.4rem;
}}
.card-desc {{
    color: {MUTE};
    font-size: 0.88rem;
    line-height: 1.5;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stSidebar"] {{ background: {SOFT_BEIGE}; }}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown(f"<div class='eyebrow'>Phi Management Group</div>", unsafe_allow_html=True)
st.markdown(f"<h1 style='font-size: 2.6rem; line-height: 1.1; margin-top: 0.3rem;'>"
            f"LinkedIn Intelligence</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {MUTE}; font-size: 1.05rem; margin-top: 0.5rem;'>"
            f"What the data says about our LinkedIn audience, and what to do with it.</p>",
            unsafe_allow_html=True)

st.markdown(f"<hr style='border:none; height:1px; background:{BORDER}; margin: 2rem 0;'>",
            unsafe_allow_html=True)

# ── The four numbers ─────────────────────────────────────────
DATA = Path(__file__).parent / "data"
warm = pd.read_csv(DATA / "phi_warm_leads_external.csv")
committees = pd.read_csv(DATA / "phi_buying_committees_classified.csv")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='stat'>{len(warm):,}</div>"
                f"<div class='stat-label'>warm leads</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='stat'>{len(committees)}</div>"
                f"<div class='stat-label'>account targets</div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='stat'>+72%</div>"
                f"<div class='stat-label'>predicted lift</div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='stat'>26.4%</div>"
                f"<div class='stat-label'>C-Suite audience</div>", unsafe_allow_html=True)

st.markdown(f"<hr style='border:none; height:1px; background:{BORDER}; margin: 2.5rem 0;'>",
            unsafe_allow_html=True)

# ── Navigation cards ─────────────────────────────────────────
st.markdown("### Where to go")
st.markdown(f"<p style='color: {MUTE}; margin-bottom: 1.5rem;'>"
            f"Two pages. Use the sidebar to navigate.</p>",
            unsafe_allow_html=True)

n1, n2 = st.columns(2)
with n1:
    st.markdown(f"""
    <div class='card'>
        <div class='eyebrow' style='font-size: 0.65rem;'>For BD</div>
        <div class='card-title'>Business Development</div>
        <div class='card-desc'>
            {len(warm):,} warm leads and {len(committees)} target accounts. Filter by role,
            seniority, or industry. Export the filtered list.
        </div>
    </div>
    """, unsafe_allow_html=True)

with n2:
    st.markdown(f"""
    <div class='card'>
        <div class='eyebrow' style='font-size: 0.65rem;'>For Marketing</div>
        <div class='card-title'>Marketing</div>
        <div class='card-desc'>
            The 8-point pre-publish checklist and the interactive lift roadmap.
            See which content rules drive engagement on the company page.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer note ──────────────────────────────────────────────
st.markdown(f"<br>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {MUTE}; font-size: 0.8rem; text-align: center; margin-top: 3rem;'>"
            f"Phi Management Group · MSBA Capstone 2026 · Antoine Saade</p>",
            unsafe_allow_html=True)
