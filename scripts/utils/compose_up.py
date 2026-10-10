import subprocess
import sys

def compose_up(path: str):
    return subprocess.run(
        ["docker", "compose", "-f", path, "up", "-d"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )