"""
Leadership page — KPIs, the 17,311 → 36 funnel, 12-month projection
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import (
    page_header, sidebar_branding, sidebar_footer, password_gate,
    big_stat, style_chart, NAVY, AMBER, SUCCESS, WARN, MUTE, CREAM, RULE,
    load_warm_leads, load_buying_committees, load_high_intent_commenters,
)

st.set_page_config(page_title="Leadership · Phi LinkedIn", page_icon="📈", layout="wide")
password_gate()
sidebar_branding()
sidebar_footer()

page_header("Leadership", "The big picture",
            "Top-line KPIs, the funnel from organic reactions to priority targets, and the 12-month adopted-scenario projection.")

# ── KPI strip ───────────────────────────────────────────────────────
st.markdown("## Headline metrics")
c1, c2, c3, c4 = st.columns(4)
with c1: big_stat("17,311", "Total reactions<br>over 11 months", color=NAVY)
with c2: big_stat("3,734", "Unique reactors<br>named individuals", color=NAVY)
with c3: big_stat("+72%", "Predicted lift<br>if company page reformats", color=SUCCESS)
with c4: big_stat("R² = 0.786", "Cross-validated model fit<br>5-fold CV, 19 features", color=NAVY)

st.markdown("<br>", unsafe_allow_html=True)

# ── Second row of KPIs ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: big_stat("26.4%", "C-Suite audience share<br>1.4–2× more senior than every peer", color=AMBER)
with c2: big_stat("−349", "Engagement units lost/month<br>p = 0.008 · trajectory is real", color=WARN)
with c3: big_stat("22% / 58%", "Internal likes / comments<br>filtered out before analysis", color=WARN)
with c4: big_stat("97%", "Multiverse robustness<br>29 of 30 paths support gap", color=NAVY)

st.markdown("<hr class='hairline'>", unsafe_allow_html=True)

# ── The funnel ──────────────────────────────────────────────────────
st.markdown("## From 17,311 reactions to 36 priority targets")
st.markdown("<div style='color: #6B6B6B; margin-bottom: 1.5rem;'>"
            "Each successive filter distills organic engagement into prioritized commercial intent. "
            "The 36 names at the bottom are the cross-validated highest-intent segment in the dataset.</div>",
            unsafe_allow_html=True)

funnel = go.Figure(go.Funnel(
    y=["Total reactions", "Unique reactors", "Warm leads (3+)", "Category shoppers", "Priority intersection"],
    x=[17311, 3734, 1003, 93, 36],
    textposition="inside",
    textinfo="value+percent initial",
    marker=dict(color=[NAVY, "#2c6ba4", "#4a8bc9", AMBER, "#a0683d"],
                line=dict(width=2, color="white")),
    connector=dict(line=dict(color=RULE, width=1)),
    textfont=dict(size=14, color="white", family="Inter"),
))
funnel.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="#FAF7F2",
    paper_bgcolor="#FAF7F2",
    font=dict(family="Inter", size=13, color=NAVY),
)
st.plotly_chart(funnel, use_container_width=True)

# Notes under the funnel
n1, n2 = st.columns(2)
with n1:
    st.markdown("""
    <div class='soft-card'>
        <div style='font-weight: 700; color: #1F4E79;'>The composition of the 36</div>
        <div style='color: #6B6B6B; font-size: 0.92rem; line-height: 1.6; margin-top: 0.4rem;'>
            <strong>50%</strong> are C-Suite or HR/L&D — the two functions Phi's offering speaks to most directly.
            <strong>Two</strong> follow Phi together with all three competitors — the deepest research signal in the data.
            <strong>Eight</strong> are active multi-vendor shoppers comparing 2+ competitors right now.
        </div>
    </div>
    """, unsafe_allow_html=True)
with n2:
    st.markdown("""
    <div class='soft-card highlight'>
        <div style='font-weight: 700; color: #1F4E79;'>Why this matters</div>
        <div style='color: #6B6B6B; font-size: 0.92rem; line-height: 1.6; margin-top: 0.4rem;'>
            Most B2B leadership consultancies operate without named-individual intelligence
            on who is engaging. The 36 here are public LinkedIn profiles, classified by role
            and industry, ready for the BD team to action this quarter.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='hairline'>", unsafe_allow_html=True)

