"""
Analytics page — variance decomposition, multiverse, audience overlap.
For the analyst inside the firm who wants to see the model behind the recommendations.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import (
    page_header, sidebar_branding, sidebar_footer, password_gate,
    big_stat, style_chart, NAVY, AMBER, SUCCESS, WARN, MUTE, CREAM, RULE,
    load_multiverse, load_audience_overlap, load_power_audience,
)

st.set_page_config(page_title="Analytics · Phi LinkedIn", page_icon="📊", layout="wide")
password_gate()
sidebar_branding()
sidebar_footer()

page_header("Analytics",
            "The model behind the recommendations",
            "Variance decomposition, multiverse robustness, audience segmentation. "
            "For the analyst who wants to inspect the work.")

# ── KPI strip ───────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: big_stat("0.786", "Cross-validated R²<br>5-fold, log-weighted", color=NAVY)
with c2: big_stat("19", "Features<br>linguistic + structural", color=NAVY)
with c3: big_stat("α = 10", "Ridge regularization<br>selected via CV", color=NAVY)
with c4: big_stat("29 / 30", "Multiverse paths<br>support founder-company gap", color=SUCCESS)

st.markdown("<hr class='hairline'>", unsafe_allow_html=True)

# ── Variance decomposition ──────────────────────────────────────────
st.markdown("## Variance decomposition")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "Of the 78.6% of engagement variance the model explains, "
    "<strong>86% is shared between author and content</strong>. "
    "After controlling for what each page publishes, the pure author effect is small. "
    "<em>The bottleneck isn't who writes — it's what gets written.</em></div>",
    unsafe_allow_html=True)

variance = pd.DataFrame([
    {"segment": "Shared (author + content)", "pct": 64.9, "color": AMBER},
    {"segment": "Unexplained",                "pct": 21.5, "color": MUTE},
    {"segment": "Unique to author",           "pct": 8.8,  "color": NAVY},
    {"segment": "Unique to content",          "pct": 4.9,  "color": "#2c6ba4"},
])

fig = go.Figure()
fig.add_trace(go.Bar(
    y=['Variance'],
    x=variance['pct'],
    name='',
    orientation='h',
    text=[f"{seg}<br>{p:.1f}%" for seg, p in zip(variance['segment'], variance['pct'])],
    textposition='inside',
    textfont=dict(size=12, color='white', family='Inter'),
    marker=dict(color=variance['color']),
    hovertemplate='%{text}<extra></extra>',
))

# This needs to be stacked, not grouped. Use separate traces:
fig = go.Figure()
left = 0
for _, row in variance.iterrows():
    fig.add_trace(go.Bar(
        y=['Variance'],
        x=[row['pct']],
        orientation='h',
        name=row['segment'],
        marker=dict(color=row['color']),
        text=f"<b>{row['pct']:.1f}%</b><br>{row['segment']}",
        textposition='inside',
        textfont=dict(size=13, color='white', family='Inter'),
        insidetextanchor='middle',
        hovertemplate=f"<b>{row['segment']}</b><br>{row['pct']:.1f}% of variance<extra></extra>",
    ))
fig.update_layout(
    barmode='stack',
    height=150,
    showlegend=False,
    xaxis=dict(showticklabels=False, range=[0, 100], showgrid=False),
    yaxis=dict(showticklabels=False, showgrid=False),
    margin=dict(l=10, r=10, t=10, b=10),
    plot_bgcolor=CREAM,
    paper_bgcolor=CREAM,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Multiverse robustness ───────────────────────────────────────────
st.markdown("## Multiverse robustness")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "30 analytical paths. Each varies the engagement metric, outlier handling, and baseline. "
    "Hover any dot for that path's configuration. "
    "<strong>29 of 30 paths</strong> show the founder-to-company gap holds.</div>",
    unsafe_allow_html=True)

mv = load_multiverse()

# Separate by baseline
ceo_baseline = mv[mv['baseline'].str.contains('Micheline', case=False, na=False)].copy()
phi_baseline = mv[mv['baseline'].str.contains('Phi', case=False, na=False)].copy()

# Build the scatter
fig = go.Figure()

# CEO baseline (amber, top half) — these are < 1.0 when gap holds
np.random.seed(0)
ceo_baseline = ceo_baseline.sort_values('ratio')
ceo_y = np.linspace(0.65, 0.95, len(ceo_baseline))

# CEO baseline points
fig.add_trace(go.Scatter(
    x=ceo_baseline['ratio'],
    y=ceo_y,
    mode='markers',
    marker=dict(
        size=14, color=AMBER, line=dict(color='white', width=1.5),
        opacity=[0.9 if h else 0.35 for h in ceo_baseline['gap_holds']],
    ),
    name='CEO baseline',
    hovertemplate=(
        '<b>CEO baseline</b><br>'
        'Metric: %{customdata[0]}<br>'
        'Outlier drop: %{customdata[1]:.0%}<br>'
        'Compared to: %{customdata[2]}<br>'
        'Ratio: %{x:.3f}<br>'
        'Supports gap: %{customdata[3]}<extra></extra>'
    ),
    customdata=ceo_baseline[['metric', 'outlier_drop_pct', 'compared_to', 'gap_holds']].values,
))

# Phi baseline (navy, bottom half)
phi_baseline = phi_baseline.sort_values('ratio')
phi_y = np.linspace(0.2, 0.45, len(phi_baseline))

fig.add_trace(go.Scatter(
    x=phi_baseline['ratio'],
    y=phi_y,
    mode='markers',
    marker=dict(
        size=14, color=NAVY, line=dict(color='white', width=1.5),
        opacity=[0.9 if h else 0.35 for h in phi_baseline['gap_holds']],
    ),
    name='Phi page baseline',
    hovertemplate=(
        '<b>Phi page baseline</b><br>'
        'Metric: %{customdata[0]}<br>'
        'Outlier drop: %{customdata[1]:.0%}<br>'
        'Compared to: %{customdata[2]}<br>'
        'Ratio: %{x:.3f}<br>'
        'Supports gap: %{customdata[3]}<extra></extra>'
    ),
    customdata=phi_baseline[['metric', 'outlier_drop_pct', 'compared_to', 'gap_holds']].values,
))

# Threshold lines
fig.add_vline(x=0.67, line_dash='dash', line_color=WARN, opacity=0.7)
fig.add_vline(x=1.5, line_dash='dash', line_color=WARN, opacity=0.7,
              annotation_text="Gap thresholds (0.67 / 1.5)",
              annotation_font_color=WARN, annotation_font_size=11)
fig.add_vline(x=1.0, line_color=MUTE, opacity=0.4,
              annotation_text="Equal engagement", annotation_position="top",
              annotation_font_color=MUTE, annotation_font_size=10)

# Annotations
fig.add_annotation(x=0.025, y=0.82, text="15 paths with CEO as baseline<br>(ratio < 0.67 supports gap)",
                   showarrow=False, font=dict(color=AMBER, size=11, family='Inter'),
                   align='left', xanchor='left')
fig.add_annotation(x=0.025, y=0.32, text="15 paths with Phi as baseline<br>(ratio > 1.5 supports gap)",
                   showarrow=False, font=dict(color=NAVY, size=11, family='Inter'),
                   align='left', xanchor='left')

fig.update_xaxes(type='log', title='Founder-to-company-page engagement ratio (log scale)',
                 showgrid=True, gridcolor=RULE, range=[np.log10(0.015), np.log10(100)])
fig.update_yaxes(showticklabels=False, range=[0.05, 1.05], showgrid=False)
fig.update_layout(height=400, showlegend=True,
                  legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center'),
                  title=None)
fig = style_chart(fig)
st.plotly_chart(fig, use_container_width=True)

# ── Multiverse summary stats ────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1: big_stat(f"{int(mv['gap_holds'].sum())}", "Paths support gap<br>out of 30", color=SUCCESS)
with m2: big_stat(f"{100*mv['gap_holds'].mean():.0f}%", "Robustness rate<br>highly significant", color=SUCCESS)
with m3: big_stat("5 × 3 × 2", "Dimensions varied<br>metric × outlier × baseline", color=NAVY)
with m4: big_stat("1", "Failing path<br>shares-only, 10% drop", color=WARN)

st.markdown("<hr class='hairline'>", unsafe_allow_html=True)

# ── Audience overlap ────────────────────────────────────────────────
st.markdown("## Audience overlap across Phi's three voices")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "3,718 unique external reactors classified by which of Phi's three pages they engage with. "
    "<strong>84%</strong> engage with only one page. <strong>158 people</strong> engage with all three "
    "— and they average ~20× more reactions per person than single-touch reactors.</div>",
    unsafe_allow_html=True)

overlap = load_audience_overlap()

if 'segment' in overlap.columns:
    seg_counts = overlap['segment'].value_counts().reset_index()
    seg_counts.columns = ['segment', 'count']
    seg_counts['pct'] = 100 * seg_counts['count'] / seg_counts['count'].sum()

    # Color segments
    color_map = {
        'CEO only': NAVY,
        'Mark only': NAVY,
        'Phi page only': NAVY,
        'CEO + Mark': "#5b88b3",
        'CEO + Phi page': "#5b88b3",
        'Mark + Phi page': "#5b88b3",
        'All three': AMBER,
        'No engagement': MUTE,
    }
    seg_counts['color'] = seg_counts['segment'].map(color_map).fillna(MUTE)

    seg_counts = seg_counts.sort_values('count', ascending=True)

    fig = go.Figure(go.Bar(
        y=seg_counts['segment'],
        x=seg_counts['count'],
        orientation='h',
        marker=dict(color=seg_counts['color']),
        text=[f"{c:,}  ({p:.1f}%)" for c, p in zip(seg_counts['count'], seg_counts['pct'])],
        textposition='outside',
        textfont=dict(size=12, color=NAVY),
        hovertemplate='<b>%{y}</b><br>%{x:,} reactors (%{customdata:.1f}%)<extra></extra>',
        customdata=seg_counts['pct'],
    ))
    fig.update_xaxes(title='Number of unique reactors')
    fig.update_yaxes(title='')
    fig.update_layout(height=400, showlegend=False, title=None)
    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

# ── The brand-loyal core ────────────────────────────────────────────
st.markdown("""
<div class='soft-card highlight'>
    <div style='font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em;
                text-transform: uppercase; color: #C08552;'>The brand-loyal core</div>
    <div style='display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; margin-top: 1rem;
                align-items: center;'>
        <div>
            <div style='font-size: 4.5rem; font-weight: 800; color: #C08552; line-height: 1;'>~20×</div>
            <div style='color: #6B6B6B; font-size: 0.9rem; margin-top: 0.5rem;'>
                Reactions per person among the 158-person "all three voices" segment
                versus any single-touch reactor segment.
            </div>
        </div>
        <div>
            <div style='color: #0B1E33; line-height: 1.7;'>
                The 158 are <strong style='color: #1F4E79;'>4.2% of the audience</strong>
                but contribute disproportionately to the engagement signal.<br>
                <strong style='color: #1F4E79;'>22%</strong> of Phi-page reactors also engage with the CEO —
                the addressable bridge for transformation.<br>
                <strong style='color: #1F4E79;'>0.7%</strong> of Phi-page reactors also engage with Mark —
                cross-promotion is required, not assumed.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Models inventory ────────────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## Models inventory")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "Every model used in the capstone, with its purpose and key parameters.</div>",
    unsafe_allow_html=True)

