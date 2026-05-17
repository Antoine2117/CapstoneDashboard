"""
Marketing page — 8-point pre-publish checklist, lift roadmap, content family playbook.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (
    page_header, sidebar_branding, sidebar_footer, password_gate,
    big_stat, style_chart, NAVY, AMBER, SUCCESS, WARN, MUTE, CREAM, RULE,
    load_roadmap,
)

st.set_page_config(page_title="Marketing · Phi LinkedIn", page_icon="✍️", layout="wide")
password_gate()
sidebar_branding()
sidebar_footer()

page_header("Marketing",
            "Editorial rules from the model",
            "The 8-point pre-publish checklist, the lift roadmap showing which features matter most, "
            "and the content-family playbook.")

# ── Top KPI strip ───────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: big_stat("+72%", "Predicted engagement lift<br>if company page reformats", color=SUCCESS)
with c2: big_stat("+58%", "Easy win from 3 changes<br>rule-based, no rewrite", color=AMBER)
with c3: big_stat("8 of 8", "Pre-publish checklist<br>≥6/8 before publication", color=NAVY)
with c4: big_stat("R² = 0.786", "Model explanatory power<br>cross-validated", color=NAVY)

st.markdown("<hr class='hairline'>", unsafe_allow_html=True)

# ── The interactive lift roadmap ────────────────────────────────────
st.markdown("## The cumulative lift roadmap")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "Use the slider to see which features matter most. Move the cursor right to add features "
    "in order of model importance. Each step shows the cumulative predicted engagement lift "
    "on the median company-page post.</div>",
    unsafe_allow_html=True)

roadmap = load_roadmap()

# Pretty feature names
feature_pretty = {
    'lex_score':         '1.  Amplifier vocabulary',
    'log_chars':         '2.  Post length (800–1,500 chars)',
    'mention_count':     '3.  Cap @-mentions at 0–1',
    'bold_unicode':      '4.  Remove bold-Unicode',
    'i_density':         '5.  First-person hook',
    'has_question':      '6.  Add a rhetorical question',
    'hashtag_count':     '7.  Cap hashtags at ≤3',
    'is_case_study':     '8.  Case-study format',
}
roadmap['feature_label'] = roadmap['feature_added'].map(feature_pretty).fillna(roadmap['feature_added'])

n_features = st.slider(
    "Number of features adopted",
    min_value=0, max_value=8, value=8, step=1,
    help="0 = baseline (no changes). 8 = full checklist adopted.",
)

# Build the chart up to n_features
roadmap_show = roadmap.head(8).copy()
roadmap_show['active'] = roadmap_show['step'] <= n_features

fig = go.Figure()

# Active portion of the line
active_x = list(range(n_features + 1))
active_y = [0] + roadmap_show.head(n_features)['cumulative_median_lift_pct'].tolist()
fig.add_trace(go.Scatter(
    x=active_x, y=active_y,
    mode='lines+markers',
    line=dict(color=AMBER, width=4),
    marker=dict(size=12, color=AMBER, line=dict(color='white', width=2)),
    name='Cumulative lift',
    hovertemplate='Step %{x}<br>+%{y:.0f}% lift<extra></extra>',
))

# Faded preview of remaining steps
if n_features < 8:
    preview_x = list(range(n_features, 9))
    preview_y = ([roadmap_show.head(n_features)['cumulative_median_lift_pct'].iloc[-1]
                  if n_features > 0 else 0]
                 + roadmap_show.tail(8 - n_features)['cumulative_median_lift_pct'].tolist())
    fig.add_trace(go.Scatter(
        x=preview_x, y=preview_y,
        mode='lines+markers',
        line=dict(color=MUTE, width=2, dash='dot'),
        marker=dict(size=8, color=MUTE, opacity=0.4),
        name='If you adopt more',
        hovertemplate='Step %{x}<br>+%{y:.0f}% lift<extra></extra>',
    ))

# Reference lines
fig.add_hline(y=58, line_dash="dash", line_color=AMBER, opacity=0.4,
              annotation_text="+58% — three rule-based wins",
              annotation_font_color=AMBER, annotation_font_size=11)
fig.add_hline(y=72, line_dash="dash", line_color=SUCCESS, opacity=0.4,
              annotation_text="+72% — full ceiling",
              annotation_font_color=SUCCESS, annotation_font_size=11)

# X axis labels
fig.update_xaxes(
    tickmode='array',
    tickvals=list(range(9)),
    ticktext=['Baseline'] + [f"Step {i}" for i in range(1, 9)],
)
fig.update_yaxes(title="Cumulative predicted lift (%)", range=[0, 85])
fig.update_layout(
    height=420,
    showlegend=False,
    title=None,
)
fig = style_chart(fig)
st.plotly_chart(fig, use_container_width=True)

# Current cumulative lift number
if n_features > 0:
    current_lift = roadmap_show.head(n_features)['cumulative_median_lift_pct'].iloc[-1]
else:
    current_lift = 0

st.markdown(f"""
<div style='display: flex; justify-content: center; gap: 3rem; margin: 1.5rem 0;'>
    <div style='text-align: center;'>
        <div style='font-size: 0.8rem; color: #6B6B6B; letter-spacing: 0.05em;
                    text-transform: uppercase; font-weight: 600;'>With {n_features} feature{'s' if n_features != 1 else ''}</div>
        <div style='font-size: 4rem; font-weight: 800; color: #C08552;
                    line-height: 1; letter-spacing: -0.02em;'>+{current_lift:.0f}%</div>
        <div style='font-size: 0.85rem; color: #6B6B6B; margin-top: 0.3rem;'>predicted lift</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── The 8-point checklist ───────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## The 8-point pre-publish checklist")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "Every company-page post must score at least <strong>6 out of 8</strong> before publication. "
    "Use the checklist as a live editorial gate.</div>",
    unsafe_allow_html=True)

