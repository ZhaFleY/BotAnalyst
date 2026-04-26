from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "settings_cb")
async def settings_cb(query: CallbackQuery):
    await query.message.answer("Clicked")

