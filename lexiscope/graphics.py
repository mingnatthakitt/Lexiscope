"""Inline SVG graphics used inside the About tab.

Each function returns a small, self-contained SVG markup string. They are
rendered inside a bordered card so the visuals sit on the existing dark theme.
"""

from __future__ import annotations


# ---------- Helpers ----------

def _wrapper(inner: str, height: int = 160) -> str:
    """Wrap raw SVG markup in a responsive viewBox-sized container."""
    return (
        "<div class='about-graphic'>"
        f"<svg viewBox='0 0 600 {height}' preserveAspectRatio='xMidYMid meet' "
        f"xmlns='http://www.w3.org/2000/svg' role='img'>{inner}</svg>"
        "</div>"
    )


# ---------- Section graphics ----------

def pipeline_graphic() -> str:
    """A 5-step pipeline diagram: text → tokens → tags → parse → entities."""
    steps = [
        ("1", "Tokenize", "#5C4DC8"),
        ("2", "Lemmatize", "#3C7CB8"),
        ("3", "POS tag", "#20c7b7"),
        ("4", "Parse", "#3AAE7E"),
        ("5", "Entities", "#D9923A"),
    ]
    width = 600
    margin = 30
    height = 170
    n = len(steps)
    step_w = (width - 2 * margin) / n
    parts = []
    parts.append(
        "<defs><marker id='arrow' viewBox='0 0 10 10' refX='9' refY='5' "
        "markerWidth='6' markerHeight='6' orient='auto'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#94a3b8'/>"
        "</marker></defs>"
    )
    for idx, (num, label, color) in enumerate(steps):
        center = margin + step_w * (idx + 0.5)
        parts.append(
            f"<circle cx='{center:.1f}' cy='60' r='24' fill='{color}' fill-opacity='0.18' "
            f"stroke='{color}' stroke-width='2'/>"
            f"<text x='{center:.1f}' y='67' text-anchor='middle' fill='{color}' "
            f"font-size='18' font-weight='600'>{num}</text>"
            f"<text x='{center:.1f}' y='110' text-anchor='middle' fill='#e2e8f0' "
            f"font-size='14' font-weight='500'>{label}</text>"
        )
        if idx < n - 1:
            arrow_x1 = center + 24
            arrow_x2 = center + step_w - 24
            parts.append(
                f"<line x1='{arrow_x1:.1f}' y1='60' x2='{arrow_x2 - 8:.1f}' y2='60' "
                f"stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='4 3' marker-end='url(#arrow)'/>"
            )
    parts.append(
        "<text x='30' y='150' fill='#9aa8b7' font-size='12'>"
        "Each stage hands structured information to the next."
        "</text>"
    )
    return _wrapper("".join(parts), height=height)


def two_models_graphic() -> str:
    """Side-by-side comparison of Fast (sm) and Accurate (md) models."""

    def panel(x: int, label: str, title: str, accent: str, rows: list[tuple[str, str]]) -> str:
        panel_w = 285
        parts = [
            f"<rect x='{x}' y='20' width='{panel_w}' height='130' rx='10' "
            f"fill='#111820' stroke='{accent}' stroke-opacity='0.35'/>"
        ]
        parts.append(
            f"<text x='{x + 16}' y='44' fill='{accent}' font-size='12' "
            f"font-weight='600' letter-spacing='1'>{label}</text>"
        )
        parts.append(
            f"<text x='{x + 16}' y='68' fill='#e2e8f0' font-size='18' "
            f"font-weight='700'>{title}</text>"
        )
        for i, (k, v) in enumerate(rows):
            y = 90 + i * 18
            parts.append(
                f"<text x='{x + 16}' y='{y}' fill='#9aa8b7' font-size='12'>{k}</text>"
            )
            parts.append(
                f"<text x='{x + 170}' y='{y}' fill='#e2e8f0' font-size='12' "
                f"font-weight='500'>{v}</text>"
            )
        return "".join(parts)

    inner = []
    inner.append(panel(15, "FAST", "en_core_web_sm", "#20c7b7", [
        ("Size", "~12 MB"),
        ("Loads", "<1 second"),
        ("Vectors", "No"),
        ("Use case", "Instant analysis"),
    ]))
    inner.append(panel(310, "ACCURATE", "en_core_web_md", "#D9923A", [
        ("Size", "~40 MB"),
        ("Loads", "3-5 seconds"),
        ("Vectors", "20,000 words"),
        ("Use case", "Similarity"),
    ]))
    return _wrapper("".join(inner), height=180)


