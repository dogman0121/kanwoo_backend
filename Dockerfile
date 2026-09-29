FROM python:3.13-slim AS builder

# Setting up poetry 
ENV POETRY_VERSION="2.2.1"
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_BIN="$POETRY_HOME/venv/bin/"
ENV PATH="$PATH:$POETRY_BIN"

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Install poetry 2.x
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 -

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

# Make logs and static folders
RUN mkdir -p logs static

# Start boot script
RUN chmod +x boot.sh

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]