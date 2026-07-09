FROM python:3.11-slim

LABEL org.opencontainers.image.title="OpenUWOC-AI"
LABEL org.opencontainers.image.description="Reproducible container for simulation-first UWOC research experiments."
LABEL org.opencontainers.image.source="https://github.com/panagiotagrosdouli/OpenUWOC-AI"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY openuwoc_ai ./openuwoc_ai
COPY configs ./configs
COPY scripts ./scripts
COPY tests ./tests

RUN pip install --upgrade pip \
    && pip install -e .[dev]

CMD ["python", "scripts/run_experiment.py", "configs/coastal_ook_baseline.yaml", "--output", "results/coastal_ook_baseline.csv"]
