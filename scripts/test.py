import subprocess
import sys

from .utils.compose_up import compose_up
from .utils.compose_down import compose_down

COMPOSE_FILE_PATH = "docker/docker-compose.test.yml"

def run_pytest():
    return subprocess.run(
        ["poetry", "run", "pytest"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def main():
    up_process = compose_up(COMPOSE_FILE_PATH)

    if up_process.returncode != 0:
        compose_down(COMPOSE_FILE_PATH)

        sys.exit(-1)

    run_pytest()

    compose_down(COMPOSE_FILE_PATH)

    

