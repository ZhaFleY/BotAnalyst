from celery import Celery
from backend.ai.agent import get_agent
celery = Celery(
    "bot",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=["backend.tasks.file_task"]
)

from celery.signals import worker_ready

@worker_ready.connect
def warmup_model(**kwargs):
    print("🔥 Warming up model...")
    get_agent()