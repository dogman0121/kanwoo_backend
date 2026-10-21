import signal
import subprocess
import sys

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


def _shutdown_signals():
    """Сигналы, которые означают «останови dev‑стек» на данной ОС."""
    # SIGTERM и SIGINT есть и на Linux, и на Windows
    sigs = [signal.SIGTERM, signal.SIGINT]

    # SIGHUP — только POSIX (Linux/macOS)
    if hasattr(signal, "SIGHUP"):
        sigs.append(signal.SIGHUP)

    # SIGBREAK — только Windows (Ctrl+Break), полезен как аналог SIGHUP
    if hasattr(signal, "SIGBREAK"):
        sigs.append(signal.SIGBREAK)

    return sigs


def main():
    def handle_graceful_down(*_args, **_kwargs):
        # Не вызываем compose_down здесь — просто разворачиваем стек,
        # а cleanup сделает `finally` ниже (иначе compose_down вызовется дважды).
        sys.exit(0)

    for sig in _shutdown_signals():
        try:
            signal.signal(sig, handle_graceful_down)
        except (ValueError, OSError, RuntimeError):
            # Например, код выполняется не в главном потоке — такой сигнал
            # зарегистрировать нельзя, просто пропускаем.
            pass

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