from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.presentation.telegram.fsm.upload_file_fsm import UploadFileFSM
from bot.shared.logger import logger

import requests

router = Router()


@router.callback_query(F.data == "upload_cb")
async def upload_cb(data: types.CallbackQuery, state: FSMContext):
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
        with open(path, "rb") as f:
            response = requests.post(
                "http://api:8000/api/process_file",
                data={"chat_id": message.chat.id},
                files={"file": f},
            )
        await msg.edit_text("Обработка...")
        if response.status_code == 200:
            await msg.edit_text("Готово")
        else:
            await msg.edit_text(f"ОШИБКА {response.status_code}, {response.text}")

    except Exception as e:
        await msg.edit_text(f"ошибка - {e}")

    await state.clear()

