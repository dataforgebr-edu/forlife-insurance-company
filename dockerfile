FROM python:3.12-slim

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root \
    && rm -rf $POETRY_CACHE_DIR

COPY README.md .
COPY projects/ ./projects/

RUN poetry install --without dev
