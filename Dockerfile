FROM python:3.9-slim AS builder

WORKDIR /app

# Install poetry 2.x
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN mkdir -p logs static

RUN chmod +x boot.sh

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]