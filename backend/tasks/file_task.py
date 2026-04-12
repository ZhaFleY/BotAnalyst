from backend.celery_app import celery
import magic
from backend.utils.tgutils import send_message
import polars as pl
import pyreadstat
import mimetypes
import os
from backend.s3.core_db import client
@celery.task
def detect_type(file_path, chat_id):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        file_type = "csv"
    elif ext in [".xls", ".xlsx"]:
        file_type = "excel"
    elif ext == ".sav":
        file_type = "spss"
    else:
        file_type = "unknown"

    return {
        "file_path": file_path,
        "chat_id": chat_id,
        "file_type": file_type
    }

@celery.task
def routers(payload):
    file_type = payload["file_type"]
    filepath = payload["file_path"]
    chat_id = payload["chat_id"]

    if file_type == "csv":
        return parse_csv.delay(filepath, chat_id)

    elif file_type == "excel":
        return parse_xlsx.delay(filepath, chat_id)

    elif file_type == "spss":
        return parse_sav.delay(filepath, chat_id)

    else:
        raise ValueError("Неподходящий формат файла")



@celery.task
def parse_csv(file_path,chat_id):
    df = pl.read_csv(file_path)
    df = df.drop_nulls()
    df = df.fill_null(0)
    df = df.unique()

    send_message(df.head(5),chat_id)


@celery.task
def parse_xlsx(object_name, chat_id):
    local_path = f"/tmp/{object_name}"



    client.fget_object(
        "files",
        object_name,
        local_path
    )

    df = pl.read_excel(local_path)
    preview = df.head(5).to_dicts()
    text = "\n".join(str(r) for r in preview)

    send_message(chat_id, text)


@celery.task
def parse_sav(file_path,chat_id):
    df,meta = pyreadstat.read_sav(file_path)
    df = df.drop_nulls()
    df = df.fill_null(0)
    send_message(df.head(5), chat_id)







