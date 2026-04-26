import os

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")


def send_message(chat_id: int, text) -> None:
    if not isinstance(text, str):
        text = str(text)

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text[:4096]},
        timeout=30,
    )


def send_document(chat_id: int, file_path: str) -> None:
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        requests.post(url, data={"chat_id": chat_id}, files={"document": f}, timeout=60)

