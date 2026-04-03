from aiogram import Router,F
from aiogram.types import CallbackQuery
from aiogram.filters.command import Command


router = Router()
@router.callback_query(F.data == "settings_cb")
async def settings_cb(query: CallbackQuery):
    await query.message.answer("Clicked")