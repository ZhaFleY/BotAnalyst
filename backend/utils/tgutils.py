

import requests
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv("TOKEN")


def send_message(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )