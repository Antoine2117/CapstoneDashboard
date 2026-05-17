"""
Business Development — 1,003 warm leads, filterable.
Clean filename so the sidebar reads "Business Development" instead of "1_📞_Business_Development".
"""
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Business Development",
    page_icon="◉",
    layout="wide",
)

CHARCOAL = "#2C2925"
GOLD = "#B8945D"
WARM = "#FBF9F5"
SOFT_BEIGE = "#F0EBE0"
MUTE = "#7A736B"
BORDER = "#E5DFD3"

st.markdown(f"""
<style>
.stApp {{ background: {WARM}; }}
.main .block-container {{ padding-top: 2rem; padding-bottom: 4rem; max-width: 1200px; }}
h1, h2, h3 {{ color: {CHARCOAL} !important; font-weight: 600 !important; letter-spacing: -0.015em !important; }}
.eyebrow {{
    font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: {GOLD}; font-weight: 600; margin-bottom: 0.4rem;
}}
.stat {{
    font-size: 2.2rem; font-weight: 600; color: {CHARCOAL};
    line-height: 1; letter-spacing: -0.02em;
}}
.stat-label {{ color: {MUTE}; font-size: 0.8rem; margin-top: 0.4rem; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stSidebar"] {{ background: {SOFT_BEIGE}; }}
[data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 6px; }}
.stMultiSelect [data-baseweb="tag"] {{ background-color: {GOLD} !important; }}
.stDownloadButton button {{
    background: white !important; color: {CHARCOAL} !important;
    border: 1px solid {BORDER} !important; border-radius: 4px !important;
}}
.stDownloadButton button:hover {{ border-color: {GOLD} !important; color: {GOLD} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown(f"<div class='eyebrow'>For BD</div>", unsafe_allow_html=True)
st.markdown("# Business Development")
st.markdown(f"<p style='color: {MUTE}; margin-top: -0.4rem;'>"
            "Warm leads ranked by engagement. Filter, sort, export.</p>",
            unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────
DATA = Path(__file__).parent.parent / "data"
warm = pd.read_csv(DATA / "phi_warm_leads_external.csv")
net_new = pd.read_csv(DATA / "warm_leads_net_new.csv")
expansion = pd.read_csv(DATA / "warm_leads_expansion.csv")
committees = pd.read_csv(DATA / "phi_buying_committees_classified.csv")

# ── Top numbers ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='stat'>{len(warm):,}</div>"
                f"<div class='stat-label'>warm leads</div>", unsafe_allow_html=True)
with c2:
    csuite = (warm['seniority'] == 'C-Suite').sum()
    st.markdown(f"<div class='stat'>{csuite:,}</div>"
                f"<div class='stat-label'>C-Suite leads</div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='stat'>{len(expansion):,}</div>"
                f"<div class='stat-label'>existing-client expansion</div>",
                unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='stat'>{len(net_new):,}</div>"
                f"<div class='stat-label'>net-new prospects</div>",
                unsafe_allow_html=True)

st.markdown(f"<hr style='border:none; height:1px; background:{BORDER}; margin: 2rem 0;'>",
            unsafe_allow_html=True)

# ── Filters ──────────────────────────────────────────────────
st.markdown("### Filter")

f1, f2, f3 = st.columns(3)
with f1:
    role_filter = st.multiselect(
        "Role",
        options=sorted(warm['role'].dropna().unique().tolist()),
    )
with f2:
    seniority_filter = st.multiselect(
        "Seniority",
        options=sorted(warm['seniority'].dropna().unique().tolist()),
    )
with f3:
    lead_type = st.radio("Type", ["All", "Net-new", "Expansion"], horizontal=True)

# Apply filters
df = warm.copy()
if role_filter:
    df = df[df['role'].isin(role_filter)]
if seniority_filter:
    df = df[df['seniority'].isin(seniority_filter)]
if lead_type == "Net-new":
    df = df[df['reactor_id'].isin(net_new['reactor_id'])]
elif lead_type == "Expansion":
    df = df[df['reactor_id'].isin(expansion['reactor_id'])]

# Result count
st.markdown(f"<p style='color: {GOLD}; font-weight: 600; margin-top: 1rem;'>"
            f"Showing {len(df):,} of {len(warm):,} leads</p>",
            unsafe_allow_html=True)

# ── Lead table ───────────────────────────────────────────────
display = df[['name', 'position', 'role', 'seniority', 'inferred_company',
              'n_reactions', 'linkedinUrl']].sort_values('n_reactions', ascending=False)
display.columns = ['Name', 'Position', 'Role', 'Seniority', 'Company',
                   'Reactions', 'LinkedIn']

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
    height=500,
    column_config={
        "Reactions": st.column_config.NumberColumn(format="%d"),
        "LinkedIn": st.column_config.LinkColumn(display_text="Open profile"),
        "Position": st.column_config.TextColumn(width="large"),
    },
)

# ── Download ─────────────────────────────────────────────────
csv = display.to_csv(index=False).encode('utf-8')
st.download_button(
    "Download filtered list (CSV)",
    csv,
    "phi_warm_leads_filtered.csv",
    "text/csv",
)

st.markdown(f"<hr style='border:none; height:1px; background:{BORDER}; margin: 2.5rem 0;'>",
            unsafe_allow_html=True)

# ── Target accounts (compact section, just a table) ──────────
st.markdown("### Target accounts")
st.markdown(f"<p style='color: {MUTE};'>"
            f"{len(committees)} companies with 3+ employees engaging. "
            f"The deepest buying signals in the data.</p>",
            unsafe_allow_html=True)

acc_display = committees.rename(columns={
    'inferred_company': 'Company',
    'n_unique_employees': 'Engaged employees',
    'n_total_reactions': 'Total reactions',
    'confidence_tier': 'Confidence',
    'matched_sector': 'Sector',
    'account_type': 'Type',
})[['Company', 'Engaged employees', 'Total reactions', 'Sector', 'Type', 'Confidence']]
acc_display = acc_display.sort_values('Engaged employees', ascending=False)

st.dataframe(
    acc_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Engaged employees": st.column_config.NumberColumn(format="%d"),
        "Total reactions": st.column_config.NumberColumn(format="%d"),
    },
)
