import subprocess
import sys
import signal

COMPOSE_FILE = "docker-compose.dev.yml"

def compose_up():
    return subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def compose_down(*args, **kwargs):
    return subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "down"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def flask_run():
    return subprocess.run(
        ["flask", "run", "-h", "0.0.0.0", "-p", "5000"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def main():
    signal.signal(signal.SIGTERM, compose_down)
    signal.signal(signal.SIGINT, compose_down)
    signal.signal(signal.SIGHUP, compose_down)

    up_process = compose_up()

    if up_process.returncode == 0:
        flask_run()

    compose_down()