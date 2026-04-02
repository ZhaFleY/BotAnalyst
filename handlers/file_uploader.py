import aiogram
from aiogram import Router,F,types
import requests
router = Router()
@router.callback_query(F.text == "upload_cb")
def upload_cb(message: types.Message, data: types.CallbackQuery):
    pass