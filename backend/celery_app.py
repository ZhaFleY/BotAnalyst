from celery import Celery

celery = Celery(
    "bot",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

celery.autodiscover_tasks(["backend.tasks"])