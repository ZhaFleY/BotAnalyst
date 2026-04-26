from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from bot.presentation.telegram.keyboards.start_menu import build_start_menu

router = Router()


@router.message(CommandStart)
async def start(message: Message):
    title, keyboard = build_start_menu()
    await message.answer(title, reply_markup=keyboard.as_markup())

