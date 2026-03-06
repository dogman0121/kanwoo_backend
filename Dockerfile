FROM python:3.9-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME=/opt/poetry
ENV VENV_PATH=/opt/venv
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# --------------------------------
# Poetry + dependencies
# --------------------------------
FROM base AS builder

RUN apt-get update && \
    apt-get install -y curl build-essential

# Install poetry 2.x
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Disable virtualenv creation (we manage it ourselves)
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# --------------------------------
# Runtime
# --------------------------------
FROM base AS runtime

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY . .

RUN mkdir -p logs static

RUN chmod +x boot.sh

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]