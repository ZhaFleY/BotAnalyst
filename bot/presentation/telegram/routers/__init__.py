from bot.presentation.telegram.routers.file_uploader import router as file_uploader_router
from bot.presentation.telegram.routers.profile_settings import router as profile_settings_router
from bot.presentation.telegram.routers.start import router as start_router

__all__ = [
    "file_uploader_router",
    "profile_settings_router",
    "start_router",
]

