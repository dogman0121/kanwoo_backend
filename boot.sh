#!/bin/bash
while true; do
    flask db stamp head
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn --bind :8000 manage:app