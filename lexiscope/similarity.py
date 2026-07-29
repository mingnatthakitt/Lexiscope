"""Word-vector similarity helpers."""

from __future__ import annotations

from spacy.language import Language
from spacy.tokens import Doc


def similar_inside_doc(doc: Doc, term: str, limit: int = 6) -> list[tuple[str, float]]:
    """Return the words in the document most similar to a chosen term."""
    target = None
    for token in doc:
        if token.text == term:
            target = token
            break
    if target is None or not target.has_vector:
        return []

    scored = []
    for token in doc:
        if token.i == target.i or not token.has_vector or token.is_punct or token.is_space:
            continue
        scored.append((token.text, float(token.similarity(target))))
    scored.sort(key=lambda item: -item[1])
    return scored[:limit]


# A curated vocabulary of common, audience-friendly words. Comparing against
# this list keeps the "neighbors" panel relevant to typical demo topics
# (business, finance, science, places, etc.) instead of returning raw 20k-vector
# noise.
REFERENCE_WORDS = [
    "company", "business", "corporation", "industry", "market", "startup",
    "office", "headquarters", "campus", "factory", "lab", "laboratory",
    "growth", "profit", "revenue", "sales", "demand", "investment",
    "technology", "innovation", "software", "platform", "product",
    "research", "study", "trial", "patient", "doctor", "scientist",
    "finance", "banking", "shares", "stock", "trader", "currency",
    "germany", "france", "japan", "brazil", "europe", "asia",
    "engineer", "manager", "analyst", "ceo", "founder", "investor",
    "vehicle", "battery", "network", "service", "customer", "client",
    "education", "university", "student", "teacher", "school",
    "energy", "climate", "environment", "pollution", "sustainability",
    "health", "medicine", "treatment", "vaccine", "drug",
    "president", "politician", "policy", "government", "election",
    "music", "movie", "television", "sport", "football", "olympics",
    "food", "coffee", "tea", "restaurant", "chef", "recipe",
    "travel", "flight", "airport", "hotel", "tourism",
]


def similar_in_vocab(nlp: Language, term: str, limit: int = 8) -> list[str]:
    """Return the curated vocabulary words most similar to a chosen term."""
    query = nlp(term)[0]
    if not query.has_vector or query.vector_norm == 0:
        return []

    query_norm = query.vector_norm
    query_unit = query.vector / query_norm
    scored = []
    for word in REFERENCE_WORDS:
        if word.casefold() == term.casefold():
            continue
        token = nlp(word)[0]
        if not token.has_vector or token.vector_norm == 0:
            continue
        score = float((token.vector / token.vector_norm) @ query_unit)
        scored.append((word, score))
    scored.sort(key=lambda item: -item[1])
    return [word for word, _ in scored[:limit]]
