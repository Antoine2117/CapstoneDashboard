"""
Account Management page — 21 buying-committee accounts, classified, tiered.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (
    page_header, sidebar_branding, sidebar_footer, password_gate,
    big_stat, style_chart, NAVY, AMBER, SUCCESS, WARN, MUTE, CREAM, RULE,
    load_buying_committees, load_warm_leads,
)

st.set_page_config(page_title="Accounts · Phi LinkedIn", page_icon="🏢", layout="wide")
password_gate()
sidebar_branding()
sidebar_footer()

page_header("Account Management",
            "21 accounts with active buying signals",
            "Companies where 3+ employees have engaged with Phi's content. "
            "Tiered against Gartner / Forrester / Influ2 thresholds for B2B buying-committee depth.")

committees = load_buying_committees()
warm = load_warm_leads()

# ── Top KPI strip ───────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    big_stat(f"{len(committees)}",
             "Total buying-committee accounts<br>3+ engaged employees",
             color=AMBER)
with c2:
    high_tier = (committees['confidence_tier'].str.contains('High', na=False)).sum()
    big_stat(f"{high_tier}",
             "High-confidence accounts<br>Gartner threshold met",
             color=SUCCESS)
with c3:
    expansion = (committees['account_type'].str.contains('expansion', case=False, na=False)).sum()
    big_stat(f"{expansion}",
             "Existing-client expansion<br>cross-sell territory",
             color=NAVY)
with c4:
    total_emp = int(committees['n_unique_employees'].sum())
    big_stat(f"{total_emp}",
             "Total engaged employees<br>across all accounts",
             color=NAVY)

st.markdown("<hr class='hairline'>", unsafe_allow_html=True)

# ── Filters ─────────────────────────────────────────────────────────
st.markdown("## Filter the account list")

f1, f2, f3 = st.columns([1, 1, 1])
with f1:
    tier_options = sorted(committees['confidence_tier'].dropna().unique().tolist())
    tier_filter = st.multiselect("Confidence tier", options=tier_options, default=[])
with f2:
    type_options = sorted(committees['account_type'].dropna().unique().tolist())
    type_filter = st.multiselect("Account type", options=type_options, default=[])
with f3:
    sector_options = sorted(committees['matched_sector'].dropna().unique().tolist())
    sector_filter = st.multiselect("Sector", options=sector_options, default=[])

df = committees.copy()
if tier_filter:
    df = df[df['confidence_tier'].isin(tier_filter)]
if type_filter:
    df = df[df['account_type'].isin(type_filter)]
if sector_filter:
    df = df[df['matched_sector'].isin(sector_filter)]

st.markdown(f"""
<div style='font-size: 0.95rem; color: #1F4E79; font-weight: 600; margin: 0.5rem 0 1rem;'>
    Showing <span style='color: #C08552;'>{len(df)}</span> accounts
</div>
""", unsafe_allow_html=True)

# ── Account list table ──────────────────────────────────────────────
st.markdown("## Account roster")

display = df.copy()
display = display.rename(columns={
    'inferred_company': 'Company',
    'n_unique_employees': 'Engaged employees',
    'n_total_reactions': 'Total reactions',
    'avg_reactions_per_employee': 'Avg reactions/employee',
    'confidence_tier': 'Confidence tier',
    'matched_client': 'Matched client',
    'matched_sector': 'Sector',
    'account_type': 'Account type',
}).sort_values('Engaged employees', ascending=False)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Engaged employees": st.column_config.NumberColumn(format="%d"),
        "Total reactions": st.column_config.NumberColumn(format="%d"),
        "Avg reactions/employee": st.column_config.NumberColumn(format="%.1f"),
        "Company": st.column_config.TextColumn(width="medium"),
        "Confidence tier": st.column_config.TextColumn(width="large"),
        "Account type": st.column_config.TextColumn(width="medium"),
    },
)

# Download
csv = display.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Download accounts (CSV)",
    csv,
    "phi_buying_committees.csv",
    "text/csv",
)

# ── Top accounts by employee count ──────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## Engaged employees per account")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "The depth of engagement at each account. Higher counts indicate stronger buying-committee formation. "
    "Gartner's threshold for complex B2B buying decisions is 6–10 stakeholders.</div>",
    unsafe_allow_html=True)

# Bar chart
ranked = df.sort_values('n_unique_employees', ascending=True).copy()
ranked['color'] = ranked['account_type'].apply(
    lambda t: AMBER if 'expansion' in str(t).lower() else NAVY
)
fig = go.Figure(go.Bar(
    y=ranked['inferred_company'],
    x=ranked['n_unique_employees'],
    orientation='h',
    marker=dict(color=ranked['color']),
    text=ranked['n_unique_employees'],
    textposition='outside',
    textfont=dict(size=12, color=NAVY),
    hovertemplate=(
        '<b>%{y}</b><br>'
        '%{x} engaged employees<br>'
        '%{customdata[0]} total reactions<br>'
        '%{customdata[1]}<extra></extra>'
    ),
    customdata=ranked[['n_total_reactions', 'account_type']].values,
))
# Gartner threshold line
fig.add_vline(x=6, line_dash='dash', line_color=AMBER, opacity=0.5,
              annotation_text="Gartner complex-B2B floor (6 stakeholders)",
              annotation_font_color=AMBER, annotation_font_size=10,
              annotation_position="top")
fig.update_xaxes(title='Number of engaged employees')
fig.update_yaxes(title='')
fig.update_layout(height=max(400, 30 * len(ranked)), showlegend=False)
fig = style_chart(fig)
st.plotly_chart(fig, use_container_width=True)

# Legend for colors
st.markdown("""
<div style='display: flex; gap: 2rem; align-items: center; margin-top: -1rem;
            font-size: 0.85rem; color: #6B6B6B;'>
    <div><span style='display: inline-block; width: 12px; height: 12px;
         background: #C08552; border-radius: 2px; margin-right: 0.4rem;
         vertical-align: middle;'></span>Existing-client expansion</div>
    <div><span style='display: inline-block; width: 12px; height: 12px;
         background: #1F4E79; border-radius: 2px; margin-right: 0.4rem;
         vertical-align: middle;'></span>Net-new prospect</div>
