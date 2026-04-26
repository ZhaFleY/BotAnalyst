from langchain.tools import tool


@tool
def do_summary(data: dict) -> str:
    """Generate a short analysis summary from provided dataset metadata."""
    return """
Анализ данных:
- выявлены тренды: ...
- аномалии: ...
- вывод: ...
"""
