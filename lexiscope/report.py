"""Export helpers for JSON and CSV report downloads."""

from __future__ import annotations

import csv
import io
import json


def csv_bytes(rows: list[dict]) -> bytes:
    """Encode a list of dictionaries as a UTF-8 CSV byte string."""
    if not rows:
        return b""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def export_payload(result: dict) -> dict:
    """Assemble a JSON-serializable snapshot of the analysis."""
    return {
        "text": result["text"],
        "model": result["model"],
        "has_vectors": result["has_vectors"],
        "metrics": result["metrics"],
        "entities": result["entities"],
        "tokens": result["tokens"],
        "sentences": result["sentences"],
        "top_terms": [{"term": term, "count": count} for term, count in result["terms"]],
    }


def export_payload_bytes(result: dict) -> bytes:
    """Convenience helper for the JSON download button."""
    return json.dumps(export_payload(result), indent=2).encode("utf-8")
