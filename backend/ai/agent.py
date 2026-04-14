from langchain.agents import create_agent

from langchain.chat_models import init_chat_model
from backend.ai.tools import *
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json

from backend.ai.tools.agent_tool import built_chart,do_summary

load_dotenv()
model = ChatGoogleGenerativeAI(
    model = "gemini-3-flash-preview",
    google_api_key= os.getenv("API-KEY"),
    temperature=0.7
)
checkpointer = InMemorySaver()

PROMPT = """
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
"""


agent = create_agent(model,tools = [built_chart,do_summary],checkpointer= checkpointer,system_prompt=PROMPT)



def do_forecast(config:dict,chat_id:int):
    config = {
        "configurable": {
            "thread_id": str(chat_id)
        }
    }

    result = agent.invoke(input=json.dumps(config))



