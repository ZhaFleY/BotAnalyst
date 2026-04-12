

import requests
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv("TOKEN")



def send_message(chat_id, text):
    if not isinstance(text, str):
        text = str(text)

    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text[:4096]
        }
    )

    print("TG RESPONSE:", r.status_code, r.text)