import subprocess
import sys
import argparse
from typing import Optional

from .utils.compose_up import compose_up
from .utils.compose_down import compose_down
from .utils.upgrade_database import upgrade_database

COMPOSE_FILE = "docker/docker-compose.dev.yml"

def create_migration(message: str):
    return subprocess.run(
        ["flask", "db", "migrate", "-m", message],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def init_parser():
    parser = argparse.ArgumentParser(description="Мой кастомный скрипт для Poetry")
    parser.add_argument("-m", "--message", type=str, required=True, help="Название миграции")

    return parser

def main(*args, **kwargs):
    parser = init_parser()

    args = parser.parse_args()

    # поднять контейнер
    result = compose_up(COMPOSE_FILE)

    if result.returncode != 0:
        raise BrokenPipeError("Docker контейнер не поднят.")
    # получить миграции
    upgrade_database()    

    try:
        result = create_migration(args.message)
        if result.returncode != 0:
            compose_down(COMPOSE_FILE)
            raise BrokenPipeError("Невозможно создать миграции.")

        print("Миграции созданы успешно.")

    finally:
        # остановить контейнер
        compose_down(COMPOSE_FILE)

    