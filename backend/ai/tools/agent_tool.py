from langchain.tools import tool, ToolRuntime
import matplotlib.pyplot as plt


@tool
def built_chart(spec: dict) -> dict:
    """
    Проверяет и нормализует структуру графика
    """
    return {
        "type": spec["type"],
        "x": spec["x"],
        "y": spec["y"]
    }


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