def vector_graphic() -> str:
    """A 2D scatter where related words cluster near the query word."""
    width = 600
    height = 200
    cx = 300
    cy = 90
    parts = [
        "<rect x='0' y='0' width='600' height='180' fill='transparent'/>",
        "<line x1='40' y1='150' x2='580' y2='150' stroke='#1f2937' stroke-width='1'/>",
        "<line x1='40' y1='20' x2='40' y2='150' stroke='#1f2937' stroke-width='1'/>",
    ]
    parts.append(
        f"<circle cx='{cx}' cy='{cy}' r='14' fill='#20c7b7' fill-opacity='0.25' "
        f"stroke='#20c7b7' stroke-width='2'/>"
        f"<text x='{cx}' y='{cy + 4}' text-anchor='middle' fill='#20c7b7' font-size='12' "
        f"font-weight='700'>query</text>"
    )
    neighbors = [
        (220, 50, "company"),
        (380, 60, "startup"),
        (170, 110, "platform"),
        (415, 95, "product"),
        (90, 75, "engineer"),
        (485, 130, "founder"),
        (260, 140, "revenue"),
        (350, 130, "investment"),
    ]
    for x, y, label in neighbors:
        parts.append(
            f"<circle cx='{x}' cy='{y}' r='6' fill='#20c7b7' fill-opacity='0.35' "
            f"stroke='#20c7b7' stroke-width='1.5'/>"
        )
        parts.append(
            f"<line x1='{cx}' y1='{cy}' x2='{x}' y2='{y}' stroke='#20c7b7' "
            f"stroke-opacity='0.55' stroke-width='1' stroke-dasharray='2 3'/>"
        )
        parts.append(
            f"<text x='{x + 9}' y='{y + 4}' fill='#cbd5df' font-size='11'>{label}</text>"
        )
    parts.append(
        "<text x='40' y='172' fill='#9aa8b7' font-size='11'>"
        "Words near the center are similar in meaning. Real vectors live in 300 dimensions; "
        "the chart flattens one slice for the eye."
        "</text>"
    )
    return _wrapper("".join(parts), height=height)


def metrics_graphic() -> str:
    """A horizontal bar chart explaining the metrics row."""
    rows = [
        ("Words", 1.0, "#20c7b7"),
        ("Sentences", 0.45, "#3C7CB8"),
        ("Entities", 0.68, "#3AAE7E"),
        ("Reading time", 0.25, "#D9923A"),
        ("Lexical diversity", 0.78, "#5C4DC8"),
        ("Pipeline time", 0.05, "#e2e8f0"),
    ]
    track_x = 130
    track_w = 380
    parts = []
    for i, (label, scale, color) in enumerate(rows):
        y = 18 + i * 22
        bar_w = track_w * scale
        parts.append(
            f"<text x='0' y='{y + 4}' fill='#cbd5df' font-size='12'>{label}</text>"
            f"<rect x='{track_x}' y='{y - 9}' width='{bar_w:.1f}' height='14' rx='3' "
            f"fill='{color}' fill-opacity='0.55'/>"
            f"<rect x='{track_x}' y='{y - 9}' width='{track_w}' height='14' rx='3' "
            f"fill='transparent' stroke='#1f2937' stroke-width='0.5'/>"
        )
    return _wrapper("".join(parts), height=160)


def architecture_graphic() -> str:
    """A layer-cake diagram of the modules."""
    layers = [
        ("app.py", "Streamlit entry point", "#20c7b7"),
        ("lexiscope/ui.py", "UI rendering", "#3C7CB8"),
        ("lexiscope/analysis.py", "NLP pipeline", "#5C4DC8"),
        ("lexiscope/similarity.py", "Vector similarity", "#3AAE7E"),
        ("lexiscope/report.py", "JSON and CSV export", "#D9923A"),
        ("lexiscope/styles.py", "Dashboard CSS", "#e2e8f0"),
    ]
    width = 600
    inner_w = 380
    inner_x = (width - inner_w) / 2
    parts = []
    for i, (label, sub, color) in enumerate(layers):
        y = 10 + i * 26
        text_x = inner_x + 14
        sub_x = inner_x + 220
        parts.append(
            f"<rect x='{inner_x:.1f}' y='{y}' width='{inner_w}' height='20' rx='5' "
            f"fill='{color}' fill-opacity='0.13' stroke='{color}' stroke-width='1'/>"
            f"<text x='{text_x:.1f}' y='{y + 14}' fill='{color}' font-size='12' "
            f"font-weight='600'>{label}</text>"
            f"<text x='{sub_x:.1f}' y='{y + 14}' fill='#9aa8b7' font-size='11'>{sub}</text>"
        )
    return _wrapper("".join(parts), height=180)


