import os
import traceback

import polars as pl
import pyreadstat

from backend.celery_app import celery
from backend.infrastructure.s3.core_db import client
from backend.modules.analysis.application.forecast import do_forecast
from backend.modules.analysis.application.report_text import prepare_text
from backend.shared.telegram.client import send_message
from backend.utils.logger import logger


@celery.task
def detect_type(file_path: str, chat_id: int):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        file_type = "csv"
    elif ext in [".xls", ".xlsx"]:
        file_type = "excel"
    elif ext == ".sav":
        file_type = "spss"
    else:
        file_type = "unknown"

    return {"file_path": file_path, "chat_id": chat_id, "file_type": file_type}


@celery.task
def routers(payload: dict):
    file_type = payload["file_type"]
    filepath = payload["file_path"]
    chat_id = payload["chat_id"]

    if file_type == "csv":
        return parse_csv.delay(filepath, chat_id)
    if file_type == "excel":
        return parse_xlsx.delay(filepath, chat_id)
    if file_type == "spss":
        return process_sav.delay(filepath, chat_id)

    raise ValueError("Неподходящий формат файла")


@celery.task
def parse_csv(file_path: str, chat_id: int):
    df = pl.read_csv(file_path).drop_nulls().fill_null(0).unique()
    send_message(chat_id, df.head(5))


@celery.task
def parse_xlsx(object_name: str, chat_id: int):
    pass


@celery.task
def process_sav(object_name: str, chat_id: int):
    try:
        local_path = f"/tmp/{object_name}"
        client.fget_object("files", object_name, local_path)

        df, meta = pyreadstat.read_sav(local_path)
        labels = meta.variable_value_labels
        for col, mapping in labels.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)

        sample_rows = int(os.getenv("ANALYSIS_SAMPLE_ROWS", "25"))
        max_cols = int(os.getenv("ANALYSIS_MAX_COLS", "60"))

        df = df.where(df.notna(), None)
        if df.shape[1] > max_cols:
            df = df.iloc[:, :max_cols]

        payload = {
            "shape": [int(df.shape[0]), int(df.shape[1])],
            "columns": list(df.columns),
            "dtypes": {k: str(v) for k, v in df.dtypes.to_dict().items()},
            "sample": df.head(sample_rows).to_dict(orient="records"),
        }

        agent_res = do_forecast(payload, chat_id)
        send_message(chat_id, prepare_text(agent_res))
    except Exception:
        logger.error(f"Ошибка обработки SAV {traceback.format_exc()}")


__all__ = ["detect_type", "routers", "parse_csv", "parse_xlsx", "process_sav"]
