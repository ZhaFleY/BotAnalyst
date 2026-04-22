from langchain.agents import create_agent

from langchain.chat_models import init_chat_model
from backend.ai.tools import *
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv
import os
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from backend.ai.tools.agent_tool import built_chart,do_summary
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline



load_dotenv()




model = None
agent = None


def get_agent():
    global model, agent

    if agent is None:
        pipe = pipeline("text-generation",model="mistralai/Mistral-7B-Instruct-v0.3",
    device_map="auto")
        model = HuggingFacePipeline(pipeline=pipe)

        agent = create_agent(
            model,
            tools=[built_chart, do_summary],
            checkpointer=checkpointer,
            system_prompt=PROMPT
        )

    return agent


checkpointer = InMemorySaver()

PROMPT = """
<s>[INST]
Ты элитный аналитик тебе на вход падает фрагмент данных из 
опроса респондентов,сделай статистику их отетов.
1.Выяви аномалии или неточности
2.Построить анализ предоставленного фрагмента данных как профессиональный Data Scientist
3.Построй дашборд (круговой или столбчатый и т.д. на твоё усмотрение) верни данные для постройки как json

Верни строго JSON:

{
  "title: тема опроса
  "charts": [
    {
      "type": "...",
      "x": "...",
      "y": "..."
      "data": "..."
    }
  ],
  "summary": "...",
  "anomalies": [],
  "verdict": "..."
}
<s>[INST]
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



