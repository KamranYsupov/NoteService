from aiogram import Bot, Dispatcher

from app.core.config import settings

bot = Bot(settings.bot_token)
dp = Dispatcher()