from aiogram import Router

from .start import start_router
from .note import note_router


def get_main_router():
    main_router = Router()

    main_router.include_router(start_router)
    main_router.include_router(note_router)

    return main_router



