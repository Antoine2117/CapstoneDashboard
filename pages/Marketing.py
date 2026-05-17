"""
Marketing — 8-point pre-publish checklist + interactive lift roadmap.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Marketing", page_icon="◉", layout="wide")

CHARCOAL = "#2C2925"
GOLD = "#B8945D"
WARM = "#FBF9F5"
SOFT_BEIGE = "#F0EBE0"
MUTE = "#7A736B"
BORDER = "#E5DFD3"

st.markdown(f"""
<style>
.stApp {{ background: {WARM}; }}
.main .block-container {{ padding-top: 2rem; padding-bottom: 4rem; max-width: 1100px; }}
h1, h2, h3 {{ color: {CHARCOAL} !important; font-weight: 600 !important; letter-spacing: -0.015em !important; }}
.eyebrow {{
    font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: {GOLD}; font-weight: 600; margin-bottom: 0.4rem;
}}
.lift-result {{
    font-size: 4rem; font-weight: 600; color: {GOLD};
    line-height: 1; letter-spacing: -0.02em;
}}
.lift-label {{ color: {MUTE}; font-size: 0.9rem; margin-top: 0.5rem; }}
.check-item {{
    background: white; border: 1px solid {BORDER}; border-radius: 6px;
    padding: 1rem 1.25rem; margin-bottom: 0.5rem;
    display: flex; gap: 1rem; align-items: flex-start;
}}
.check-num {{
    font-size: 1.5rem; font-weight: 600; color: {GOLD};
    line-height: 1; min-width: 2rem;
}}
.check-title {{ font-weight: 600; color: {CHARCOAL}; font-size: 0.98rem; }}
.check-body {{ color: {MUTE}; font-size: 0.85rem; line-height: 1.5; margin-top: 0.3rem; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stSidebar"] {{ background: {SOFT_BEIGE}; }}
.stSlider [data-baseweb="slider"] [role="slider"] {{ background: {GOLD} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown(f"<div class='eyebrow'>For Marketing</div>", unsafe_allow_html=True)
st.markdown("# Marketing")
st.markdown(f"<p style='color: {MUTE}; margin-top: -0.4rem;'>"
            "The 8-point pre-publish checklist and the lift roadmap.</p>",
            unsafe_allow_html=True)

st.markdown(f"<hr style='border:none; height:1px; background:{BORDER}; margin: 2rem 0;'>",
            unsafe_allow_html=True)

# ── Interactive lift roadmap ─────────────────────────────────
st.markdown("### Cumulative lift roadmap")
st.markdown(f"<p style='color: {MUTE}; margin-bottom: 1.5rem;'>"
            "Drag the slider to add features in order of model importance. "
            "Each step shows the predicted engagement lift on the median company-page post.</p>",
            unsafe_allow_html=True)

DATA = Path(__file__).parent.parent / "data"
roadmap = pd.read_csv(DATA / "roadmap_cumulative_external.csv").head(8)

feature_pretty = {
    'lex_score':     '1. Amplifier vocabulary',
    'log_chars':     '2. Post length (800–1,500 chars)',
    'mention_count': '3. Cap @-mentions at 0–1',
    'bold_unicode':  '4. Remove bold-Unicode',
    'i_density':     '5. First-person hook',
    'has_question':  '6. Add a rhetorical question',
    'hashtag_count': '7. Cap hashtags at ≤3',
    'is_case_study': '8. Case-study format',
}
roadmap['label'] = roadmap['feature_added'].map(feature_pretty).fillna(roadmap['feature_added'])

n_features = st.slider("Number of features adopted", 0, 8, 8)

# Chart
fig = go.Figure()
x_active = list(range(n_features + 1))
y_active = [0] + roadmap.head(n_features)['cumulative_median_lift_pct'].tolist()
fig.add_trace(go.Scatter(
    x=x_active, y=y_active,
    mode='lines+markers',
    line=dict(color=GOLD, width=3),
    marker=dict(size=10, color=GOLD, line=dict(color='white', width=2)),
    hovertemplate='Step %{x}: +%{y:.0f}%<extra></extra>',
    showlegend=False,
))
if n_features < 8:
    x_preview = list(range(n_features, 9))
    y_preview = ([y_active[-1]] +
                 roadmap.tail(8 - n_features)['cumulative_median_lift_pct'].tolist())
    fig.add_trace(go.Scatter(
        x=x_preview, y=y_preview,
        mode='lines+markers',
        line=dict(color=MUTE, width=1.5, dash='dot'),
        marker=dict(size=6, color=MUTE, opacity=0.4),
        hovertemplate='Step %{x}: +%{y:.0f}%<extra></extra>',
        showlegend=False,
    ))
fig.add_hline(y=72, line_dash="dot", line_color=GOLD, opacity=0.4,
              annotation_text="+72% ceiling", annotation_position="right",
              annotation_font=dict(color=GOLD, size=10))

fig.update_xaxes(
    title="",
    tickmode='array',
    tickvals=list(range(9)),
    ticktext=['Start'] + [f'Step {i}' for i in range(1, 9)],
    showgrid=False,
    color=MUTE,
)
fig.update_yaxes(title="Cumulative lift (%)", range=[0, 80], gridcolor=BORDER,
                 zeroline=False, color=MUTE)
fig.update_layout(
    height=320,
    plot_bgcolor=WARM,
    paper_bgcolor=WARM,
    font=dict(family="sans-serif", size=11, color=CHARCOAL),
    margin=dict(l=10, r=10, t=20, b=10),
)
st.plotly_chart(fig, use_container_width=True)

current = roadmap.head(n_features)['cumulative_median_lift_pct'].iloc[-1] if n_features > 0 else 0
st.markdown(f"""
<div style='text-align: center; margin: 1rem 0 2rem;'>
    <div class='lift-result'>+{current:.0f}%</div>
    <div class='lift-label'>predicted lift with {n_features} feature{'s' if n_features != 1 else ''}</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<hr style='border:none; height:1px; background:{BORDER}; margin: 2rem 0;'>",
            unsafe_allow_html=True)

# ── The 8-point checklist ────────────────────────────────────
st.markdown("### 8-point pre-publish checklist")
st.markdown(f"<p style='color: {MUTE}; margin-bottom: 1.5rem;'>"
            f"Every company-page post should score at least <strong style='color:{CHARCOAL};'>6 of 8</strong> "
            "before it ships.</p>",
            unsafe_allow_html=True)

items = [
    ("01", "Post length 800–1,500 characters",
     "Founder-voice editorial sweet spot. Too short reads as announcement; too long loses attention."),
    ("02", "Hashtag count ≤ 3",
     "More than 3 hashtags suppresses engagement in 15/15 multiverse paths."),
    ("03", "No bold-Unicode characters",
     "Stylized fonts signal 'promotional broadcast' to LinkedIn. Single strongest suppressor in the data."),
    ("04", "At least one rhetorical question",
     "Founders use questions at 5× the company-page rate. Questions invite comments."),
    ("05", "First-person hook in first line",
     "'I went to…', 'We learned…' — story before claim. Reader leans in."),
    ("06", "Mention count of 0 or 1",
     "Each additional @-tag suppresses engagement. Recommend 0 unless essential."),
    ("07", "Amplifier vocabulary present",
     "Use: leadership, journey, perspective, story. Avoid: register, click, secure your seat."),
    ("08", "Case-study or methodology format",
     "Client-as-protagonist narrative beats announcement format. Phi observes; the client carries the story."),
]

for num, title, body in items:
    st.markdown(f"""
    <div class='check-item'>
        <div class='check-num'>{num}</div>
        <div>
            <div class='check-title'>{title}</div>
            <div class='check-body'>{body}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