models = pd.DataFrame([
    {"Model": "Ridge regression with author FE",
     "Purpose": "Decompose engagement variance · counterfactual lift",
     "Parameters": "α = 10 (RidgeCV, 5-fold), 19 features, log-weighted outcome",
     "Output": "R² = 0.786 · +72% counterfactual"},
    {"Model": "LDA (content clustering)",
     "Purpose": "Cluster 270 posts into 6 content families",
     "Parameters": "K = 14, max_iter=100, batch · CountVectorizer (1,2)-grams",
     "Output": "6 named families: founder, methodology, culture, etc."},
    {"Model": "LDA (comment topics)",
     "Purpose": "Cluster 3,275 comments into 12 topics",
     "Parameters": "K = 12, max_iter=50, batch · TF-IDF (1,2)-grams",
     "Output": "4 high-intent topics (42.4% of all comments)"},
    {"Model": "KMeans (lexical signature)",
     "Purpose": "Derive amplifier/suppressor vocabulary for Ridge feature lex_score",
     "Parameters": "K = 20, n_init=20, TF-IDF (1,2)-grams",
     "Output": "Lex_score feature used in Ridge model"},
    {"Model": "VADER sentiment",
     "Purpose": "Score sentiment of 2,212 external comments",
     "Parameters": "Rule-based, no tuning · compound score on [-1, +1]",
     "Output": "82.3% positive · mean compound +0.541"},
    {"Model": "Twitter-RoBERTa transformer",
     "Purpose": "Cross-validate VADER on stratified sample",
     "Parameters": "cardiffnlp/twitter-roberta-base-sentiment-latest",
     "Output": "Confirms VADER is fit-for-purpose"},
    {"Model": "Multiverse robustness",
     "Purpose": "Test founder-company gap across 30 analytical paths",
     "Parameters": "5 metrics × 3 outlier strategies × 2 baselines = 30 paths",
     "Output": "29/30 paths support gap (97%)"},
    {"Model": "OLS time-series regression",
     "Purpose": "Test engagement decline significance",
     "Parameters": "scipy.stats.linregress on monthly aggregates",
     "Output": "Slope = −349/month, p = 0.008"},
])

st.dataframe(
    models,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Model": st.column_config.TextColumn(width="medium"),
        "Purpose": st.column_config.TextColumn(width="large"),
        "Parameters": st.column_config.TextColumn(width="large"),
        "Output": st.column_config.TextColumn(width="large"),
    },
)
