import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.presentation.telegram.routers.file_uploader import router as file_uploader_router
from bot.presentation.telegram.routers.profile_settings import router as profile_settings_router
from bot.presentation.telegram.routers.start import router as start_router

load_dotenv()
logging.basicConfig(level=logging.INFO)


async def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("TOKEN env var is not set")

    bot = Bot(token)
    dp = Dispatcher()
    dp.include_routers(file_uploader_router, start_router, profile_settings_router)
    await dp.start_polling(bot)


def run() -> None:
    asyncio.run(main())

