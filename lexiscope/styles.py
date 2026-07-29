"""Dashboard styling and typography constants."""

PAGE_CSS = """
<style>
:root {
    --accent: #20c7b7;
    --accent-soft: rgba(32, 199, 183, 0.18);
    --accent-2: #3C7CB8;
    --accent-3: #3AAE7E;
    --accent-4: #D9923A;
    --accent-5: #5C4DC8;
    --surface: #111820;
    --surface-2: #0d141c;
    --border: rgba(148, 163, 184, 0.18);
    --border-strong: rgba(148, 163, 184, 0.28);
    --muted: #9aa8b7;
    --text: #e2e8f0;
}

/* ---------- Base layout ---------- */
.stApp { background: #091017; color: var(--text); }
.block-container {
    max-width: 1440px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
h1, h2, h3, h4, h5 {
    letter-spacing: -0.025em;
    color: #f1f5f9;
}
h1 { margin-bottom: 0.4rem; }
h2 { margin: 0 0 0.6rem; }
h3 { margin: 0 0 0.5rem; }
p { margin: 0 0 0.6rem; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { background: transparent; }
hr { margin: 1.4rem 0 1.2rem; border-color: var(--border); }

/* ---------- Hero / status ---------- */
.hero-copy {
    color: var(--muted);
    max-width: 780px;
    margin: 0 0 0.85rem 0;
    line-height: 1.55;
}
.status-line {
    display: flex;
    gap: 0.85rem;
    align-items: center;
    flex-wrap: wrap;
    color: var(--muted);
    font-size: 0.82rem;
    margin: 0.25rem 0 1.5rem;
    padding: 0.45rem 0.85rem;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--surface-2);
}
.status-dot {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 0 4px var(--accent-soft);
    flex-shrink: 0;
}
.status-line > span:not(.status-dot) + span:not(.status-dot)::before {
    content: "·";
    margin-right: 0.85rem;
    color: var(--border-strong);
}

/* ---------- Panels ---------- */
.panel-note {
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    background: var(--surface);
    color: #cbd5df;
    line-height: 1.45;
    font-size: 0.9rem;
}
.panel-note strong { color: #e2e8f0; }

.insight {
    border-left: 3px solid var(--accent);
    background: var(--surface);
    padding: 0.85rem 1rem;
    margin: 0.55rem 0;
    border-radius: 0 12px 12px 0;
    color: #d6dee8;
    line-height: 1.5;
}

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    min-height: 92px;
}
[data-testid="stMetricValue"] {
    color: #eefcf9;
    font-weight: 600;
    font-size: 1.35rem;
    line-height: 1.15;
    word-break: break-word;
}
[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ---------- Buttons ---------- */
.stButton > button {
    border-radius: 10px;
    min-height: 2.6rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    border: 1px solid var(--border-strong);
    background: var(--surface);
    color: var(--text);
    transition: transform 0.12s ease, background 0.12s ease, border-color 0.12s ease;
}
.stButton > button:hover {
    border-color: var(--accent);
    color: var(--accent);
}
.stButton > button:active {
    transform: translateY(1px);
}
.stButton > button[kind="primary"] {
    background: var(--accent);
    color: #04110f;
    border: 1px solid var(--accent);
}
.stButton > button[kind="primary"]:hover {
    background: #43d6c7;
    color: #04110f;
    border-color: #43d6c7;
}
div[data-testid="stDownloadButton"] button {
    width: 100%;
    border-radius: 10px;
}

/* ---------- Inputs ---------- */
.stTextArea textarea,
.stTextInput input,
.stSelectbox [data-baseweb="select"] {
    border-radius: 12px !important;
    border-color: var(--border) !important;
    background: var(--surface) !important;
    color: var(--text) !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
.stTextArea label,
.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stRadio label,
[data-baseweb="popover"] {
    color: var(--muted) !important;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.stCaption, [data-testid="stCaption"] {
    color: var(--muted) !important;
}

/* ---------- Top-level section picker ---------- */
[data-testid="stRadio"] {
    margin-bottom: 0.25rem;
}
[data-testid="stRadio"] > label {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 0 !important;
}
[data-testid="stRadio"] [data-baseweb="radio"] {
    display: none !important;
}
[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}
[data-testid="stRadio"] label > div:last-child {
    text-transform: none !important;
    letter-spacing: 0.02em !important;
    font-size: 0.95rem !important;
    padding: 0.45rem 1.1rem !important;
    border-radius: 999px !important;
    border: 1px solid var(--border) !important;
    background: var(--surface-2) !important;
    color: var(--muted) !important;
    transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}
[data-testid="stRadio"] label:hover > div:last-child {
    border-color: var(--accent) !important;
    color: var(--text) !important;
}
[data-testid="stRadio"] [aria-checked="true"] > div:last-child {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #04110f !important;
}

/* ---------- Sub tab label ---------- */
.subtab-label {
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin: 1.4rem 0 0.6rem;
    border-top: 1px solid var(--border);
    padding-top: 0.85rem;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.25rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.25rem;
    margin-bottom: 1.25rem;
    overflow-x: auto;
    flex-wrap: nowrap;
}
.stTabs [data-baseweb="tab"] {
    padding: 0.6rem 0;
    background: transparent;
    border: none;
    color: var(--muted);
    font-weight: 500;
    white-space: nowrap;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text); }
.stTabs [aria-selected="true"] {
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 0.5rem;
}

/* ---------- displaCy output ---------- */
.entity-panel, .syntax-panel {
    overflow-x: auto;
    overflow-y: hidden;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    background: var(--surface-2);
    margin-bottom: 1rem;
}
.entity-panel { line-height: 2.4; }
.entity-panel .entities { line-height: 2.4; }
.syntax-panel svg { max-width: 100%; height: auto; }
.syntax-panel svg text { fill: #dce7ef; font-size: 13px; }
.syntax-panel svg path { stroke: #6ee7d6; }
.syntax-panel svg .arcs path { stroke: #94a3b8; }

/* ---------- DataFrames ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

/* ---------- About tab graphics ---------- */
.about-eyebrow {
    color: var(--accent);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.about-page-card {
    border: 1px solid var(--border);
    border-radius: 14px;
    background: var(--surface);
    padding: 1rem 1.2rem;
    margin: 1.6rem 0 1rem;
    position: relative;
}
.about-graphic {
    border: 1px solid var(--border);
    border-radius: 14px;
    background: var(--surface-2);
    padding: 1rem 1.2rem;
    margin: 0 0 1rem;
    overflow-x: auto;
}
.about-graphic svg {
    width: 100%;
    min-width: 600px;
    max-height: 240px;
    display: block;
}
.about-foot {
    margin-top: 1.5rem;
    padding: 0.7rem 1rem;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.85rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
}
.about-foot-link {
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.15s ease;
}
.about-foot-link:hover {
    color: #43d6c7;
    text-decoration: underline;
}
.about-foot-divider {
    color: var(--border-strong);
}
.about-page-card h3 { color: #f1f5f9; }
.about-counter {
    position: absolute;
    top: 1rem;
    right: 1.2rem;
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.about-anchor {
    display: block;
    position: relative;
    top: -1rem;
    visibility: hidden;
}

/* ---------- About in-page nav ---------- */
.about-nav {
    border: 1px solid var(--border);
    border-radius: 14px;
    background: var(--surface);
    padding: 0.85rem 1rem;
    margin: 1rem 0 0.5rem;
    position: sticky;
    top: 0.5rem;
    z-index: 10;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}
.about-nav-label {
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    font-weight: 600;
}
.about-nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.4rem 0.7rem;
}
.about-nav-link {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.4rem 0.6rem;
    border-radius: 8px;
    color: var(--muted);
    text-decoration: none;
    font-size: 0.85rem;
    border: 1px solid transparent;
    transition: background 0.12s ease, border-color 0.12s ease, color 0.12s ease;
}
.about-nav-link:hover {
    background: var(--surface-2);
    border-color: var(--border);
    color: var(--text);
}
.about-nav-num {
    color: var(--accent);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
.about-nav-title {
    color: inherit;
    line-height: 1.3;
}

/* ---------- Responsive ---------- */
@media (max-width: 1200px) {
    .block-container { padding-left: 1.4rem; padding-right: 1.4rem; }
    [data-testid="stMetricValue"] { font-size: 1.2rem; }
}
@media (max-width: 1024px) {
    .block-container { padding-left: 1.1rem; padding-right: 1.1rem; }
    [data-testid="stMetric"] { min-height: 84px; padding: 0.7rem 0.85rem; }
    [data-testid="stMetricValue"] { font-size: 1.1rem; }
}
@media (max-width: 768px) {
    .block-container { padding: 1rem 0.9rem 2rem; }
    .status-line { gap: 0.5rem; font-size: 0.78rem; }
    [data-testid="stMetric"] { padding: 0.65rem 0.8rem; min-height: 72px; }
    [data-testid="stMetricValue"] { font-size: 1rem; }
    h1 { font-size: 1.7rem; }
    .panel-note { font-size: 0.85rem; }
    [data-testid="stRadio"] label { padding: 0.35rem 0.85rem !important; font-size: 0.85rem !important; }
}
</style>
"""
