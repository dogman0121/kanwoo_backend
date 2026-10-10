import subprocess
import sys
import signal

from .utils.compose_down import compose_down
from .utils.compose_up import compose_up
from .utils.upgrade_database import upgrade_database
from .utils.seed_database import seed_database

COMPOSE_FILE = "docker/docker-compose.dev.yml"

def flask_run():
    return subprocess.run(
        ["flask", "run", "-h", "0.0.0.0", "-p", "5000"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def handle_gracefull_down(*args, **kwargs):

    compose_down(COMPOSE_FILE)

    sys.exit(0)

def main():
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, handle_gracefull_down)

    up_process = compose_up(COMPOSE_FILE)

    if up_process.returncode != 0:
        compose_down(COMPOSE_FILE)
        raise BrokenPipeError("Не получилось запустить Docker контейнер.")

    try:
        upgrade_process = upgrade_database()

        if upgrade_process.returncode != 0:
            raise BrokenPipeError("Невозможно применить миграции")

        seed_database()

        if up_process.returncode == 0:
            flask_run()
    finally:
        compose_down(COMPOSE_FILE)