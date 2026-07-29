"""Render the Streamlit UI for the dashboard."""

from __future__ import annotations

import streamlit as st
from spacy import displacy

from .analysis import analyze_text, build_insights
from .config import DEFAULT_MODEL_LABEL, MAX_CHARACTERS, MODEL_OPTIONS, SAMPLES
from .graphics import (
    architecture_graphic,
    metrics_graphic,
    pipeline_graphic,
    stages_graphic,
    tradeoff_graphic,
    two_models_graphic,
    vector_graphic,
)
from .report import csv_bytes, export_payload_bytes
from .similarity import similar_in_vocab, similar_inside_doc
from .styles import PAGE_CSS
from .about import ABOUT_SECTIONS


SECTION_OPTIONS = ["About", "Analyze"]
ANALYSIS_TABS = [
    "Overview",
    "Entities",
    "Syntax",
    "Similarity",
    "Tokens",
    "Insights & export",
]


def _similarity_chip_html(words: list[str]) -> str:
    """Return HTML for the vocabulary neighbor chips."""
    return " ".join(
        "<span style='display:inline-block;margin:.18rem .3rem;padding:.35rem .7rem;"
        "border-radius:999px;background:var(--surface);border:1px solid var(--border);"
        "color:#e2e8f0;font-size:.85rem;line-height:1'>{word}</span>".format(word=word)
        for word in words
    )


def _graphic_for(name: str) -> str:
    return {
        "pipeline": pipeline_graphic,
        "two_models": two_models_graphic,
        "vector": vector_graphic,
        "metrics": metrics_graphic,
        "architecture": architecture_graphic,
        "stages": stages_graphic,
        "tradeoff": tradeoff_graphic,
    }.get(name, lambda: "")()


