from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status,UploadFile, File, Form
from backend.workflows.file_flow import run_workflow

router = APIRouter(prefix="/api")


@router.post("/process_file")
async def process_file(file: UploadFile = File(...),
    chat_id: int = Form(...)):
    file_path = f"/tmp/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    run_workflow(file_path,chat_id)

    return {"status": "ok"}






