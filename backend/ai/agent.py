from langchain.agents import create_agent

from langchain.chat_models import init_chat_model
from backend.ai.tools import *
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv
import os
import json

from backend.ai.tools.agent_tool import do_summary

from langchain_gigachat.chat_models import GigaChat



load_dotenv()

GIGA_KEY = os.getenv("GIGA-KEY")


model = None
agent = None


def get_agent():
    global model, agent

    if agent is None:
        giga = GigaChat(

            credentials=GIGA_KEY,
            verify_ssl_certs=False,
        )


        agent = create_agent(
            giga,
            tools=[do_summary],
            checkpointer=checkpointer,
            system_prompt=PROMPT
        )

    return agent


checkpointer = InMemorySaver()

PROMPT = """
<s>
Ты элитный аналитик тебе на вход падает фрагмент данных из 
опроса респондентов,сделай статистику их отетов.
1.Выяви аномалии или неточности

Верни сторого json с параметрами title, summary  

"""






def do_forecast(config,chat_id:int):
    agent = get_agent()


    configs = {
        "configurable": {
            "thread_id": str(chat_id)
        }
    }
    print(f"конфиг собран")

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(config, ensure_ascii=False)
                }
            ]
        },
        config=configs
    )


    print("Готово")
    return result



