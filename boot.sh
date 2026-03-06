#!/bin/bash

poetry install --no-interaction

while true; do
    poetry run flask db upgrade

    if [[ "$?" == "0" ]]; then
        break
    fi

    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

exec poetry run gunicorn --bind :8000 manage:app