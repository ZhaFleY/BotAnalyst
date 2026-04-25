from backend.celery_app import celery
import magic
from backend.utils.tgutils import send_message,send_document
import polars as pl
import pyreadstat
from backend.utils.data_processing import extract_useful_data,do_pdf_report,prepare_text
from backend.utils.logger import logger
import os
from backend.ai.agent import do_forecast
from backend.s3.core_db import client
import traceback
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
        return process_sav.delay(filepath, chat_id)

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
    pass





@celery.task
def process_xlsx_csv(df: pl.DataFrame):
    df = df.drop_nulls()
    df = df.fill_null(0)

    return df

@celery.task
def process_sav(objectname, chat_id):

    try:
        local_path = f"/tmp/{objectname}"
        print(f"LOCAL PATH: {local_path}")





        client.fget_object(
            "files",
            objectname,
            local_path
        )


        df, meta = pyreadstat.read_sav(local_path)


        labels = meta.variable_value_labels
        for col, mapping in labels.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)



        df = df.astype(str)
        print(111111)
        df = pl.DataFrame({
            "names":["Drake",'Kira','Anna'],
            "age": [33,20,18],
            "salary":[6000,1000,800]
        })
        agent_res = do_forecast(df.to_dicts(),chat_id)
        print(2222222)

        print("Бот дал ответ")
        print(agent_res)

        # pdf_path = do_pdf_report(agent_res)
        text = prepare_text(agent_res)
        send_message(chat_id,text)






        logger.info("Отчёт ушёл на сервер")

    except Exception as e:
        logger.error(f"Ошибка обработки SAV {traceback.format_exc()}")














