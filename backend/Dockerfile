FROM 127.0.0.1:5000/ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml uv.lock ./

RUN uv venv
RUN uv lock
RUN uv sync

COPY src/ ./src/
RUN uv pip install -e .

ENV PYTHONPATH=/app/src
EXPOSE 8000
CMD ["uv", "run", "-m", "work.main"]
