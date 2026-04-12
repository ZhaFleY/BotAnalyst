from celery import Celery

celery = Celery(
    "bot",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=["backend.tasks.file_task"]
)

