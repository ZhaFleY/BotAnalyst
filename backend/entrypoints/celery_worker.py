from celery import Celery
from celery.signals import worker_ready

from backend.modules.analysis.application.forecast import get_agent


def create_celery() -> Celery:
    return Celery(
        "bot",
        broker="redis://redis:6379/0",
        backend="redis://redis:6379/1",
        include=["backend.application.tasks.file_task"],
    )


celery = create_celery()


@worker_ready.connect
def warmup_model(**kwargs):
    print("🔥 Warming up model...")
    get_agent()

