from aiogram import Router, Bot
from aiogram.filters.command import Command,CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart)
async def start(message:Message):
    await message.answer("hitler")
