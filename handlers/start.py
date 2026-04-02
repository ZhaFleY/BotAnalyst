from aiogram import Router, Bot
from aiogram.filters.command import Command,CommandStart
from aiogram.types import Message
from keyboards.start_menu import build_start_menu
router = Router()

@router.message(CommandStart)
async def start(message:Message):

    title ,keyboard = build_start_menu()
    await message.answer(title,reply_markup=keyboard.as_markup())
