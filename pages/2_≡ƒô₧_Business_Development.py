"""
Business Development page — 1,003 warm leads, filterable + exportable,
plus the priority-intersection breakdown.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (
    page_header, sidebar_branding, sidebar_footer, password_gate,
    big_stat, style_chart, NAVY, AMBER, SUCCESS, WARN, MUTE, CREAM, RULE,
    load_warm_leads, load_warm_leads_net_new, load_warm_leads_expansion,
)

st.set_page_config(page_title="BD · Phi LinkedIn", page_icon="📞", layout="wide")
password_gate()
sidebar_branding()
sidebar_footer()

page_header("Business Development",
            "1,003 warm leads. Ready to action.",
            "Every individual on this page reacted 3+ times to a Phi post in the study window. "
            "Filter by role, seniority, or industry. Click any LinkedIn URL to view their profile.")

warm = load_warm_leads()
net_new = load_warm_leads_net_new()
expansion = load_warm_leads_expansion()

# ── Top KPI strip ───────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: big_stat(f"{len(warm):,}", "Total warm leads<br>3+ reactions, classified", color=AMBER)
with c2: big_stat(f"{len(expansion)}", "Existing-client expansion<br>matched to client list", color=NAVY)
with c3: big_stat(f"{len(net_new)}", "Net-new prospects<br>not in current client roster", color=NAVY)
with c4:
    csuite = (warm['seniority'] == 'C-Suite').sum()
    big_stat(f"{csuite}", f"C-Suite leads<br>{100*csuite/len(warm):.0f}% of total", color=AMBER)

st.markdown("<hr class='hairline'>", unsafe_allow_html=True)

# ── Filters ─────────────────────────────────────────────────────────
st.markdown("## Filter the list")

f1, f2, f3, f4 = st.columns([1, 1, 1, 1])
with f1:
    role_filter = st.multiselect(
        "Role",
        options=sorted(warm['role'].dropna().unique().tolist()),
        default=[],
    )
with f2:
    seniority_filter = st.multiselect(
        "Seniority",
        options=sorted(warm['seniority'].dropna().unique().tolist()),
        default=[],
    )
with f3:
    min_reactions = st.slider(
        "Min reactions",
        min_value=3,
        max_value=int(warm['n_reactions'].max()),
        value=3,
        step=1,
    )
with f4:
    lead_type = st.radio("Lead type", ["All", "Net-new", "Expansion"], horizontal=True)

# Apply filters
df = warm.copy()
if role_filter:
    df = df[df['role'].isin(role_filter)]
if seniority_filter:
    df = df[df['seniority'].isin(seniority_filter)]
df = df[df['n_reactions'] >= min_reactions]
if lead_type == "Net-new":
    df = df[df['reactor_id'].isin(net_new['reactor_id'])]
elif lead_type == "Expansion":
    df = df[df['reactor_id'].isin(expansion['reactor_id'])]

# Show result count
st.markdown(f"""
<div style='font-size: 0.95rem; color: #1F4E79; font-weight: 600; margin: 0.5rem 0 1rem;'>
    Showing <span style='color: #C08552;'>{len(df):,}</span> leads
    ({100*len(df)/len(warm):.0f}% of total)
