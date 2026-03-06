FROM python:3.9-slim AS python-base
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv \
    POETRY_VERSION=2.2.1
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"

FROM python-base AS poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
    \
    # install poetry - uses $POETRY_VERSION internally
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && mv /root/.poetry $POETRY_PATH \
    && poetry --version \
    \
    # configure poetry & make a virtualenv ahead of time since we only need one
    && python -m venv $VENV_PATH \
    && poetry config settings.virtualenvs.create false \
    \
    # cleanup
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-ansi -vvv


FROM python-base AS runtime

COPY kanwoo kanwoo

WORKDIR /kanwoo

RUN mkdir "logs" -p
RUN mkdir "static" -p

COPY migrations migrations

COPY manage.py config.py boot.sh ./

RUN chmod a+x boot.sh

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]