# ── 12-month projection ─────────────────────────────────────────────
st.markdown("## A 12-month projection: status quo vs. adopted scenario")
st.markdown("<div style='color: #6B6B6B; margin-bottom: 1.5rem;'>"
            "If Phi adopts the three recommendations — reformat the company page, "
            "launch the HR/L&D sprint, work the priority list — model predictions over 12 months "
            "with ±25% sensitivity bounds derived from the 30 multiverse paths.</div>",
            unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)
projections = [
    ("Company-page median engagement", 25, 67, "weighted units / post"),
    ("HR / L&D audience share",         10.0, 16.5, "% of audience"),
    ("Engaged warm-lead pipeline",      1050, 1545, "named individuals"),
]
for col, (label, sq, adopted, unit) in zip([p1, p2, p3], projections):
    delta = adopted - sq
    pct = (adopted / sq - 1) * 100 if sq else 0
    with col:
        st.markdown(f"""
        <div class='soft-card'>
            <div style='font-size: 0.8rem; color: #6B6B6B; text-transform: uppercase;
                        letter-spacing: 0.08em; font-weight: 600;'>{label}</div>
            <div style='margin-top: 1rem; display: flex; align-items: baseline; gap: 1rem;'>
                <div>
                    <div style='font-size: 0.7rem; color: #6B6B6B;'>Status quo</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #6B6B6B;'>{sq:,}</div>
                </div>
                <div style='font-size: 1.5rem; color: #C08552;'>→</div>
                <div>
                    <div style='font-size: 0.7rem; color: #C08552;'>Adopted</div>
                    <div style='font-size: 2.5rem; font-weight: 800; color: #C08552;
                                letter-spacing: -0.02em;'>{adopted:,}</div>
                </div>
            </div>
            <div style='font-size: 0.8rem; color: #4A7C59; font-weight: 600; margin-top: 0.5rem;'>
                +{pct:.0f}% lift · {unit}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── 3 recommendations recap ─────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## Three recommendations")

r1, r2, r3 = st.columns(3)
recs = [
    ("01", "Reformat the company page",
     "Three rule-based changes capture the easy 58% of the available 72% lift. "
     "Every company-page post scores ≥6/8 on the pre-publish checklist before publication.",
     "+72% predicted lift"),
    ("02", "Close the HR/L&D gap",
     "90-day HR/L&D content sprint. HR-functional content rather than founder-thematic. "
     "Track audience-function shift weekly.",
     "10.5% → 16.5% target"),
    ("03", "Work the lists this quarter",
     "36-person priority intersection is pipeline-ready. No content changes required. "
     "Close two measurement loops: re-run with impressions, validate against CRM.",
     "36 priority targets"),
]
for col, (num, title, body, metric) in zip([r1, r2, r3], recs):
    with col:
        st.markdown(f"""
        <div class='soft-card' style='height: 100%;'>
            <div style='font-size: 3rem; font-weight: 800; color: #C08552;
                        line-height: 1; margin-bottom: 0.5rem;'>{num}</div>
            <div style='font-weight: 700; color: #1F4E79; font-size: 1.1rem;'>{title}</div>
            <div style='color: #6B6B6B; font-size: 0.9rem; line-height: 1.5;
                        margin-top: 0.6rem;'>{body}</div>
            <div style='font-size: 0.85rem; color: #C08552; font-weight: 700;
                        margin-top: 0.8rem; padding-top: 0.6rem;
                        border-top: 1px solid #D9D2C5;'>{metric}</div>
        </div>
        """, unsafe_allow_html=True)
