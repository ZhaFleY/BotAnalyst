from fastapi import APIRouter, UploadFile, File, Form
from backend.workflows.file_flow import run_workflow
from backend.s3.core_db import client
import uuid
import os
from backend.utils.data_processing import extract_zip

router = APIRouter(prefix="/api")


@router.post("/process_file")
async def process_file(
    file: UploadFile = File(...),
    chat_id: int = Form(...)
):
    import uuid

    tmp_zip = f"/tmp/{uuid.uuid4()}_{file.filename}"

    with open(tmp_zip, "wb") as f:
        f.write(await file.read())


    extracted_file = extract_zip(tmp_zip)


    object_name = f"{uuid.uuid4()}_{os.path.basename(extracted_file)}"

    client.fput_object(
        "files",
        object_name,
        extracted_file
    )


    run_workflow(object_name, chat_id)

    return {"status": "ok"}