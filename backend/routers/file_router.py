from fastapi import APIRouter, UploadFile, File, Form
from backend.workflows.file_flow import run_workflow
from backend.s3.core_db import client
import uuid
import os

router = APIRouter(prefix="/api")


@router.post("/process_file")
async def process_file(
    file: UploadFile = File(...),
    chat_id: int = Form(...)
):
    # 1. временный файл
    tmp_path = f"/tmp/{file.filename}"

    with open(tmp_path, "wb") as f:
        f.write(await file.read())

    # 2. уникальное имя в S3 (ВАЖНО)
    object_name = f"{uuid.uuid4()}_{file.filename}"

    # 3. загрузка в MinIO
    client.fput_object(
        "files",
        object_name,
        tmp_path
    )


    run_workflow(object_name, chat_id)

    return {"status": "ok"}