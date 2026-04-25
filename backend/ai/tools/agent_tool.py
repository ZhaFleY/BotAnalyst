from langchain.tools import tool, ToolRuntime
import matplotlib.pyplot as plt




@tool
def do_summary(data: dict) -> str:
    """
    Генерация текста анализа (или подготовка)
    """

    return f"""
    Анализ данных:
    - выявлены тренды: ...
    - аномалии: ...
    - вывод: ...
    """