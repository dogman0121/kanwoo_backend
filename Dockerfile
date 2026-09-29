FROM python:3.14-slim AS builder

ENV POETRY_VERSION="2.2.1"
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_BIN="$POETRY_HOME/venv/bin/"
ENV PATH="$PATH:$POETRY_BIN"

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Устанавливаем Poetry через Python 3.13 из /usr/local/bin
RUN curl -sSL https://install.python-poetry.org | /usr/local/bin/python3.14 - && \
    poetry --version

COPY pyproject.toml poetry.lock ./

# Явно указываем Poetry использовать Python 3.13
RUN poetry env use /usr/local/bin/python3.14 && \
    poetry install --no-root

COPY . .

RUN mkdir -p logs static
RUN chmod +x boot.sh

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]