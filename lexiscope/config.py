"""Static configuration shared across the dashboard."""

from __future__ import annotations

MODEL_OPTIONS = {
    "Fast (en_core_web_sm)": "en_core_web_sm",
    "Accurate (en_core_web_md)": "en_core_web_md",
}
DEFAULT_MODEL_LABEL = "Fast (en_core_web_sm)"

MAX_CHARACTERS = 20_000

SAMPLES = {
    "Product launch": (
        "Google CEO Sundar Pichai announced new AI features in Mountain View on Tuesday. "
        "The company plans to invest $2 billion in cloud infrastructure and expects revenue "
        "to grow by 20% in the third quarter. Analysts at Morgan Stanley called the strategy ambitious."
    ),
    "Market report": (
        "Tesla shares rose 4.7% in New York after the company reported 443,956 vehicle deliveries. "
        "Chief Financial Officer Vaibhav Taneja said lower battery costs improved margins across Europe "
        "and North America, although demand in China remained uneven."
    ),
    "Science brief": (
        "Researchers at the University of Cambridge published a study in Nature Medicine on Monday. "
        "The trial followed 1,250 patients for three years and found that the new screening method "
        "identified early-stage disease six months sooner than conventional tests."
    ),
}
