"""Lexiscope - interactive NLP analysis dashboard."""

from .config import MAX_CHARACTERS, MODEL_OPTIONS, DEFAULT_MODEL_LABEL, SAMPLES
from .analysis import analyze_text, build_insights
from .similarity import similar_inside_doc, similar_in_vocab
from .report import csv_bytes, export_payload
from .about import ABOUT_SECTIONS

__all__ = [
    "MAX_CHARACTERS",
    "MODEL_OPTIONS",
    "DEFAULT_MODEL_LABEL",
    "SAMPLES",
    "analyze_text",
    "build_insights",
    "similar_inside_doc",
    "similar_in_vocab",
    "csv_bytes",
    "export_payload",
    "ABOUT_SECTIONS",
]
