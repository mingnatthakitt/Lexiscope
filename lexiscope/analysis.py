"""Text analysis pipeline built on spaCy."""

from __future__ import annotations

import math
import time
from collections import Counter

import spacy
from spacy.language import Language
from spacy.tokens import Doc


def content_tokens(doc: Doc) -> list:
    """Tokens excluding whitespace and punctuation."""
    return [token for token in doc if not token.is_space and not token.is_punct]


def build_token_rows(doc: Doc) -> list[dict]:
    """Return the token-level annotations used in the Tokens explorer."""
    return [
        {
            "Token": token.text,
            "Lemma": token.lemma_,
            "POS": token.pos_,
            "Tag": token.tag_,
            "Dependency": token.dep_,
            "Head": token.head.text,
            "Entity": token.ent_type_ or "-",
            "Shape": token.shape_,
            "Stop word": token.is_stop,
            "Punctuation": token.is_punct,
        }
        for token in doc
        if not token.is_space
    ]


def build_entity_rows(doc: Doc) -> list[dict]:
    """Return the named entity annotations used in the Entities tab."""
    return [
        {
            "Text": entity.text,
            "Label": entity.label_,
            "Meaning": spacy.explain(entity.label_) or entity.label_,
            "Start": entity.start_char,
            "End": entity.end_char,
        }
        for entity in doc.ents
    ]


def top_terms(doc: Doc, limit: int = 12) -> list[tuple[str, int]]:
    """Return the most content-dense normalized terms in the document."""
    terms = [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha and not token.is_stop and len(token.text) > 2
    ]
    return Counter(terms).most_common(limit)


def analyze_text(text: str, nlp: Language) -> dict:
    """Run the NLP pipeline and assemble a result bundle for the UI."""
    started = time.perf_counter()
    doc = nlp(text)
    elapsed_ms = (time.perf_counter() - started) * 1_000

    words = content_tokens(doc)
    sentences = list(doc.sents) if doc.has_annotation("SENT_START") else []
    unique_lemmas = {token.lemma_.lower() for token in words if token.is_alpha}
    lexical_diversity = len(unique_lemmas) / max(1, sum(token.is_alpha for token in words))

    entity_rows = build_entity_rows(doc)
    token_rows = build_token_rows(doc)

    sentence_rows = [
        {
            "Sentence": index + 1,
            "Words": len(content_tokens(sentence)),
            "Text": sentence.text.strip(),
        }
        for index, sentence in enumerate(sentences)
    ]

    return {
        "doc": doc,
        "text": text,
        "metrics": {
            "words": len(words),
            "tokens": len([token for token in doc if not token.is_space]),
            "sentences": len(sentences),
            "entities": len(entity_rows),
            "reading_minutes": max(1, math.ceil(len(words) / 225)),
            "lexical_diversity": lexical_diversity,
            "average_sentence_length": len(words) / max(1, len(sentences)),
            "processing_ms": elapsed_ms,
        },
        "entities": entity_rows,
        "tokens": token_rows,
        "sentences": sentence_rows,
        "entity_counts": Counter(row["Label"] for row in entity_rows),
        "pos_counts": Counter(token.pos_ for token in words),
        "terms": top_terms(doc),
        "has_vectors": nlp.meta.get("vectors", {}).get("vectors", 0) > 0,
    }


def build_insights(result: dict) -> list[str]:
    """Explainable observations derived from spaCy annotations."""
    metrics = result["metrics"]
    entity_counts = result["entity_counts"]
    doc = result["doc"]
    insights: list[str] = []

    if entity_counts:
        label, count = entity_counts.most_common(1)[0]
        meaning = spacy.explain(label) or label
        insights.append(f"{meaning.capitalize()} is the dominant entity class, appearing {count} time(s).")
    else:
        insights.append(
            "No named entities were detected. The text may be generic, very short, or outside the model's domain."
        )

    average = metrics["average_sentence_length"]
    if average >= 25:
        insights.append(
            f"Sentence structure is dense at {average:.1f} words per sentence. Shortening sentences may improve readability."
        )
    elif average <= 10:
        insights.append(f"Sentence structure is concise at {average:.1f} words per sentence.")
    else:
        insights.append(f"Sentence length is moderate at {average:.1f} words per sentence.")

    numbers = [token.text for token in doc if token.like_num]
    if numbers:
        preview = ", ".join(numbers[:5])
        suffix = "" if len(numbers) <= 5 else f" and {len(numbers) - 5} more"
        insights.append(f"The document contains {len(numbers)} numerical reference(s): {preview}{suffix}.")

    if result["terms"]:
        insights.append(
            "Prominent content terms include " + ", ".join(term for term, _ in result["terms"][:5]) + "."
        )

    insights.append(
        f"Lexical diversity is {metrics['lexical_diversity']:.0%}, based on unique normalized words divided by alphabetic words."
    )
    if result["has_vectors"]:
        insights.append("Word vectors are enabled. Similarity comparisons are available in the Similarity tab.")
    else:
        insights.append(
            "The active model does not ship word vectors. Switch to en_core_web_md for similarity comparisons."
        )
    return insights