checklist = [
    ("01", "Post length 800–1,500 characters",
     "Founder-voice editorial sweet spot. Too short reads as announcement; too long loses scroll attention."),
    ("02", "Hashtag count ≤ 3",
     "Bold-Unicode and high hashtag count are the two strongest suppressors in the model. 15/15 multiverse paths."),
    ("03", "No bold-Unicode characters",
     "Those stylized fonts signal 'promotional broadcast' to LinkedIn's ranking model. Single most robust finding."),
    ("04", "At least one rhetorical question or CTA-style ask",
     "Founders use questions at 5× the company page's rate. Questions invite comments, comments amplify reach."),
    ("05", "First-person or named-individual hook in the first line",
     "'I went to...', 'We learned...', 'Sarah told me...' — story before claim. Reader leans in."),
    ("06", "Mention count of 0 or 1",
     "Each additional @-tag suppresses engagement. The model recommends 0; 1 is acceptable when essential."),
    ("07", "Amplifier vocabulary score > 0",
     "Use leadership, journey, perspective, story, ambiguity. Avoid promotional, register, click, secure your seat."),
    ("08", "Case-study or methodology format",
     "Client-as-protagonist narrative beats announcement format. Phi observes; the client carries the story."),
]

# 2-column grid of checklist items
for i in range(0, 8, 2):
    c1, c2 = st.columns(2)
    for col, (num, title, body) in zip([c1, c2], checklist[i:i+2]):
        with col:
            st.markdown(f"""
            <div class='soft-card' style='min-height: 120px;'>
                <div style='display: flex; gap: 0.8rem; align-items: flex-start;'>
                    <div style='font-size: 1.5rem; font-weight: 800; color: #C08552;
                                line-height: 1; min-width: 2rem;'>{num}</div>
                    <div>
                        <div style='font-weight: 700; color: #1F4E79; font-size: 1rem;'>{title}</div>
                        <div style='color: #6B6B6B; font-size: 0.85rem; line-height: 1.5;
                                    margin-top: 0.4rem;'>{body}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Content family playbook ─────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## Content-family playbook")
st.markdown(
    "<div style='color: #6B6B6B; margin-bottom: 1rem;'>"
    "Six content families emerged from K-means clustering on TF-IDF vectors (K=14, aggregated by inspection). "
    "Median engagement varies 8× from top to bottom.</div>",
    unsafe_allow_html=True)

families = pd.DataFrame([
    {"family": "Founder thought leadership", "median": 237, "tier": "Reach engine", "what": "Sunday Coffee, executive commentary — long-form, named-individual voice"},
    {"family": "Founder editorial",          "median": 220, "tier": "Reach engine", "what": "Personal narrative, observations, contrarian takes"},
    {"family": "Methodology / case study",   "median": 50,  "tier": "Conversion engine", "what": "How Phi works, anonymized client stories — institutional voice OK"},
    {"family": "Client showcase",            "median": 50,  "tier": "Conversion engine", "what": "Named client wins, ROI stories, programme outcomes"},
    {"family": "Internal / culture",         "median": 22,  "tier": "Brand maintenance", "what": "Team birthdays, anniversaries, culture posts — keep, but don't over-publish"},
    {"family": "Programme recruitment",      "median": 30,  "tier": "Failing", "what": "Announcement-format posts — REWRITE as case studies"},
])

fig = go.Figure()
colors_by_tier = {
    "Reach engine": NAVY,
    "Conversion engine": AMBER,
    "Brand maintenance": MUTE,
    "Failing": WARN,
}
fig.add_trace(go.Bar(
    y=families['family'],
    x=families['median'],
    orientation='h',
    marker=dict(color=[colors_by_tier[t] for t in families['tier']]),
    text=families['median'],
    textposition='outside',
    textfont=dict(size=12, color=NAVY),
    hovertemplate='<b>%{y}</b><br>Median: %{x}<br>%{customdata}<extra></extra>',
    customdata=families['tier'],
))
fig.update_yaxes(categoryorder='total ascending', title="")
fig.update_xaxes(title="Median weighted engagement per post")
fig.update_layout(height=380, showlegend=False, title=None)
fig = style_chart(fig)
st.plotly_chart(fig, use_container_width=True)

# Family details table
st.dataframe(
    families[['family', 'tier', 'median', 'what']].rename(columns={
        'family': 'Content family',
        'tier': 'Strategic role',
        'median': 'Median engagement',
        'what': 'What it is',
    }),
    use_container_width=True,
    hide_index=True,
)

# ── The 90-day calendar ─────────────────────────────────────────────
st.markdown("<hr class='hairline'>", unsafe_allow_html=True)
st.markdown("## The 90-day rollout calendar")

cal = [
    ("Days 0–30", "Reformat",
     ["Train content team on the 8-point checklist",
      "Reformat 12 existing company-page posts as case studies",
      "Brief 8 BD targets from the priority intersection",
      "Track checklist score per post (target ≥6/8)"]),
    ("Days 31–60", "HR/L&D Sprint",
     ["Publish 6 HR-functional posts from founder pages",
      "Topics: succession, calibration, pipeline diagnostics, capability mapping",
      "Continue outreach + book meetings with priority targets",
      "Track audience-function shift weekly"]),
    ("Days 61–90", "Measurement",
     ["Cross-reference high-intent list against CRM deal flow",
      "Re-run engagement model with impressions data (once available)",
      "Validate +20% engagement target on reformatted posts",
      "Publish full 90-day report to leadership"]),
]
for phase, headline, items in cal:
    st.markdown(f"""
    <div class='soft-card'>
        <div style='display: flex; align-items: baseline; gap: 1rem;'>
            <div style='font-size: 0.75rem; font-weight: 600; color: #C08552;
                        letter-spacing: 0.1em; text-transform: uppercase;'>{phase}</div>
            <div style='font-size: 1.2rem; font-weight: 700; color: #1F4E79;'>{headline}</div>
        </div>
        <ul style='color: #0B1E33; line-height: 1.7; margin-top: 0.5rem;'>
            {''.join(f'<li>{item}</li>' for item in items)}
        </ul>
    </div>
    """, unsafe_allow_html=True)
