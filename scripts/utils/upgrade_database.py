import subprocess

def upgrade_database():
    return subprocess.run(
        ["flask", "db", "upgrade"]
    )