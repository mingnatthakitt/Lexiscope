"""Streamlit entry point for the Lexiscope NLP dashboard."""

from __future__ import annotations

import streamlit as st

from lexiscope.ui import render_app


@st.cache_resource(show_spinner=False)
def load_model(model_name: str):
    import spacy

    return spacy.load(model_name)


render_app(load_model)
