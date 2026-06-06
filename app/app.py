import streamlit as st
import streamlit.components.v1 as components
import pickle
import re
import os
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="SkyPulse · Flight Sentiment Analysis",
    page_icon="✈️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0c0f1a;
    --surface:   #131726;
    --surface2:  #1b2035;
    --border:    #252d45;
    --accent:    #4f8ef7;
    --accent2:   #7b5ea7;
    --pos:       #34d399;
    --neu:       #fbbf24;
    --neg:       #f87171;
    --text:      #e8eaf6;
    --muted:     #7880a0;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1100px !important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a2040 0%, #0e1628 50%, #1a1030 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3rem 3.5rem 2.5rem;
    margin: 1.5rem 0 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "✈";
    position: absolute;
    right: 2rem; top: 50%;
    transform: translateY(-50%) rotate(-15deg);
    font-size: 9rem;
    opacity: 0.04;
    pointer-events: none;
    line-height: 1;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    color: #fff;
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    margin: 0 0 0.6rem !important;
    color: #fff !important;
    letter-spacing: -0.02em;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    max-width: 520px;
    margin: 0;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    gap: 2.5rem;
    margin-top: 1.8rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}
.stat-item { display: flex; flex-direction: column; gap: 0.2rem; }
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
}
.stat-label { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Section headings ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Sample review cards ── */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.review-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    cursor: pointer;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.review-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.review-card.pos::before { background: var(--pos); }
.review-card.neu::before { background: var(--neu); }
.review-card.neg::before { background: var(--neg); }
.review-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.35);
}
.review-card.pos:hover  { border-color: var(--pos); }
.review-card.neu:hover  { border-color: var(--neu); }
.review-card.neg:hover  { border-color: var(--neg); }
.card-sentiment {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.card-sentiment.pos { color: var(--pos); }
.card-sentiment.neu { color: var(--neu); }
.card-sentiment.neg { color: var(--neg); }
.card-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    display: inline-block;
}
.pos .card-dot { background: var(--pos); }
.neu .card-dot { background: var(--neu); }
.neg .card-dot { background: var(--neg); }
.card-text {
    font-size: 0.88rem;
    color: #c5c9e0;
    line-height: 1.55;
    font-style: italic;
}
.card-action {
    margin-top: 0.9rem;
    font-size: 0.72rem;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

/* ── Text area ── */
.stTextArea > label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.06em;
}
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    resize: vertical;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
}

/* ── Analyse button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.4rem !important;
    transition: opacity 0.2s, transform 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Result card ── */
.result-card {
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}
.result-card.pos { background: rgba(52,211,153,0.08); border: 1px solid rgba(52,211,153,0.3); }
.result-card.neu { background: rgba(251,191,36,0.08);  border: 1px solid rgba(251,191,36,0.3); }
.result-card.neg { background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.3); }
.result-emoji { font-size: 3rem; margin-bottom: 0.5rem; display: block; }
.result-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0 0 0.3rem;
}
.result-card.pos .result-label { color: var(--pos); }
.result-card.neu .result-label { color: var(--neu); }
.result-card.neg .result-label { color: var(--neg); }
.result-confidence {
    font-size: 0.85rem;
    color: var(--muted);
    margin-bottom: 1.4rem;
}
.confidence-bar-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    height: 6px;
    margin-bottom: 1.5rem;
    overflow: hidden;
}
.confidence-bar { height: 100%; border-radius: 100px; transition: width 0.8s ease; }
.pos .confidence-bar  { background: var(--pos); }
.neu .confidence-bar  { background: var(--neu); }
.neg .confidence-bar  { background: var(--neg); }
.actions-heading {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
}
.action-item {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.88rem;
    color: #c5c9e0;
}
.action-item:last-child { border-bottom: none; }
.action-icon { flex-shrink: 0; margin-top: 1px; }