</div>
""", unsafe_allow_html=True)

# ── Sector breakdown ────────────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## Distribution by sector")

if df['matched_sector'].notna().any():
    sector_counts = df.groupby('matched_sector').agg(
        n_accounts=('inferred_company', 'count'),
        total_employees=('n_unique_employees', 'sum'),
        total_reactions=('n_total_reactions', 'sum'),
    ).reset_index().sort_values('n_accounts', ascending=False)

    g1, g2 = st.columns([1, 1])
    with g1:
        fig = px.bar(
            sector_counts, x='n_accounts', y='matched_sector',
            orientation='h', color_discrete_sequence=[AMBER],
            title="Accounts per sector",
        )
        fig.update_traces(
            text=sector_counts['n_accounts'],
            textposition='outside',
            textfont=dict(color=NAVY),
        )
        fig.update_yaxes(categoryorder='total ascending', title="")
        fig.update_xaxes(title="Accounts")
        fig = style_chart(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with g2:
        fig = px.bar(
            sector_counts, x='total_employees', y='matched_sector',
            orientation='h', color_discrete_sequence=[NAVY],
            title="Engaged employees per sector",
        )
        fig.update_traces(
            text=sector_counts['total_employees'],
            textposition='outside',
            textfont=dict(color=NAVY),
        )
        fig.update_yaxes(categoryorder='total ascending', title="")
        fig.update_xaxes(title="Engaged employees")
        fig = style_chart(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)

# ── Account drill-down: show leads inside one account ───────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## Drill into an account")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "Select an account to see the individual leads inside it.</div>",
    unsafe_allow_html=True)

selected = st.selectbox(
    "Select an account",
    options=[""] + sorted(committees['inferred_company'].dropna().unique().tolist()),
    index=0,
)

if selected:
    leads_in_account = warm[warm['inferred_company'] == selected]
    if len(leads_in_account):
        st.markdown(f"""
        <div class='soft-card'>
            <div style='font-weight: 700; color: #1F4E79; font-size: 1.1rem;'>{selected}</div>
            <div style='color: #6B6B6B; margin-top: 0.3rem;'>
                <strong>{len(leads_in_account)}</strong> engaged employees ·
                <strong>{int(leads_in_account['n_reactions'].sum())}</strong> total reactions
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            leads_in_account[['name', 'position', 'role', 'seniority',
                              'n_reactions', 'linkedinUrl']].rename(columns={
                'name': 'Name', 'position': 'Position', 'role': 'Role',
                'seniority': 'Seniority', 'n_reactions': 'Reactions',
                'linkedinUrl': 'LinkedIn',
            }).sort_values('Reactions', ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Reactions": st.column_config.NumberColumn(format="%d"),
                "LinkedIn": st.column_config.LinkColumn(display_text="View profile"),
            },
        )
    else:
        st.info(f"No individual lead records found for {selected}. This may indicate the account "
                "is in the buying-committee list via a different name match.")

# ── Playbook ────────────────────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## How to use this list")

p1, p2, p3 = st.columns(3)
plays = [
    ("Expansion plays",
     "Accounts marked 'existing-client expansion' already trust Phi. Focus expansion conversations on adjacent service lines they haven't bought. "
     "Azadea Group (47 engaged) is the strongest signal in the dataset."),
    ("Net-new plays",
     "Accounts with no client match are net-new opportunities. The strongest signal is a high engaged-employee count plus a Gartner High tier — those are mature buying committees."),
    ("Insights to bring",
     "Use the model's content findings as a conversation opener: 'We've been studying leadership-content engagement across your industry. Here's what we found about HR/L&D buying patterns…'"),
]
for col, (title, body) in zip([p1, p2, p3], plays):
    with col:
        st.markdown(f"""
        <div class='soft-card' style='height: 100%;'>
            <div style='font-weight: 700; color: #1F4E79; font-size: 1.05rem;'>{title}</div>
            <div style='color: #6B6B6B; font-size: 0.9rem; line-height: 1.55;
                        margin-top: 0.6rem;'>{body}</div>
        </div>
        """, unsafe_allow_html=True)