def _render_overview(result: dict) -> None:
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.subheader("Entity distribution")
        if result["entity_counts"]:
            st.bar_chart(dict(result["entity_counts"]), horizontal=True)
        else:
            st.info("No named entities were detected in this text.")
    with right:
        st.subheader("Parts of speech")
        st.bar_chart(dict(result["pos_counts"]), horizontal=True)

    terms_col, sentences_col = st.columns([1, 2], gap="large")
    with terms_col:
        st.subheader("Key terms")
        if result["terms"]:
            st.dataframe(
                [{"Term": term, "Count": count} for term, count in result["terms"]],
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No meaningful content terms were found.")
    with sentences_col:
        st.subheader("Sentence profile")
        st.dataframe(result["sentences"], hide_index=True, use_container_width=True)


def _render_entities(result: dict) -> None:
    st.subheader("Named entity recognition")
    if not result["entities"]:
        st.info("No entities were found. Try a text containing people, companies, places, dates, or quantities.")
        return

    entity_labels = sorted({row["Label"] for row in result["entities"]})
    chosen_labels = st.multiselect("Filter entity labels", entity_labels, default=entity_labels)
    filtered_entities = [row for row in result["entities"] if row["Label"] in chosen_labels]
    entity_html = displacy.render(
        result["doc"],
        style="ent",
        options={"ents": chosen_labels},
        page=False,
    )
    st.markdown(f"<div class='entity-panel'>{entity_html}</div>", unsafe_allow_html=True)
    st.dataframe(filtered_entities, hide_index=True, use_container_width=True)


def _render_syntax(result: dict) -> None:
    st.subheader("Dependency structure")
    if not result["doc"].has_annotation("DEP"):
        st.info("The active pipeline does not provide dependency parsing.")
        return

    sentences = list(result["doc"].sents)
    sentence_number = st.selectbox(
        "Sentence",
        range(len(sentences)),
        format_func=lambda index: f"{index + 1}. {sentences[index].text[:100]}",
    )
    dependency_html = displacy.render(
        sentences[sentence_number],
        style="dep",
        options={"compact": True, "distance": 105, "bg": "#091017", "color": "#dce7ef"},
        page=False,
    )
    st.markdown(f"<div class='syntax-panel'>{dependency_html}</div>", unsafe_allow_html=True)
    st.dataframe(
        [
            {
                "Token": token.text,
                "Relation": token.dep_,
                "Head": token.head.text,
                "POS": token.pos_,
            }
            for token in sentences[sentence_number]
        ],
        hide_index=True,
        use_container_width=True,
    )


def _render_similarity(result: dict, nlp) -> None:
    st.subheader("Semantic similarity")
    if not result["has_vectors"]:
        st.info(
            f"The active model ({result['model']}) does not include word vectors. "
            "Switch to en_core_web_md and click Analyze text to enable similarity."
        )
        return

    candidate_tokens = [
        token for token in result["doc"]
        if token.is_alpha and not token.is_stop and token.has_vector
    ]
    if not candidate_tokens:
        st.info("No content words with vectors were found in this text.")
        return

    token_choices = [token.text for token in candidate_tokens]
    query_token = st.selectbox(
        "Pick a word to compare",
        token_choices,
        key="similarity_word",
        help="Similarity uses the spaCy word vectors in the active model.",
    )
    with st.spinner("Comparing vectors..."):
        in_doc = similar_inside_doc(result["doc"], query_token)
        vocab_neighbors = similar_in_vocab(nlp, query_token)

    sim_left, sim_right = st.columns([1, 1], gap="large")
    with sim_left:
        st.markdown("Closest words in this document")
        if in_doc:
            st.dataframe(
                [{"Word": word, "Similarity": f"{score:.2f}"} for word, score in in_doc],
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No comparable words were found in this document.")
    with sim_right:
        st.markdown("Closest words in the model vocabulary")
        if vocab_neighbors:
            st.markdown(
                f"<div class='panel-note'>{_similarity_chip_html(vocab_neighbors)}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.info("No comparable vocabulary entries were found.")


def _render_tokens(result: dict) -> None:
    st.subheader("Token explorer")
    search = st.text_input("Search tokens or lemmas", placeholder="Try: company")
    token_rows = result["tokens"]
    if search:
        query = search.casefold()
        token_rows = [
            row for row in token_rows
            if query in row["Token"].casefold() or query in row["Lemma"].casefold()
        ]
    st.caption(f"Showing {len(token_rows):,} of {len(result['tokens']):,} tokens")
    st.dataframe(token_rows, hide_index=True, use_container_width=True, height=460)


def _render_insights_and_export(result: dict) -> None:
    insights_col, export_col = st.columns([2, 1], gap="large")
    with insights_col:
        st.subheader("Explainable observations")
        for insight in build_insights(result):
            st.markdown(f'<div class="insight">{insight}</div>', unsafe_allow_html=True)
        st.caption("Observations are deterministic summaries of spaCy annotations, not generative AI output.")
    with export_col:
        st.subheader("Export analysis")
        st.download_button(
            "Download JSON",
            data=export_payload_bytes(result),
            file_name="lexiscope-analysis.json",
            mime="application/json",
            use_container_width=True,
        )
        st.download_button(
            "Download tokens CSV",
            data=csv_bytes(result["tokens"]),
            file_name="lexiscope-tokens.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.download_button(
            "Download entities CSV",
            data=csv_bytes(result["entities"]),
            file_name="lexiscope-entities.csv",
            mime="text/csv",
            use_container_width=True,
            disabled=not result["entities"],
        )


def _render_metrics(result: dict, target_model: str) -> None:
    metrics = result["metrics"]
    st.markdown(
        "<div class='panel-note' style='display:inline-block;padding:0.55rem 0.9rem;margin:0 0 1rem 0;'>"
        "<span style='color:var(--muted);font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;'>Model</span>"
        "&nbsp;&nbsp;<strong>{model}</strong>"
        "&nbsp;&nbsp;<span style='color:var(--muted);font-size:0.85rem;'>· {vectors}</span>"
        "</div>".format(
            model=result["model"],
            vectors="word vectors enabled" if result["has_vectors"] else "no word vectors",
        ),
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(6, gap="small")
    metric_values = [
        ("Words", f"{metrics['words']:,}"),
        ("Sentences", f"{metrics['sentences']:,}"),
        ("Entities", f"{metrics['entities']:,}"),
        ("Reading time", f"{metrics['reading_minutes']} min"),
        ("Lexical diversity", f"{metrics['lexical_diversity']:.0%}"),
        ("Pipeline time", f"{metrics['processing_ms']:.1f} ms"),
    ]
    for column, (label, value) in zip(metric_columns, metric_values):
        column.metric(label, value)

    if result["model"] != target_model:
        st.info(
            f"The active model is {result['model']}. Switch to {target_model} and rerun analysis to refresh results."
        )


def _render_empty_state() -> None:
    st.divider()
    st.subheader("Ready for analysis")
    st.write("Use the prepared sample or paste your own text. Results remain available while you explore the dashboard.")


def _render_about() -> None:
    intro = st.columns([3, 2], gap="large")
    with intro[0]:
        st.markdown(
            "<div class='about-eyebrow'>Lexiscope · Project readme</div>"
            "<h2 style='margin:0.3rem 0 0.6rem;'>What this project is, "
            "why it exists, and how it works.</h2>"
            "<p class='hero-copy'>A walkthrough written for everyone. "
            "No technical background required. Read in order, or jump to any section "
            "from the nav below.</p>",
            unsafe_allow_html=True,
        )
    with intro[1]:
        st.markdown(
            "<div class='panel-note'>"
            "<strong>At a glance</strong><br>"
            "<span style='color:var(--muted);'>English text in · structured information out</span><br>"
            "<span style='color:var(--muted);'>Two spaCy models · runs locally</span><br>"
            "<span style='color:var(--muted);'>No LLM · no internet · no black box</span>"
            "</div>"
            "<div class='panel-note' style='margin-top:0.6rem;'>"
            "<strong>How to read</strong><br>"
            "<span style='color:var(--muted);'>Each section has a tagline, a graphic, "
            "and a short essay. The graphic is the takeaway; the essay is the proof.</span>"
            "</div>",
            unsafe_allow_html=True,
        )

    _render_about_nav(ABOUT_SECTIONS)

    for index, section in enumerate(ABOUT_SECTIONS):
        st.markdown(
            f"<a id='{section['anchor']}' class='about-anchor'></a>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='about-page-card'>"
            f"<div class='about-eyebrow'>{section['tagline']}</div>"
            f"<h3 style='margin:0.25rem 0 0.4rem;'>{section['title']}</h3>"
            f"<div class='about-counter'>{index + 1} of {len(ABOUT_SECTIONS)}</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if section.get("graphic"):
            st.markdown(_graphic_for(section["graphic"]), unsafe_allow_html=True)
        st.markdown(section["body"])

        next_section = ABOUT_SECTIONS[(index + 1) % len(ABOUT_SECTIONS)]
        st.markdown(
            f"<div class='about-foot'>"
            f"<a href='#about-nav-top' class='about-foot-link'>↑ Back to top</a>"
            f"<span class='about-foot-divider'>·</span>"
            f"Next: <a href='#{next_section['anchor']}' class='about-foot-link'>"
            f"{next_section['title']} →</a>"
            f"</div>",
            unsafe_allow_html=True,
        )


def _render_about_nav(sections: list[dict]) -> None:
    """Render an in-page anchor nav linking to each section."""
    items = "".join(
        f"<a class='about-nav-link' href='#{section['anchor']}'>"
        f"<span class='about-nav-num'>{i + 1:02d}</span>"
        f"<span class='about-nav-title'>{section['title']}</span>"
        f"</a>"
        for i, section in enumerate(sections)
    )
    st.markdown(
        "<a id='about-nav-top' class='about-anchor'></a>"
        "<nav class='about-nav' aria-label='On this page'>"
        "<div class='about-nav-label'>On this page</div>"
        f"<div class='about-nav-grid'>{items}</div>"
        "</nav>",
        unsafe_allow_html=True,
    )


def _render_input_controls() -> tuple[str, str, str, bool]:
    cols = st.columns([3, 1], gap="large")
    with cols[1]:
        st.markdown("<div class='about-eyebrow'>Inputs</div>", unsafe_allow_html=True)
        selected_sample = st.selectbox("Demo sample", list(SAMPLES), key="sample_name")
        if st.button("Load sample", use_container_width=True):
            st.session_state.input_text = SAMPLES[selected_sample]
            st.session_state.analysis = None
            st.rerun()
        selected_model_label = st.selectbox(
            "spaCy model",
            list(MODEL_OPTIONS),
            key="model_label",
            help="Fast model for instant analysis. Accurate model adds word vectors and similarity.",
        )
        st.markdown(
            "<div class='panel-note'>"
            "<strong>Demo flow</strong><br>"
            "Load a sample, analyze it, then move through entities, syntax, similarity, and export."
            "</div>",
            unsafe_allow_html=True,
        )
    with cols[0]:
        st.markdown("<div class='about-eyebrow'>Text</div>", unsafe_allow_html=True)
        text = st.text_area(
            "Text to analyze",
            key="input_text",
            height=180,
            max_chars=MAX_CHARACTERS,
            label_visibility="collapsed",
            help=f"English text, up to {MAX_CHARACTERS:,} characters.",
        )
        action_col, count_col = st.columns([1, 3], gap="small")
        with action_col:
            analyze_clicked = st.button("Analyze text", type="primary", use_container_width=True)
        with count_col:
            st.caption(f"{len(text):,} / {MAX_CHARACTERS:,} characters")
    return text, selected_sample, selected_model_label, analyze_clicked


def _run_analysis(text: str, nlp, target_model_name: str) -> None:
    cleaned = text.strip()
    if not cleaned:
        st.warning("Enter text or load a demo sample before running the analysis.")
        return
    if len(cleaned) > MAX_CHARACTERS:
        st.error(f"Text must be {MAX_CHARACTERS:,} characters or fewer.")
        return

    with st.status("Running the linguistic pipeline...", expanded=False) as status:
        try:
            result = analyze_text(cleaned, nlp)
            result["model"] = target_model_name
            st.session_state.analysis = result
            status.update(label=f"Analysis complete with {target_model_name}", state="complete")
        except Exception as error:
            st.session_state.analysis = None
            status.update(label="Analysis failed", state="error")
            st.error(f"The text could not be analyzed: {error}")


def _render_analyze_section(nlp, target_model_name: str) -> None:
    text, _sample, _selected_model_label, analyze_clicked = _render_input_controls()

    try:
        active_nlp = nlp
    except Exception:
        active_nlp = None

    if analyze_clicked and active_nlp is not None:
        _run_analysis(text, active_nlp, target_model_name)

    result = st.session_state.analysis

    if result is not None:
        _render_metrics(result, target_model_name)
    else:
        _render_empty_state()

    st.markdown("<div class='subtab-label'>Analysis views</div>", unsafe_allow_html=True)
    overview, entities, syntax, similarity, tokens, insights = st.tabs(ANALYSIS_TABS)

    with overview:
        if result is None:
            st.info("Run an analysis to see the overview.")
        else:
            _render_overview(result)
    with entities:
        if result is None:
            st.info("Run an analysis to see named entities.")
        else:
            _render_entities(result)
    with syntax:
        if result is None:
            st.info("Run an analysis to see dependency structure.")
        else:
            _render_syntax(result)
    with similarity:
        if result is None:
            st.info("Run an analysis to see semantic similarity.")
        else:
            _render_similarity(result, nlp)
    with tokens:
        if result is None:
            st.info("Run an analysis to search tokens.")
        else:
            _render_tokens(result)
    with insights:
        if result is None:
            st.info("Run an analysis to see insights and export.")
        else:
            _render_insights_and_export(result)


def render_app(load_model) -> None:
    """Render the dashboard. The model loader is injected so it can be cached."""
    st.set_page_config(
        page_title="Lexiscope | Interactive NLP Analysis",
        page_icon="◈",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    st.title("Lexiscope")
    st.markdown(
        '<p class="hero-copy">Turn unstructured English text into explainable linguistic signals in seconds.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="status-line"><span class="status-dot"></span><span>Local spaCy pipeline</span>'
        '<span>Switch models any time</span><span>No data leaves this app</span></div>',
        unsafe_allow_html=True,
    )

    if "input_text" not in st.session_state:
        st.session_state.input_text = SAMPLES["Product launch"]
    if "model_label" not in st.session_state:
        st.session_state.model_label = DEFAULT_MODEL_LABEL
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "section" not in st.session_state:
        st.session_state.section = "Analyze"

    section = st.radio(
        "Section",
        SECTION_OPTIONS,
        key="section",
        horizontal=True,
        label_visibility="collapsed",
    )

    st.divider()

    target_model_name = MODEL_OPTIONS[st.session_state.model_label]

    if section == "Analyze":
        try:
            nlp = load_model(target_model_name)
        except OSError:
            st.error(
                f"The spaCy model '{target_model_name}' is not installed. Run: "
                f"`conda activate NLP && python -m spacy download {target_model_name}`"
            )
            st.stop()
        except Exception as error:
            st.error(f"The NLP pipeline could not start: {error}")
            st.stop()
        _render_analyze_section(nlp, target_model_name)
    else:
        _render_about()