/* ── Probability breakdown ── */
.prob-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.82rem;
}
.prob-label { width: 70px; color: var(--muted); text-transform: capitalize; }
.prob-bar-wrap { flex: 1; background: rgba(255,255,255,0.06); border-radius: 100px; height: 5px; overflow: hidden; }
.prob-val { width: 42px; text-align: right; color: var(--text); font-weight: 500; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Word count chip ── */
.wc-chip {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 100px; padding: 0.25rem 0.8rem;
    font-size: 0.75rem; color: var(--muted);
    margin-top: 0.5rem;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* History badge */
.history-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.7rem 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
}
.history-text { color: #c5c9e0; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-right: 1rem; }
.badge { padding: 0.2rem 0.6rem; border-radius: 100px; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em; }
.badge.pos { background: rgba(52,211,153,0.15); color: var(--pos); }
.badge.neu { background: rgba(251,191,36,0.15);  color: var(--neu); }
.badge.neg { background: rgba(248,113,113,0.15); color: var(--neg); }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL AND VECTORIZER
# --------------------------------------------------

BASE_DIR = os.path.dirname(__file__)
model_path      = os.path.join(BASE_DIR, "../models/sentiment_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "../models/tfidf_vectorizer.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)
with open(vectorizer_path, "rb") as f:
    tfidf = pickle.load(f)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "review_text" not in st.session_state:
    st.session_state.review_text = ""
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------
# SAMPLE REVIEWS
# --------------------------------------------------

SAMPLES = {
    "pos": [
        "The crew was incredibly warm and the seats were more comfortable than expected. Best flight I've had all year!",
        "Smooth boarding, on-time departure, and the complimentary meal was genuinely delicious. Highly recommend this airline.",
        "Staff went above and beyond to make sure my connecting flight wasn't missed. Outstanding service from start to finish.",
        "The in-flight entertainment had a great selection and the legroom was surprisingly generous. Will definitely fly again.",
    ],
    "neu": [
        "The flight departed on time and arrived as scheduled. Nothing exceptional, but no complaints either.",
        "Check-in was straightforward and the crew was professional. A fairly standard economy experience.",
        "Baggage arrived without issues and the seat was average. The food was okay — not great, not terrible.",
        "The flight was unremarkable in both good and bad ways. Functional and efficient, which is all I needed.",
    ],
    "neg": [
        "Worst airline experience ever. We sat on the tarmac for 3 hours with zero communication from the crew.",
        "My luggage was lost and the customer service was dismissive and unhelpful. Very disappointed.",
        "The seats were broken, the food was inedible, and the cabin temperature was freezing the entire flight.",
        "Constant delays, rude staff, and my vegetarian meal request was completely ignored. Never flying again.",
    ],
}

ACTIONS = {
    "positive": [
        ("🌟", "Continue maintaining high service quality across all routes."),
        ("🎁", "Reward loyal customers through personalised loyalty programs."),
        ("📣", "Amplify positive feedback in marketing and social campaigns."),
        ("📝", "Encourage satisfied passengers to leave public reviews."),
    ],
    "neutral": [
        ("📋", "Collect targeted feedback to identify specific improvement areas."),
        ("💬", "Improve in-flight engagement with personalised passenger communication."),
        ("🔍", "Identify touchpoints where experience can be elevated from average to great."),
        ("🔄", "Design follow-up surveys to convert neutral passengers into advocates."),
    ],
    "negative": [
        ("🔎", "Investigate and document the root cause of reported issues immediately."),
        ("⚡", "Improve customer support response times and complaint resolution workflows."),
        ("📊", "Monitor recurring complaint themes to surface systemic problems."),
        ("🛠️", "Implement corrective training and service improvements on affected routes."),
    ],
}

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 1.5rem'>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:0.3rem'>✈ SkyPulse</div>
        <div style='font-size:0.75rem;color:var(--muted)'>Flight Review Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Model Details**")
    st.markdown("""
    <div style='font-size:0.82rem;color:var(--muted);line-height:2'>
                
    🤖 &nbsp; Logistic Regression<br>
    📐 &nbsp; TF-IDF Vectorization<br>
    📦 &nbsp; US Airline Tweets Dataset<br>
    🎯 &nbsp; Accuracy: <span style='color:#4f8ef7;font-weight:600'>77.87%</span><br>
    🏷️ &nbsp; Classes: Positive · Neutral · Negative
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Prediction history
    st.markdown("**Recent Predictions**")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            cls = item["cls"]
            st.markdown(f"""
            <div class="history-row">
                <div class="history-text">{item['text'][:55]}…</div>
                <span class="badge {cls}">{cls.upper()}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.8rem;color:var(--muted)'>No predictions yet.</div>", unsafe_allow_html=True)

    if st.session_state.history:
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-badge">✈ Airline Sentiment Intelligence</div>
    <h1>How Are Passengers<br>Feeling About Your Flights?</h1>
    <p>Paste any flight review below — or pick a sample card — and our NLP model instantly classifies it as Positive, Neutral, or Negative with actionable recommendations.</p>
    <div class="hero-stats">
        <div class="stat-item">
            <span class="stat-value">77.87%</span>
            <span class="stat-label">Accuracy</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">3</span>
            <span class="stat-label">Sentiment Classes</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">TF-IDF</span>
            <span class="stat-label">Vectorisation</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">LogReg</span>
            <span class="stat-label">Classifier</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SAMPLE CARDS
# --------------------------------------------------

st.markdown('<div class="section-label">✦ &nbsp; Try a Sample Review</div>', unsafe_allow_html=True)

tabs = st.tabs(["😊 Positive", "😞 Negative"])

for tab, (cls, label) in zip(tabs, [("pos","Positive"), ("neu","Neutral"), ("neg","Negative")]):
    with tab:
        cols = st.columns(2)
        for i, sample in enumerate(SAMPLES[cls]):
            with cols[i % 2]:
                if st.button(f'"{sample[:60]}…"' if len(sample) > 60 else f'"{sample}"',
                             key=f"card_{cls}_{i}",
                             help="Click to load this review"):
                    st.session_state.review_text = sample

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# INPUT + ANALYSIS
# --------------------------------------------------

st.markdown('<div class="section-label">✦ &nbsp; Enter Your Review</div>', unsafe_allow_html=True)

review = st.text_area(
    "Type or paste a flight review:",
    value=st.session_state.review_text,
    height=130,
    placeholder="e.g. The flight crew was amazing and departure was perfectly on time…",
    label_visibility="collapsed",
)

# Live word counter
word_count = len(review.strip().split()) if review.strip() else 0
st.markdown(f'<div class="wc-chip">📝 {word_count} word{"s" if word_count != 1 else ""}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
analyse = st.button("⚡ Analyse Sentiment", use_container_width=True)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if analyse:
    if not review.strip():
        st.warning("Please enter a review or select a sample card above.")
    else:
        with st.spinner("Analysing…"):
            time.sleep(0.4)  # brief dramatic pause

        cleaned = clean_text(review)
        vector  = tfidf.transform([cleaned])
        pred    = model.predict(vector)[0]
        probs   = model.predict_proba(vector)[0]
        classes = model.classes_
        conf    = max(probs) * 100

        # Map class → CSS key
        css_map  = {"positive": "pos", "neutral": "neu", "negative": "neg"}
        emoji_map = {"positive": "😊", "neutral": "😐", "negative": "😞"}
        css_cls  = css_map.get(pred, "neu")
        emoji    = emoji_map.get(pred, "😐")

        # Save to history
        st.session_state.history.append({"text": review, "cls": css_cls})

        # Result card
        actions_html = "".join(
            f'<div class="action-item"><span class="action-icon">{icon}</span><span>{text}</span></div>'
            for icon, text in ACTIONS.get(pred, [])
        )

        # Probability rows  (fully inline styles — rendered inside iframe)
        prob_bars = ""
        for c, p in sorted(zip(classes, probs), key=lambda x: -x[1]):
            bar_col = {"positive": "#34d399", "neutral": "#fbbf24", "negative": "#f87171"}.get(c, "#4f8ef7")
            prob_bars += f"""
            <div class="prob-row">
                <span class="prob-label">{c.capitalize()}</span>
                <div class="prob-bar-wrap">
                    <div style="width:{p*100:.1f}%;background:{bar_col};height:6px;border-radius:100px;"></div>
                </div>
                <span class="prob-val">{p*100:.1f}%</span>
            </div>"""

        border_color = {"pos": "rgba(52,211,153,0.35)", "neu": "rgba(251,191,36,0.35)", "neg": "rgba(248,113,113,0.35)"}.get(css_cls, "#252d45")
        bg_color     = {"pos": "rgba(52,211,153,0.07)", "neu": "rgba(251,191,36,0.07)", "neg": "rgba(248,113,113,0.07)"}.get(css_cls, "transparent")
        label_color  = {"pos": "#34d399", "neu": "#fbbf24", "neg": "#f87171"}.get(css_cls, "#e8eaf6")
        bar_color    = label_color

        components.html(f"""
<!DOCTYPE html>
<html>
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: transparent;
    font-family: 'DM Sans', sans-serif;
    color: #e8eaf6;
    padding: 0;
  }}
  .card {{
    background: {bg_color};
    border: 1px solid {border_color};
    border-radius: 16px;
    padding: 2rem 2.2rem;
    position: relative;
    overflow: hidden;
  }}
  .result-emoji {{ font-size: 2.8rem; display: block; margin-bottom: 0.4rem; line-height: 1; }}
  .result-label {{
    font-family: 'Syne', sans-serif;
    font-size: 1.75rem;
    font-weight: 800;
    color: {label_color};
    margin-bottom: 0.25rem;
  }}
  .result-confidence {{ font-size: 0.85rem; color: #7880a0; margin-bottom: 1rem; }}
  .conf-bar-wrap {{
    background: rgba(255,255,255,0.07);
    border-radius: 100px;
    height: 6px;
    margin-bottom: 1.6rem;
    overflow: hidden;
  }}
  .conf-bar {{
    height: 100%;
    border-radius: 100px;
    background: {bar_color};
    width: {conf:.1f}%;
    transition: width 0.9s ease;
  }}
  .section-head {{
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #7880a0;
    margin-bottom: 0.8rem;
  }}
  .action-item {{
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 0.875rem;
    color: #c5c9e0;
    line-height: 1.5;
  }}
  .action-item:last-child {{ border-bottom: none; }}
  .divider {{ height: 1px; background: rgba(255,255,255,0.07); margin: 1.5rem 0; }}
  .prob-row {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.65rem;
    font-size: 0.82rem;
  }}
  .prob-label {{ width: 72px; color: #7880a0; text-transform: capitalize; flex-shrink: 0; }}
  .prob-bar-wrap {{
    flex: 1;
    background: rgba(255,255,255,0.07);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
  }}
  .prob-val {{ width: 46px; text-align: right; color: #e8eaf6; font-weight: 500; }}
</style>
</head>
<body>
<div class="card">
  <span class="result-emoji">{emoji}</span>
  <div class="result-label">{pred.capitalize()} Sentiment</div>
  <div class="result-confidence">Confidence: <strong>{conf:.1f}%</strong></div>
  <div class="conf-bar-wrap"><div class="conf-bar"></div></div>

  <div class="section-head">Recommended Actions</div>
  {actions_html}

  <div class="divider"></div>

  <div class="section-head">Probability Breakdown</div>
  {prob_bars}
</div>
</body>
</html>
""", height=580, scrolling=False)