import subprocess
import sys

COMPOSE_FILE_PATH = "docker/docker-compose.test.yml"

def compose_up():
    return subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE_PATH, "up", "-d"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def compose_down():
    return subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE_PATH, "down"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def run_pytest():
    return subprocess.run(
        ["poetry", "run", "pytest"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def main():
    up_process = compose_up()

    if up_process.returncode != 0:
        compose_down()

        sys.exit(-1)

    run_pytest()

    compose_down()

    

