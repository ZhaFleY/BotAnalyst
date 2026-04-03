import aiogram
from aiogram import Router,F,types
import requests
from aiogram.fsm.context import FSMContext
from webhooks.file_manager import send_to_agent
from utils.logger import logger

from FSM.ulpload_file_fsm import UploadFileFSM
router = Router()
@router.callback_query(F.data == "upload_cb")
async def upload_cb( data: types.CallbackQuery,state: FSMContext):
    logger.info("button is clicked")


    await state.set_state(UploadFileFSM.upload)
    await data.message.answer("Скиньте файл формата .sav, .csv , .xlsx")

@router.message(UploadFileFSM.upload, F.document)
async def file_cb(message: types.Message, state: FSMContext):
    doc = message.document
    file_name = doc.file_name or "file.dat"
    path = f"uploads/{file_name}"

    msg = await message.answer("⏳ Загружаю файл...")

    try:

        await message.bot.download(doc, destination=path)

        await msg.edit_text("Обработка...")

        res = send_to_agent(path)

        await msg.edit_text("Готово")

    except Exception as e:
        await msg.edit_text(f"ошибка - {e}")

    await state.clear()