</div>
""", unsafe_allow_html=True)

# ── Composition charts ──────────────────────────────────────────────
g1, g2 = st.columns(2)

with g1:
    role_counts = df['role'].value_counts().reset_index()
    role_counts.columns = ['role', 'count']
    if len(role_counts):
        fig = px.bar(
            role_counts, y='role', x='count', orientation='h',
            color_discrete_sequence=[AMBER],
            title="By role",
        )
        fig.update_traces(
            text=role_counts['count'],
            textposition='outside',
            textfont=dict(size=11, color=NAVY),
            hovertemplate='<b>%{y}</b><br>%{x} leads<extra></extra>',
        )
        fig = style_chart(fig, height=350)
        fig.update_yaxes(categoryorder='total ascending', title="")
        fig.update_xaxes(title="Number of leads")
        st.plotly_chart(fig, use_container_width=True)

with g2:
    sen_counts = df['seniority'].value_counts().reset_index()
    sen_counts.columns = ['seniority', 'count']
    if len(sen_counts):
        sen_order = ['C-Suite', 'VP/Director', 'Manager', 'Mid/Junior', 'Other']
        sen_counts['order'] = sen_counts['seniority'].map(
            {s: i for i, s in enumerate(sen_order)}).fillna(99)
        sen_counts = sen_counts.sort_values('order')
        fig = px.bar(
            sen_counts, x='seniority', y='count',
            color_discrete_sequence=[NAVY],
            title="By seniority",
        )
        fig.update_traces(
            text=sen_counts['count'],
            textposition='outside',
            textfont=dict(size=11, color=NAVY),
            hovertemplate='<b>%{x}</b><br>%{y} leads<extra></extra>',
        )
        fig = style_chart(fig, height=350)
        fig.update_xaxes(title="")
        fig.update_yaxes(title="Number of leads")
        st.plotly_chart(fig, use_container_width=True)

# ── The lead list itself ────────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## The lead list")
st.markdown(
    "<div style='color: #6B6B6B; font-size: 0.95rem; margin-bottom: 1rem;'>"
    "Sorted by reaction count, descending. Click any URL to open the LinkedIn profile. "
    "Use the download button to export the filtered list as CSV.</div>",
    unsafe_allow_html=True)

display = df[['name', 'position', 'role', 'seniority', 'inferred_company',
              'n_reactions', 'linkedinUrl']].sort_values('n_reactions', ascending=False)
display.columns = ['Name', 'Position', 'Role', 'Seniority', 'Company', 'Reactions', 'LinkedIn']

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
    height=520,
    column_config={
        "Reactions": st.column_config.NumberColumn(format="%d"),
        "LinkedIn": st.column_config.LinkColumn(display_text="View profile"),
        "Position": st.column_config.TextColumn(width="large"),
        "Name": st.column_config.TextColumn(width="medium"),
    },
)

# Download
csv = display.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Download filtered list (CSV)",
    csv,
    "phi_warm_leads_filtered.csv",
    "text/csv",
    key='download-csv',
)

# ── Priority intersection callout ───────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("""
<div class='soft-card highlight'>
    <div style='font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em;
                text-transform: uppercase; color: #C08552;'>The 36-person priority intersection</div>
    <div style='display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; margin-top: 1rem;
                align-items: center;'>
        <div>
            <div style='font-size: 5rem; font-weight: 800; color: #C08552; line-height: 1;'>36</div>
            <div style='color: #6B6B6B; font-size: 0.9rem; margin-top: 0.5rem;'>
                Warm Phi leads who <em>also</em> engage with at least one direct competitor
                (Mercer IMEA, Mercer global, or Korn Ferry).
            </div>
        </div>
        <div>
            <div style='color: #0B1E33; line-height: 1.7;'>
                <strong style='color: #1F4E79;'>50%</strong> are C-Suite or HR/L&D — the two functions Phi's offering speaks to most directly.<br>
                <strong style='color: #1F4E79;'>8 active multi-vendor shoppers</strong> are comparing 2+ competitors right now. Outreach this week.<br>
                <strong style='color: #1F4E79;'>2 deepest signals</strong> follow Phi together with all three competitors.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Suggested workflow ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## Suggested workflow")
st.markdown("""
1. **Filter** by role and seniority to match your current campaign's ICP
2. **Sort** by reaction count to find the most engaged individuals first
3. **Export** the filtered CSV for your CRM or outreach tool
4. **Cross-reference** each lead's LinkedIn profile before outreach — context matters
5. **Track outcomes** in your CRM and revisit this dashboard weekly as new data flows in
""")
