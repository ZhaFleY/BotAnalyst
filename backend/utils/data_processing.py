from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from matplotlib import pyplot as plt
import uuid
import zipfile
from io import BytesIO
import os
def extract_useful_data(df):
    """
    Подготавливает данные для агента

    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "sample": df.head(10).to_dicts(),
        "describe": df.describe().to_dicts()
    }



def do_pdf_report(report:dict):
    """
       Собирает PDF отчет из JSON
       """

    file_id = str(uuid.uuid4())
    path = f"/tmp/{file_id}.pdf"

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    content = []

    # TITLE
    content.append(Paragraph(report["title"], styles["Title"]))
    content.append(Spacer(1, 12))

    # SUMMARY
    content.append(Paragraph(report["summary"], styles["Normal"]))
    content.append(Spacer(1, 12))

    # CHARTS
    for chart in report.get("charts", []):
        img_path = f"/tmp/{uuid.uuid4()}.png"


        plt.figure()
        plt.title(f'{chart["type"]}: {chart["x"]} vs {chart["y"]}')
        plt.plot(chart["data"])
        plt.savefig(img_path)
        plt.close()

        content.append(Image(img_path, width=400, height=200))
        content.append(Spacer(1, 12))

    doc.build(content)

    return path
def extract_zip(tmp_zip_path: str) -> str:
    extract_dir = f"/tmp/{uuid.uuid4()}"
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(tmp_zip_path, "r") as z:
        z.extractall(extract_dir)

    # берем первый файл внутри
    files = os.listdir(extract_dir)
    if not files:
        raise ValueError("Zip пустой")

    return os.path.join(extract_dir, files[0])