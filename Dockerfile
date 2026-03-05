FROM python:3.9-slim-bullseye

COPY kanwoo kanwoo

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

RUN mkdir "logs"
RUN mkdir "static"

COPY migrations migrations
COPY manage.py config.py boot.sh ./
RUN chmod a+x boot.sh

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]