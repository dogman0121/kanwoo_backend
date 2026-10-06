import subprocess
import sys
import signal

from .utils.compose_down import compose_down
from .utils.compose_up import compose_up

COMPOSE_FILE = "docker/docker-compose.dev.yml"

def flask_run():
    return subprocess.run(
        ["flask", "run", "-h", "0.0.0.0", "-p", "5000"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def seed_database():
    pass

def handle_gracefull_down(*args, **kwargs):

    return compose_down(COMPOSE_FILE)

def main():
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, handle_gracefull_down)

    up_process = compose_up(COMPOSE_FILE)

    seed_database()

    if up_process.returncode == 0:
        flask_run()

    compose_down(COMPOSE_FILE)