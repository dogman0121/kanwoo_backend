import subprocess
import sys

def compose_down(path: str):
    return subprocess.run(
        ["docker", "compose", "-f", path, "down"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )