"""
Phi LinkedIn Intelligence — Home page
Entry point. Shows the four headline numbers, the seven-act narrative,
and navigation to each department page.
"""
import streamlit as st
from utils import (
    inject_css, sidebar_branding, sidebar_footer, password_gate,
    big_stat, NAVY, AMBER, SUCCESS, WARN, MUTE,
    load_warm_leads, load_buying_committees, load_high_intent_commenters,
    load_audience_overlap,
)

st.set_page_config(
    page_title="Phi LinkedIn Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

password_gate()
inject_css()
sidebar_branding()
sidebar_footer()

# ── Hero ────────────────────────────────────────────────────────────
st.markdown("<div class='eyebrow'>Phi Management Group · LinkedIn Intelligence</div>",
            unsafe_allow_html=True)
st.markdown("""
<h1 style='font-size: 3rem; line-height: 1.05; margin-top: 0.5rem;
           letter-spacing: -0.025em; max-width: 950px;'>
    From <span style='color: #C08552;'>Reach</span>
    to <span style='color: #C08552;'>Conversion</span>.
</h1>
<p style='font-size: 1.15rem; color: #6B6B6B; max-width: 800px; line-height: 1.5;
          margin-top: 0.75rem;'>
    A LinkedIn analytics framework for Phi Management Group.
    One year of organic engagement across three pages, modeled, segmented,
    and operationalized into deliverables for every team.
</p>
""", unsafe_allow_html=True)

st.markdown("<hr class='hairline-amber'>", unsafe_allow_html=True)

# ── The four headline numbers ───────────────────────────────────────
warm = load_warm_leads()
committees = load_buying_committees()
commenters = load_high_intent_commenters()
overlap = load_audience_overlap()

c1, c2, c3, c4 = st.columns(4)
with c1:
    big_stat(f"{len(warm):,}", "Warm leads<br>3+ reactions, classified", color=AMBER)
with c2:
    big_stat(f"{len(committees)}", "Buying-committee accounts<br>3+ engaged employees", color=AMBER)
with c3:
    big_stat(f"{len(commenters):,}", "High-intent commenters<br>substantive comments", color=AMBER)
with c4:
    # 36 priority intersection — count from data if available
    big_stat("36", "Priority intersection<br>warm leads × competitor overlap", color=AMBER)

st.markdown("<br>", unsafe_allow_html=True)

# ── Three pillars ───────────────────────────────────────────────────
st.markdown("## What's inside")
st.markdown("Five department pages. Each one wired to the underlying data, "
            "filterable, exportable, ready to act on.")

cols = st.columns(5)
pages = [
    ("📈", "Leadership",       "KPIs, the funnel, the projection",
     "Top-level metrics, the 17,311 → 36 funnel, 12-month adoption scenario."),
    ("📞", "Business Development", "1,003 leads + priority list",
     "Filterable warm-lead list, role and seniority filters, LinkedIn URLs to copy."),
    ("✍️", "Marketing",         "Checklist + content rules",
     "8-point pre-publish checklist, lift roadmap, content-family playbook."),
    ("📊", "Analytics",         "Models, multiverse, audience",
     "Ridge model results, 30-path multiverse, audience overlap, all the numbers."),
    ("🏢", "Account Management", "21 buying-committee accounts",
     "Companies with 3+ engaged employees, Gartner-tier scoring, expansion vs net-new."),
]
for col, (icon, name, tag, desc) in zip(cols, pages):
    with col:
        st.markdown(f"""
        <div class='soft-card' style='height: 200px; display: flex; flex-direction: column;'>
            <div style='font-size: 1.5rem;'>{icon}</div>
            <div style='font-size: 1.05rem; font-weight: 700; color: #1F4E79;
                        margin-top: 0.5rem;'>{name}</div>
            <div style='font-size: 0.75rem; color: #C08552; font-weight: 600;
                        margin-top: 0.25rem; letter-spacing: 0.05em;'>{tag}</div>
            <div style='font-size: 0.8rem; color: #6B6B6B; line-height: 1.4;
                        margin-top: 0.5rem;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='font-size: 0.85rem; color: #6B6B6B; margin-top: 0.5rem;'>"
            "Use the sidebar to navigate.</div>", unsafe_allow_html=True)

# ── The 7-act story ─────────────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## The story in seven acts")

acts = [
    ("I",   "The Firm and Its Puzzle",
     "Phi has a multi-page LinkedIn architecture. Leadership wants the company page to be the commercial home. Empirically, it's the weakest of the three."),
    ("II",  "A Framework, Not a Dashboard",
     "270 posts, 17,311 reactions, 2,579 comments. 36 notebooks. A multivariate Ridge regression with author fixed effects. R² = 0.786."),
    ("III", "Why the Company Page Underperforms",
     "86% of explained variance is *shared* between author and content. The bottleneck isn't who writes — it's what gets written. Predicted lift: **+72%**."),
    ("IV",  "Knowing Who's Listening",
     "Behind 17,311 reactions sit 3,734 named individuals. 1,003 warm leads, 21 buying committees, 408 high-intent commenters."),
    ("V",   "The Competitive Picture",
     "Phi's audience indexes 1.4× to 2× more senior than every benchmark — but is 3× under-weighted on HR/L&D versus Korn Ferry."),
    ("VI",  "From Diagnosis to Action",
     "Three recommendations. A 90-day calendar. A 12-month projection. Status quo: 25 median engagement. Adopted: 67."),
    ("VII", "Limitations and Future Work",
     "Engagement-only data, no CRM linkage yet, asymmetric cleaning. Future: impressions, CRM cross-reference, real-time scoring."),
]

for num, title, body in acts:
    st.markdown(f"""
    <div style='display: grid; grid-template-columns: 60px 1fr; gap: 1rem;
                padding: 0.6rem 0; border-bottom: 1px solid #D9D2C5;'>
        <div style='font-size: 1.4rem; font-weight: 800; color: #C08552;'>{num}</div>
        <div>
            <div style='font-weight: 700; color: #1F4E79; font-size: 1.05rem;'>{title}</div>
            <div style='color: #6B6B6B; font-size: 0.92rem; line-height: 1.5; margin-top: 0.2rem;'>{body}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Methodology note ────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class='soft-card highlight'>
    <div style='font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em;
                text-transform: uppercase; color: #C08552;'>Methodology note</div>
    <div style='margin-top: 0.5rem; color: #0B1E33; line-height: 1.6;'>
        All figures in this dashboard reflect <strong>cleaned external engagement</strong> —
        Phi staff reactions and comments have been filtered out using LinkedIn URN identifiers
        cross-referenced against the firm's roster. Removing internal noise <em>widens</em>
        the founder-to-company gap from 6.1× to 7.5× on the CEO and from 3.8× to 4.7× on the
        Managing Partner. The diagnosis is stronger, not weaker.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #6B6B6B; font-size: 0.85rem; margin-top: 2rem;'>
    AUB MSBA Capstone · Antoine Saade · Spring 2026<br>
    <span style='color: #C08552;'>Phi Management Group</span> · Company Representative: Celine Ghantous
</div>
""", unsafe_allow_html=True)
