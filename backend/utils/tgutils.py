

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


def send_document(chat_id: int, file_path: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"

    with open(file_path, "rb") as f:
        requests.post(
            url,
            data={"chat_id": chat_id},
            files={"document": f}
        )