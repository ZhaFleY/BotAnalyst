import json
import os
from datetime import date, datetime
from decimal import Decimal

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_gigachat.chat_models import GigaChat
from langgraph.checkpoint.memory import InMemorySaver

from backend.modules.analysis.infrastructure.llm.tools.summary_tool import do_summary

load_dotenv()

GIGA_KEY = os.getenv("GIGA-KEY")

_checkpointer = InMemorySaver()
_agent = None

PROMPT = """
<s>
Ты элитный аналитик. Тебе на вход приходит JSON с данными датасета:
- shape: [rows, cols]
- columns: список колонок
- dtypes: типы колонок
- sample: несколько строк (records)
Сделай статистику и выводы по данным.
1. Выяви аномалии или неточности

Верни СТРОГО валидный JSON (без markdown/комментариев) вида:
{
  "title": "строка",
  "summary": {
    "объем выборки": "строка",
    "признаки": "строка",
    "проблемы и замечания": ["строка1", "строка2"]
  }
}
"""


def get_agent():
    global _agent
    if _agent is None:
        giga = GigaChat(credentials=GIGA_KEY, verify_ssl_certs=False)
        _agent = create_agent(
            giga,
            tools=[do_summary],
            checkpointer=_checkpointer,
            system_prompt=PROMPT,
        )
    return _agent


def do_forecast(config, chat_id: int):
    agent = get_agent()
    configs = {"configurable": {"thread_id": str(chat_id)}}

    def _json_default(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        try:
            import numpy as np

            if isinstance(obj, (np.integer, np.floating, np.bool_)):
                return obj.item()
        except Exception:
            pass
        try:
            import pandas as pd

            if isinstance(obj, pd.Timestamp):
                return obj.isoformat()
        except Exception:
            pass
        if hasattr(obj, "isoformat"):
            try:
                return obj.isoformat()
            except Exception:
                pass
        return str(obj)

    try:
        return agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": json.dumps(config, ensure_ascii=False, default=_json_default),
                    }
                ]
            },
            config=configs,
        )
    except Exception as e:
        return {"error": str(e), "error_type": e.__class__.__name__}
