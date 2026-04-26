from aiogram.fsm.state import State, StatesGroup


class UploadFileFSM(StatesGroup):
    upload = State()

