from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet

import uuid
import zipfile
import json
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





try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
except Exception as e:
    print(f"Шрифт не найден, будет ошибка с кириллицей: {e}")


def do_pdf_report(report_data: dict):
    # 1. Извлекаем данные
    final_message = report_data['messages'][-1].content
    # Очищаем от возможных ```json ... ``` если агент их добавил
    clean_json = final_message.strip().replace('```json', '').replace('```', '')
    report = json.loads(clean_json)

    file_id = str(uuid.uuid4())
    path = f"/tmp/{file_id}.pdf"

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    # 2. Настраиваем шрифты для всех используемых стилей
    for style_name in styles.byName:
        styles[style_name].fontName = 'DejaVu'

    content = []

    # TITLE
    title_text = report.get("title", "Отчет по анализу данных")
    content.append(Paragraph(title_text, styles["Title"]))
    content.append(Spacer(1, 12))

    # SUMMARY
    summary = report.get("summary", {})
    # Делаем JSON красивым для PDF:
    # indent=4, заменяем переводы строк на <br/>, а пробелы на &nbsp;
    summary_raw = json.dumps(summary, ensure_ascii=False, indent=4)
    summary_formatted = summary_raw.replace('\n', '<br/>').replace('  ', '&nbsp;&nbsp;')

    # Оборачиваем в тег <font>, если нужно явно указать размер или еще раз шрифт
    content.append(Paragraph(summary_formatted, styles["Normal"]))
    content.append(Spacer(1, 12))

    # BUILD
    doc.build(content)
    return path


def prepare_text(report_data: dict):
    try:
        # 1. Извлекаем контент
        final_message = report_data['messages'][-1].content

        # 2. Очищаем от Markdown и пытаемся распарсить JSON
        clean_json = final_message.strip().replace('```json', '').replace('```', '')
        report = json.loads(clean_json)

        # 3. Красиво форматируем summary
        summary = report.get('summary', {})

        # Если summary — это словарь или список, превращаем его в читаемый текст
        if isinstance(summary, (dict, list)):
            # indent=4 сделает "лесенку", ensure_ascii=False сохранит русские буквы
            summary_text = json.dumps(summary, ensure_ascii=False, indent=4)
        else:
            summary_text = str(summary)

        # 4. Собираем финальный текст
        title = report.get('title', 'Отчет по анализу данных').upper()

        txt = f"""
{title}
{'-' * len(title)}

АНАЛИЗ ДАННЫХ:
{summary_text}

Дата генерации: 2026-04-25
"""
        return txt

    except Exception as e:
        # Если JSON всё-таки сломался, возвращаем сырой текст, чтобы не падать
        raw_text = report_data['messages'][-1].content
        return f"ОШИБКА ФОРМАТИРОВАНИЯ (Сырые данные):\n\n{raw_text}"




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