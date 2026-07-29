"""Long-form content for the About tab.

Each section includes a title, body, optional graphic, and a short tagline.
The strings are rendered as Markdown. They are deliberately written in plain
English so a non-technical reader can follow every decision behind the
project, while a professional can still recognise the technical choices.
"""

from __future__ import annotations


def _slug(title: str) -> str:
    return (
        title.lower()
        .replace(" ", "-")
        .replace("&", "and")
        .replace(",", "")
        .replace(".", "")
        .replace("?", "")
        .replace("!", "")
    )


_RAW_SECTIONS = [
    {
        "title": "What this project is",
        "tagline": "A local app that explains what is inside any English text.",
        "graphic": None,
        "body": (
            "Lexiscope is a small interactive app that takes any English text you give it "
            "and explains exactly what is inside.\n\n"
            "If you paste a news headline, it will tell you who is mentioned, which places "
            "are involved, how the sentence is structured, and which words carry the most "
            "meaning. If you paste a paragraph, it will tell you how easy it is to read, "
            "how varied the vocabulary is, and which topics come through the strongest.\n\n"
            "This is not a chatbot. It does not invent summaries. It does not guess at the "
            "meaning of what you wrote. Every piece of information in the app comes from a "
            "well-known language model trained by spaCy, an open-source library used by "
            "thousands of companies and researchers. Every observation the app shows is "
            "directly computed from the words you gave it.\n\n"
            "**The name.** Lexiscope is a coinage. "
            "**Lex-** from Latin *lexicon* (a vocabulary, a dictionary of words). "
            "**-scope** from Greek *skopein* (to look, to examine) — same ending as "
            "microscope, telescope, kaleidoscope. So: \"a device for looking at words.\" "
            "That's exactly what the app does — it shows you the structure of text you "
            "can't normally see."
        ),
    },
    {
        "title": "Why this matters",
        "tagline": "Honest analysis beats clever guessing for live demos.",
        "graphic": "tradeoff",
        "body": (
            "Most apps that say they 'understand text' are powered by a large language model "
            "behind a curtain. The model invents, hallucinates, and forgets. That is risky "
            "for any business that needs reliable answers about a document.\n\n"
            "Lexiscope uses a different approach: classical NLP. Instead of asking a model "
            "to guess, it walks through the text step by step, exactly the way a linguist "
            "would. It is fully transparent. Every entity has a label and a position. Every "
            "token has a part of speech and a dependency relation. Every score you see in the "
            "dashboard is computed from the text itself, not imagined.\n\n"
            "For a demo, this is powerful. A viewer can see the work happen, trace any "
            "result back to the words it came from, and ask 'why' without needing to "
            "trust a black box."
        ),
    },
    {
        "title": "The pipeline, step by step",
        "tagline": "Five stages turn letters into structured information.",
        "graphic": "pipeline",
        "body": (
            "When you click **Analyze text**, the app runs five stages in order. Together "
            "they turn a bag of letters into structured information you can read and export.\n\n"
            "**1. Tokenization.** The text is split into individual words and punctuation "
            "marks. Each piece is called a *token*. \"The dog is fast.\" becomes five "
            "tokens: The, dog, is, fast, and a period.\n\n"
            "**2. Lemmatization.** Each word is reduced to its dictionary form. "
            "\"running\", \"ran\", \"runs\" all become \"run\". This is what makes the "
            "app count \"is talking\" and \"talked\" as the same verb.\n\n"
            "**3. Part-of-speech tagging.** Every token is labelled with its role in the "
            "sentence. Nouns, verbs, adjectives, adverbs, prepositions, and so on. This is "
            "what powers the parts-of-speech chart.\n\n"
            "**4. Dependency parsing.** spaCy draws an arrow from each word to the word "
            "it depends on. \"The CEO announced\" has an arrow from CEO to announced, "
            "because announce is the action and CEO is the actor. This is what powers the "
            "dependency tree in the Syntax tab.\n\n"
            "**5. Named entity recognition.** spaCy scans the text and labels people, "
            "organizations, places, dates, money amounts, percentages, and so on. This is "
            "what powers the highlighted text in the Entities tab."
        ),
    },
    {
        "title": "Why two models",
        "tagline": "Speed for the warm-up, depth for the wow moment.",
        "graphic": "two_models",
        "body": (
            "The app offers two spaCy models. They are both for English, but they trade "
            "speed for depth.\n\n"
            "**en_core_web_sm (Fast).** Roughly 12 MB on disk. Loads in well under a "
            "second. Runs the five pipeline stages above. It does not include word "
            "vectors, which means it cannot tell you that 'Google' is similar to 'Microsoft' "
            "in meaning.\n\n"
            "**en_core_web_md (Accurate).** Roughly 40 MB on disk. Includes 20,000 word "
            "vectors, each a 300-dimensional mathematical snapshot of a word's meaning. "
            "With these vectors, the app can compare words for similarity and light up the "
            "Similarity tab.\n\n"
            "For a live demo, the move is to start with the Fast model to show speed, then "
            "switch to Accurate when the audience wants to see semantic understanding. "
            "Both run on a normal laptop with no internet connection."
        ),
    },
    {
        "title": "What word vectors actually are",
        "tagline": "A 300-number fingerprint for each word's meaning.",
        "graphic": "vector",
        "body": (
            "If you have not seen this idea before, here is the short version.\n\n"
            "A word vector is a list of 300 numbers, like `[0.21, -0.07, 0.89, ...]`, "
            "assigned to each word. The numbers are not random. They were learned by "
            "training on millions of sentences of text, so that words with similar meanings "
            "end up with similar numbers.\n\n"
            "Because the numbers are similar, you can measure how close two words are by "
            "doing a small piece of math called cosine similarity. The result is a number "
            "between -1 and 1. Around 0.5 means 'somewhat related', around 0.8 means "
            "'very related', and below 0.2 means 'probably unrelated'.\n\n"
            "In the Similarity tab, when you pick a word like *Google*, the app compares "
            "its vector to every other word in the document and shows the closest matches. "
            "It also compares the same vector to a curated vocabulary of common words so "
            "you can see what the model thinks is related to your chosen word."
        ),
    },
    {
        "title": "How the metrics are calculated",
        "tagline": "Every number is computed from the text. No external data.",
        "graphic": "metrics",
        "body": (
            "Every number in the dashboard is computed from the text. No external "
            "data is used. Here is exactly how each one is built.\n\n"
            "**Words.** Tokens that are not spaces and not punctuation. \"Apple\" counts "
            "as one word. \"Apple's\" counts as one word. Commas and periods do not count.\n\n"
            "**Sentences.** Sentence boundaries are detected by spaCy from the punctuation "
            "and capitalization. A sentence ends at a period, question mark, or exclamation "
            "mark, plus the right capitalization in the next word.\n\n"
            "**Entities.** The number of named entities spaCy detected. A person, an "
            "organization, a place, a date, and a money amount each count as one entity.\n\n"
            "**Reading time.** Words divided by 225, rounded up to the next minute. The "
            "average adult reads around 225 words per minute.\n\n"
            "**Lexical diversity.** The number of unique normalized words divided by the "
            "total number of words. A high number means the writer avoided repeating "
            "themselves. A low number means the text reuses the same words.\n\n"
            "**Pipeline time.** The wall-clock time the spaCy model took to process the "
            "text, measured in milliseconds. This is the metric that proves the model is "
            "fast."
        ),
    },
    {
        "title": "How the observations are written",
        "tagline": "Deterministic summaries, not LLM-composed prose.",
        "graphic": None,
        "body": (
            "In the Insights tab, every sentence you see is built from the same analysis "
            "the rest of the app uses. There is no LLM inventing takeaways.\n\n"
            "Examples you can rely on:\n\n"
            "- If the most common entity label is `ORG`, the app says \"Companies, agencies, "
            "institutions, etc. is the dominant entity class\". The label meaning is taken "
            "from spaCy's official description.\n\n"
            "- If the average sentence has 30 words, the app says the text is dense and "
            "suggests shorter sentences. If it has 8 words, the app says it is concise.\n\n"
            "- If the text contains numbers, the app lists up to five of them and notes how "
            "many more there are.\n\n"
            "- If the active model has vectors, the app points you to the Similarity tab. "
            "If it does not, the app suggests switching to en_core_web_md."
        ),
    },
    {
        "title": "How the app is built",
        "tagline": "Six small files. ~600 lines of Python.",
        "graphic": "architecture",
        "body": (
            "The codebase is small on purpose. There are six files.\n\n"
            "`app.py` is the entry point. It sets up the Streamlit page, loads the spaCy "
            "model once, and hands control to the UI module. There is no Flask, no React, "
            "no Next.js, no database. The app is a single Python process you can run on a "
            "laptop.\n\n"
            "`lexiscope/config.py` holds the model options, the demo samples, and shared "
            "constants. The samples are real paragraphs that exercise the entity and "
            "syntax pipelines.\n\n"
            "`lexiscope/analysis.py` wraps spaCy. It exposes a single `analyze_text` "
            "function that takes the input string and returns a structured result bundle. "
            "It also exposes `build_insights`, which turns the result bundle into the "
            "human-readable observations shown in the Insights tab.\n\n"
            "`lexiscope/similarity.py` contains the two vector comparison helpers: one "
            "for the document and one for a curated vocabulary.\n\n"
            "`lexiscope/report.py` converts the result bundle into JSON and CSV bytes "
            "ready for download.\n\n"
            "`lexiscope/styles.py` is the full CSS. It is one block, plain text, easy to "
            "tweak without touching component code.\n\n"
            "`lexiscope/ui.py` is the only place that knows about Streamlit. Every widget, "
            "every tab, every board is rendered from here. The pure data modules above can "
            "be tested without Streamlit, and the UI module can be redesigned without "
            "touching the analysis.\n\n"
            "The whole thing is about 600 lines of code."
        ),
    },
    {
        "title": "Run it locally",
        "tagline": "Three commands. No internet. No API key.",
        "graphic": None,
        "body": (
            "All commands assume the `NLP` conda environment.\n\n"
            "```\nconda activate NLP\npip install -r requirements.txt\n"
            "python -m spacy download en_core_web_sm\npython -m spacy download en_core_web_md\n"
            "streamlit run app.py\n```\n\n"
            "Streamlit will print a local URL, usually `http://localhost:8501`. Open it in "
            "any browser. The app processes text entirely on your machine. Nothing is "
            "uploaded to any server."
        ),
    },
    {
        "title": "What we did not use, and why",
        "tagline": "Predictability, trust, and speed over hallucination.",
        "graphic": "tradeoff",
        "body": (
            "The app could have been built with a large language model such as GPT. We "
            "chose not to. There are three reasons.\n\n"
            "**Predictability.** A large language model is a probability machine. Ask it "
            "the same question twice and you can get two different answers. For a demo "
            "where the audience is testing edge cases, this is risky. spaCy is deterministic. "
            "The same input always produces the same output.\n\n"
            "**Trust.** A large language model can invent entities that are not in the "
            "text. It can attribute quotes to the wrong person. spaCy cannot. Every label "
            "the app shows came from explicit linguistic rules and trained statistical "
            "models. If spaCy labels a word as a person, you can trust it actually "
            "identified a person-shaped token.\n\n"
            "**Speed.** A small spaCy model processes a paragraph in under ten milliseconds. "
            "A request to a large language model takes one to ten seconds, plus network "
            "latency, plus a paid API call. For a live demo, spaCy wins on speed every "
            "time.\n\n"
            "We also chose not to use a transformer model for the demo. Transformer models "
            "give better accuracy, but they are slow to load, slow to run, and require "
            "more memory. We want the audience to see responsiveness, not wait for it."
        ),
    },
    {
        "title": "The story the dashboard tells",
        "tagline": "A five-minute script for the presenter.",
        "graphic": "stages",
        "body": (
            "If you only have five minutes for the demo, here is the order to walk through.\n\n"
            "**Open and load.** Click **Load sample**. The text appears in the input box. "
            "This is the moment the audience sees the dashboard is live and friendly.\n\n"
            "**Analyze.** Click **Analyze text**. The pipeline runs in under fifty "
            "milliseconds. The **Pipeline time** metric lights up. This is the moment the "
            "audience sees the system is fast.\n\n"
            "**Overview.** The two charts show the entity distribution and the parts of "
            "speech. The metrics row shows words, sentences, entities, reading time, "
            "lexical diversity, and pipeline time. This is the moment the audience sees "
            "the system is structured.\n\n"
            "**Entities.** The text is highlighted with colour-coded entity labels. People, "
            "organizations, places, dates, money. The user can filter to focus on one "
            "type. This is the moment the audience sees the system can read.\n\n"
            "**Syntax.** A sentence is selected. The dependency graph shows which words "
            "depend on which, drawn as arrows. The token table underneath labels each "
            "word's role. This is the moment the audience sees the system understands "
            "structure.\n\n"
            "**Switch models.** Pick **Accurate (en_core_web_md)** in the sidebar and "
            "click **Analyze text** again. The pipeline time goes up slightly. The "
            "Similarity tab is now enabled. This is the moment the audience sees the system "
            "has depth.\n\n"
            "**Similarity.** Pick a word like *Google*. The app shows the closest words "
            "in the document and the closest words in the model vocabulary. Engineeer, "
            "founder, startup, platform. This is the moment the audience sees the system "
            "understands meaning.\n\n"
            "**Insights and export.** Walk through the explainable observations. The "
            "audience sees every claim is grounded. Then click **Download JSON** or "
            "**Download CSV**. The artifact is in their hands. This is the moment the "
            "audience sees the system is real."
        ),
    },
    {
        "title": "Final note",
        "tagline": "Small, honest, local.",
        "graphic": None,
        "body": (
            "Lexiscope is a small, honest app. It does one thing well: it makes the "
            "structure of English text visible. It is open, it is local, it is fast, and "
            "every result is traceable back to the words you gave it. If you want a model "
            "that can hallucinate the meaning of a novel, look elsewhere. If you want a "
            "model that can show you, with confidence, exactly what is in the text, this is "
            "it."
        ),
    },
]


ABOUT_SECTIONS = [
    {**section, "anchor": _slug(section["title"])}
    for section in _RAW_SECTIONS
]
