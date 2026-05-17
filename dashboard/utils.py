"""
Shared utilities for the Phi LinkedIn Intelligence dashboard.
Used across all pages: theming, data loading, formatting helpers, password stub.
"""
import os
import streamlit as st
import pandas as pd
from pathlib import Path

# ── Palette ─────────────────────────────────────────────────────────
NAVY    = "#1F4E79"
NAVY_DK = "#0B1E33"
AMBER   = "#C08552"
AMBER_LT = "#D9A373"
PAPER   = "#FAF7F2"
CREAM   = "#F5EFE3"
MUTE    = "#6B6B6B"
RULE    = "#D9D2C5"
SUCCESS = "#4A7C59"
WARN    = "#B85450"

CHART_TEMPLATE = "simple_white"
CHART_FONT = dict(family="Inter, system-ui, sans-serif", size=12, color=NAVY_DK)

DATA_DIR = Path(__file__).parent / "data"


# ── Custom CSS injected once per page ───────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* Base */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', system-ui, sans-serif;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #1F4E79;
    }
    h1 { font-size: 2.5rem; }
    h2 { font-size: 1.6rem; }
    h3 { font-size: 1.2rem; }

    /* Eyebrow */
    .eyebrow {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #6B6B6B;
        margin-bottom: 0.4rem;
    }

    /* Big stat */
    .big-stat {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1;
        color: #1F4E79;
        letter-spacing: -0.025em;
    }
    .big-stat.amber { color: #C08552; }
    .big-stat.success { color: #4A7C59; }
    .big-stat.warn { color: #B85450; }
    .big-stat-label {
        font-size: 0.85rem;
        color: #6B6B6B;
        margin-top: 0.4rem;
        line-height: 1.4;
    }

    /* Soft card */
    .soft-card {
        background: #F5EFE3;
        border: 1px solid #D9D2C5;
        border-radius: 6px;
        padding: 1.25rem 1.5rem;
        margin: 0.5rem 0;
    }
    .soft-card.highlight {
        border-color: #C08552;
        border-width: 2px;
    }

    /* Hairline */
    .hairline {
        height: 1px;
        background: #D9D2C5;
        border: none;
        margin: 1.5rem 0;
    }
    .hairline-amber {
        height: 2px;
        background: #C08552;
        border: none;
        margin: 0.5rem 0 1rem;
        width: 60px;
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #D9D2C5;
        border-radius: 6px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F5EFE3;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #1F4E79;
    }

    /* Hide streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Tag chips for filters */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #C08552 !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ── Page chrome (call at top of every page) ────────────────────────
def page_header(department, page_title, subtitle=None):
    """Render a consistent page header."""
    inject_css()
    st.markdown(f"<div class='eyebrow'>{department}</div>", unsafe_allow_html=True)
    st.markdown(f"# {page_title}")
    if subtitle:
        st.markdown(f"<p style='color: #6B6B6B; font-size: 1.05rem; margin-top: -0.5rem;'>{subtitle}</p>",
                    unsafe_allow_html=True)
    st.markdown("<hr class='hairline-amber'>", unsafe_allow_html=True)


def big_stat(value, label, color=NAVY):
    """Render a big stat box. Use inside st.columns()."""
    cls = ""
    if color == AMBER: cls = "amber"
    elif color == SUCCESS: cls = "success"
    elif color == WARN: cls = "warn"
    st.markdown(
        f"<div class='big-stat {cls}'>{value}</div>"
        f"<div class='big-stat-label'>{label}</div>",
        unsafe_allow_html=True,
    )


def sidebar_branding():
    """Add Phi branding to the sidebar."""
    with st.sidebar:
        st.markdown("""
        <div style='padding: 0.5rem 0 1rem;'>
            <div style='font-size: 0.7rem; font-weight: 600; letter-spacing: 0.2em;
                        text-transform: uppercase; color: #6B6B6B;'>
                Phi Management
            </div>
            <div style='font-size: 1.5rem; font-weight: 800; color: #1F4E79;
                        line-height: 1.1; margin-top: 0.2rem;'>
                LinkedIn Intelligence
            </div>
            <div style='font-size: 0.85rem; color: #C08552; font-style: italic;
                        margin-top: 0.4rem;'>
                From reach to conversion
            </div>
        </div>
        <hr style='border: none; height: 1px; background: #D9D2C5;'>
        """, unsafe_allow_html=True)


def sidebar_footer():
    """Bottom of sidebar info."""
    with st.sidebar:
        st.markdown("""
        <div style='position: fixed; bottom: 1rem; left: 1rem; right: 1rem;
                    font-size: 0.75rem; color: #6B6B6B; line-height: 1.4;'>
            <hr style='border: none; height: 1px; background: #D9D2C5;'>
            AUB MSBA Capstone · 2026<br>
            Antoine Saade · 36 notebooks<br>
            Study window: Jun 2025 – May 2026
        </div>
        """, unsafe_allow_html=True)


# ── Data loaders (cached) ──────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_warm_leads():
    df = pd.read_csv(DATA_DIR / "phi_warm_leads_external.csv")
    df['n_reactions'] = df['n_reactions'].astype(int)
    return df


@st.cache_data(show_spinner=False)
def load_buying_committees():
    return pd.read_csv(DATA_DIR / "phi_buying_committees_classified.csv")


@st.cache_data(show_spinner=False)
def load_high_intent_commenters():
    return pd.read_csv(DATA_DIR / "phi_high_intent_commenters_external.csv")


@st.cache_data(show_spinner=False)
def load_audience_overlap():
    return pd.read_csv(DATA_DIR / "audience_overlap_full.csv")


@st.cache_data(show_spinner=False)
def load_power_audience():
    return pd.read_csv(DATA_DIR / "power_audience_all_brand_touchpoints.csv")


@st.cache_data(show_spinner=False)
def load_roadmap():
    return pd.read_csv(DATA_DIR / "roadmap_cumulative_external.csv")


@st.cache_data(show_spinner=False)
def load_warm_leads_net_new():
    return pd.read_csv(DATA_DIR / "warm_leads_net_new.csv")


@st.cache_data(show_spinner=False)
def load_warm_leads_expansion():
    return pd.read_csv(DATA_DIR / "warm_leads_expansion.csv")


@st.cache_data(show_spinner=False)
def load_multiverse():
    return pd.read_csv(DATA_DIR / "multiverse_results.csv")


# ── Password gate (stub — flip ENABLED to True when you set the secret) ─
def password_gate():
    """
    Optional password protection. To enable:
      1. In Streamlit Cloud → App settings → Secrets, add:
         DASHBOARD_PASSWORD = "yourpassword"
      2. Set ENABLED below to True.
    The gate is currently OFF — the dashboard is fully public.
    """
    ENABLED = False
    if not ENABLED:
        return True

    try:
        expected = st.secrets["DASHBOARD_PASSWORD"]
    except (KeyError, FileNotFoundError):
        st.error("Password protection is enabled but no secret is configured.")
        st.stop()

    if st.session_state.get("authenticated"):
        return True

    st.markdown("# Phi LinkedIn Intelligence")
    st.markdown("This dashboard is password-protected.")
    pw = st.text_input("Password", type="password")
    if st.button("Sign in"):
        if pw == expected:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()


# ── Plotly default styling ─────────────────────────────────────────
def style_chart(fig, height=None):
    """Apply consistent Plotly styling."""
    fig.update_layout(
        template=CHART_TEMPLATE,
        font=CHART_FONT,
        plot_bgcolor=PAPER,
        paper_bgcolor=PAPER,
        margin=dict(l=20, r=20, t=40, b=20),
        title_font_size=14,
        title_font_color=NAVY,
        showlegend=fig.layout.showlegend if fig.layout.showlegend is not None else True,
    )
    if height:
        fig.update_layout(height=height)
    fig.update_xaxes(showgrid=False, gridcolor=RULE, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=RULE, gridwidth=0.5, zeroline=False)
    return fig


def linkedin_link(url):
    """Format a LinkedIn URL as a clickable column."""
    if pd.isna(url) or not url:
        return ""
    return url
