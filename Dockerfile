# syntax=docker/dockerfile:1.7
# =============================================================================
#  Lexiscope -- Hugging Face Spaces Dockerfile
# =============================================================================
#  Builds a slim image that ships both spaCy English models and the Streamlit
#  app. The final image is roughly 1.1 GB. Cold start is one container pull
#  instead of "boot Python, install pip, install spaCy, download 50 MB of
#  models, parse text".
#
#  This is what Hugging Face Spaces calls a "Docker Space". To deploy:
#    1. Push this repo to GitHub.
#    2. On https://huggingface.co, create a new Space.
#    3. Choose "Docker" as the Space SDK.
#    4. Connect the GitHub repo.
#    5. Wait for the first build (~6-8 minutes).
#    6. Disable sleep mode in the Space settings so visitors don't pay a
#       cold-start penalty.
# =============================================================================

# -----------------------------------------------------------------------------
# Base image. python:3.11-slim is small and has the wheels spaCy needs.
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

# -----------------------------------------------------------------------------
# System packages. We only need the basics for spaCy and Streamlit on Linux.
# - ca-certificates: TLS for Hugging Face CLI / wget
# - build-essential + gcc: only needed for pip wheels that ship C extensions
#   (thinc, blis, pyarrow). Removed at the end to keep the image small.
# - curl: used by the healthcheck.
# -----------------------------------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        build-essential \
        gcc \
        curl \
 && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Working directory.
# -----------------------------------------------------------------------------
WORKDIR /app

# -----------------------------------------------------------------------------
# Python dependencies first. This stage is cached as long as requirements.txt
# does not change, so quick code-only rebuilds skip the slow pip install.
# -----------------------------------------------------------------------------
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# spaCy English models. We download them during the build so the runtime image
# ships with them ready. Streaming install cannot reuse them later.
# -----------------------------------------------------------------------------
RUN python -m spacy download en_core_web_sm \
 && python -m spacy download en_core_web_md \
 && python -m spacy validate

# -----------------------------------------------------------------------------
# Application code.
# -----------------------------------------------------------------------------
COPY app.py ./
COPY lexiscope ./lexiscope

# -----------------------------------------------------------------------------
# Final cleanup. build-essential and gcc were only needed for the pip wheel
# step. Removing them trims roughly 500 MB.
# -----------------------------------------------------------------------------
RUN apt-get purge -y build-essential gcc \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Streamlit configuration. Disable file watching because the production
# container does not need to react to source-file changes. Set the bind
# address to 0.0.0.0 so the HF Spaces proxy can reach the server.
# -----------------------------------------------------------------------------
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_THEME_BASE=dark

# -----------------------------------------------------------------------------
# Healthcheck. Hugging Face Spaces uses this to confirm the container is
# running. The Streamlit health endpoint at /_stcore/health returns "ok".
# -----------------------------------------------------------------------------
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl --fail --silent http://127.0.0.1:8501/_stcore/health || exit 1

EXPOSE 8501

# -----------------------------------------------------------------------------
# Entrypoint. Streamlit runs in headless mode and binds to all interfaces.
# -----------------------------------------------------------------------------
CMD ["streamlit", "run", "app.py"]