def stages_graphic() -> str:
    """Tokenize → tag → parse → label → compare, with arrows between cards."""
    items = [
        ("00", "Tokenize"),
        ("01", "Tag roles"),
        ("02", "Parse deps"),
        ("03", "Label entities"),
        ("04", "Compare vectors"),
    ]
    width = 600
    height = 180
    n = len(items)
    margin = 16
    arrow_w = 8
    card_w = (width - 2 * margin - (n - 1) * arrow_w) / n
    parts = [
        "<defs><marker id='arrow2' viewBox='0 0 10 10' refX='9' refY='5' "
        "markerWidth='6' markerHeight='6' orient='auto'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#3C7CB8'/>"
        "</marker></defs>"
    ]
    for idx, (num, label) in enumerate(items):
        x = margin + idx * (card_w + arrow_w)
        parts.append(
            f"<rect x='{x:.1f}' y='30' width='{card_w:.1f}' height='90' rx='8' "
            f"fill='#111820' stroke='#3C7CB8' stroke-opacity='0.4'/>"
            f"<text x='{x + 12:.1f}' y='54' fill='#3C7CB8' font-size='10' "
            f"letter-spacing='1' font-weight='600'>{num}</text>"
        )
        # Split labels into two lines on the first space if longer than 8 chars
        words = label.split(" ")
        if len(words) >= 2 and len(label) > 8:
            line1 = words[0]
            line2 = " ".join(words[1:])
            parts.append(
                f"<text x='{x + 12:.1f}' y='82' fill='#e2e8f0' font-size='13' "
                f"font-weight='500'>{line1}</text>"
            )
            parts.append(
                f"<text x='{x + 12:.1f}' y='102' fill='#e2e8f0' font-size='13' "
                f"font-weight='500'>{line2}</text>"
            )
        else:
            parts.append(
                f"<text x='{x + 12:.1f}' y='90' fill='#e2e8f0' font-size='13' "
                f"font-weight='500'>{label}</text>"
            )
        if idx < n - 1:
            arrow_y = 75
            arrow_x1 = x + card_w + 1
            arrow_x2 = x + card_w + arrow_w - 1
            parts.append(
                f"<line x1='{arrow_x1:.1f}' y1='{arrow_y}' x2='{arrow_x2:.1f}' y2='{arrow_y}' "
                f"stroke='#3C7CB8' stroke-width='1.5' marker-end='url(#arrow2)'/>"
            )
    parts.append(
        f"<text x='{margin}' y='148' fill='#9aa8b7' font-size='11'>"
        "A live demo walks through these stages in roughly five minutes."
        "</text>"
    )
    return _wrapper("".join(parts), height=height)


def tradeoff_graphic() -> str:
    """Two bars per row: classical NLP vs LLM on speed, predictability, trust."""
    rows = [
        ("Speed", 0.92, 0.18),
        ("Predictability", 0.95, 0.30),
        ("Traceability", 0.90, 0.25),
    ]
    track_x = 130
    track_w = 380
    bar_h = 14
    row_gap = 48
    classify_color = "#20c7b7"
    llm_color = "#D9923A"
    parts = []
    parts.append(
        f"<text x='{track_x}' y='10' fill='{classify_color}' font-size='11' "
        f"font-weight='700' letter-spacing='1'>CLASSICAL NLP</text>"
    )
    parts.append(
        f"<text x='{track_x + 200}' y='10' fill='{llm_color}' font-size='11' "
        f"font-weight='700' letter-spacing='1'>LLM</text>"
    )
    for i, (label, classical, llm) in enumerate(rows):
        y = 24 + i * row_gap
        classical_w = track_w * classical
        llm_w = track_w * llm
        parts.append(
            f"<text x='0' y='{y + bar_h - 1}' fill='#cbd5df' font-size='12'>{label}</text>"
        )
        parts.append(
            f"<rect x='{track_x}' y='{y}' width='{classical_w:.1f}' height='{bar_h}' rx='3' "
            f"fill='{classify_color}' fill-opacity='0.55'/>"
        )
        parts.append(
            f"<rect x='{track_x + classical_w:.1f}' y='{y}' width='{track_w - classical_w:.1f}' "
            f"height='{bar_h}' rx='3' fill='#1f2937' fill-opacity='0.6'/>"
        )
        parts.append(
            f"<rect x='{track_x}' y='{y + bar_h + 4}' width='{llm_w:.1f}' height='{bar_h}' rx='3' "
            f"fill='{llm_color}' fill-opacity='0.55'/>"
        )
        parts.append(
            f"<rect x='{track_x + llm_w:.1f}' y='{y + bar_h + 4}' width='{track_w - llm_w:.1f}' "
            f"height='{bar_h}' rx='3' fill='#1f2937' fill-opacity='0.6'/>"
        )
    return _wrapper("".join(parts), height=180)


def meter_inline(value: float) -> str:
    """A tiny meter gauge for the at-a-glance header."""
    ratio = max(0.0, min(1.0, value))
    return (
        "<div class='about-meter'>"
        "<div class='about-meter-track'>"
        f"<div class='about-meter-fill' style='width:{(ratio * 100):.1f}%;'></div>"
        "</div>"
        "</div>"
    )
