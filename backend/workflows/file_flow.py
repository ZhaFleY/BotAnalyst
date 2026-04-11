from celery import chain
from backend.tasks.file_task import detect_type, routers

def run_workflow(file_path, chat_id):


    print("FFF",chat_id)

    workflow = chain(
        detect_type.s(file_path, chat_id),
        routers.s()
    )

    workflow.apply_async()