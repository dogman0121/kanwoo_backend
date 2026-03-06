FROM python:3.10-slim AS builder

ENV POETRY_VERSION="2.2.1"
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_BIN="$POETRY_HOME/venv/bin/"

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Install poetry 2.x
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 -

ENV PATH="$PATH:$POETRY_BIN"

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

RUN mkdir -p logs static

RUN chmod +x boot.sh

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]