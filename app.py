import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os
from handlers import start,file_uploader,profile_settings
from dotenv import load_dotenv
from keyboards.start_menu import build_start_menu
load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
print(TOKEN)


"""
Запуск бота


"""
async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_routers(file_uploader.router,start.router,profile_settings.router)


    await dp.start_polling(bot)









if __name__ == '__main__':
     asyncio.run(main())









