import loguru
import aiohttp
from dependency_injector.wiring import inject, Provide
from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from app.bot.keyboards.reply import reply_note_actions_keyboard
from app.core.config import settings
from app.schemas.user import CreateUserSchema
from app.utils.auth import generate_password

start_router = Router()


@start_router.message(CommandStart())
async def start_command_handler(
    message: types.Message,
):
    user_data = message.from_user.model_dump()
    user_data['telegram_id'] = user_data.pop('id')
    user_data['password'] = generate_password()
    create_user_schema = CreateUserSchema(**user_data)
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{settings.api_v1_url}/users/',
            json=create_user_schema.model_dump()
        ) as response:
            message_data = dict(
                reply_markup=reply_note_actions_keyboard
            )
            if response.status == 201:
                await message.answer(
                    'Вы успешно зарегестрированы, выберите действие',
                    **message_data
                )
            else:
                await message.answer(
                    'Вы уже зарегестрированы, выберите действие',
                    **message_data
                )
