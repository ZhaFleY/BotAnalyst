from celery import chain

from backend.application.tasks.file_task import detect_type, routers


def run_workflow(object_name: str, chat_id: int):
    workflow = chain(detect_type.s(object_name, chat_id), routers.s())
    workflow.apply_async()

