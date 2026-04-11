from backend.celery_app import celery
import magic
from backend.utils.tgutils import send_message
import polars as pl
import pyreadstat
@celery.task
def detect_type(path,chat_id):
    mime = magic.from_file(path,mime=True)
    return mime

@celery.task
def routers(filepath,chat_id):
    file_type = detect_type(filepath)

    if "csv" in file_type:
        return parse_csv.delay(filepath,chat_id)

    elif "excel" in file_type or "spreadsheet" in file_type:
        return parse_xlsx(filepath, chat_id)

    elif "spss" in file_type or filepath.endswith(".sav"):
        return parse_sav(filepath,chat_id)

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
def parse_xlsx(file_path,chat_id):
    df = pl.read_excel(file_path)
    df = df.drop_nulls()
    df = df.fill_null(0)
    send_message(df.head(5), chat_id)
    print(f"Готово на {chat_id}")

@celery.task
def parse_sav(file_path,chat_id):
    df,meta = pyreadstat.read_sav(file_path)
    df = df.drop_nulls()
    df = df.fill_null(0)
    send_message(df.head(5), chat_id)







