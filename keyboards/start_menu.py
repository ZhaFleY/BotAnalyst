from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardButton
from configs.config import cfg

def build_start_menu():
    start_menu = cfg["start_menu"]
    title = start_menu["title"]

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text=start_menu["upload_data"]["name"], callback_data=start_menu["upload_data"]["callback"]),
        InlineKeyboardButton(text=start_menu["settings"]["name"], callback_data=start_menu["settings"]["callback"]),
    )

    return title,builder



