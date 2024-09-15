import aiohttp
import json
from dependency_injector.wiring import inject, Provide
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from fastapi import HTTPException

from app.bot.keyboards.reply import reply_note_actions_keyboard
from app.core.config import settings
from app.core.container import Container
from app.services import UserService
from app.schemas.user import CreateUserSchema
from app.schemas.note import CreateNoteSchema
from app.schemas.auth import AuthUserSchema
from app.utils.auth import generate_password
from app.utils.http import authenticate

note_router = Router()


class NoteState(StatesGroup):
    title = State()
    content = State()
    tags_names = State()
    
    
class TagSearchState(StatesGroup):
    tag = State()
    
    
@note_router.message(F.text.casefold() == 'создать запись 📝')
async def start_create_note_handler(
    message: types.Message,
    state: FSMContext,
):
    await message.answer('Напиши и отправь заголовок записи')
    await state.set_state(NoteState.title)
    

    

@note_router.message(NoteState.title)
async def title_create_note_handler(
    message: types.Message,
    state: FSMContext,
):
    await state.update_data(title=message.text)
    await message.answer('Теперь напиши содержание для твоей записи')
    await state.set_state(NoteState.content)
    

@note_router.message(NoteState.content)
async def content_create_note_handler(
    message: types.Message,
    state: FSMContext,
):
    await state.update_data(content=message.text)
    await message.answer(
        'На последок можешь отправить '
        'теги в формате "#тег1 #тег2",'
        'они нужны для поиска записей')
    await state.set_state(NoteState.tags_names)
    

@note_router.message(NoteState.tags_names)
@inject
async def tags_names_create_note_handler(
    message: types.Message,
    state: FSMContext,
    user_service: UserService = Provide[
        Container.user_service
    ],
):
    current_user = await user_service.get(telegram_id=message.from_user.id)
   
    tags_names = message.text.split()
    while '#' in tags_names:
        tags_names.remove('#') 

    await state.update_data(tags_names=tags_names)
    data = await state.get_data()
    data['owner_id'] = current_user.id
    create_note_schema = CreateNoteSchema(**data)
    create_note_schema.owner_id = str(current_user.id)
    
    auth_schema = AuthUserSchema(
        username=message.from_user.username,
        password=settings.telegram_client_password,
    )
    try:
        token_data = await authenticate(auth_schema)
        access_token = token_data['access_token']
    except HTTPException as e:
        await message.answer(е)
        await state.clear()
        return
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{settings.api_v1_url}/notes',
            json=create_note_schema.model_dump(),
            headers={'Authorization': f'Bearer {access_token}'}
        ) as response:
            if response.status != 201:
                await message.answer(
                    'Ошибка сервера. Попробуйте позже.',
                )
                await state.clear()
                return 
            response_data = await response.json()
            
            tags_str = ' '.join([f'{tag} 'for tag in response_data['tags']])
            await message.answer(
                response_data['title'] + '\n\n' +
                response_data['content'] + '\n\n' +
                'Теги:' + tags_str
            )
            await state.clear()
            
            
@note_router.message(F.text.casefold() == 'поиск по тегам 🔍')
async def start_tag_search_handler(
    message: types.Message,
    state: FSMContext,
):
    await message.answer('Отправь тег, записи с которым хочешь найти')
    await state.set_state(TagSearchState.tag)
    
@note_router.message(TagSearchState.tag)
@inject
async def notes_tag_search_handler(
    message: types.Message,
    state: FSMContext,
    user_service: UserService = Provide[
        Container.user_service
    ],
):
    current_user = await user_service.get(telegram_id=message.from_user.id)
    auth_schema = AuthUserSchema(
        username=message.from_user.username,
        password=settings.telegram_client_password,
    )
    try:
        token_data = await authenticate(auth_schema)
        access_token = token_data['access_token']
    except HTTPException as e:
        await message.answer(е)
        await state.clear()
        return
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{settings.api_v1_url}/notes/by_tag_name',
            params={'tag_name': message.text},
            headers={'Authorization': f'Bearer {access_token}'}
        ) as response:
            if response.status != 200:
                await message.answer(
                    'Ошибка сервера. Попробуйте позже.',
                )
                await state.clear()
                return 
            response_data = await response.json()
            message_text = ''
            
            for data in response_data:
                tags_str = ' '.join([f'{tag} 'for tag in data['tags']])
                message_text += (
                data['title'] + '\n\n' +
                data['content'] + '\n\n' +
                'Теги:' + tags_str + '\n\n'
            )
            
            await message.answer(message_text) 
            await state.clear()
            
    
@note_router.message(F.text.casefold() == 'мои записи 📃')
@inject
async def notes_handler(
    message: types.Message,
    state: FSMContext,
    user_service: UserService = Provide[
        Container.user_service
    ],
):
    current_user = await user_service.get(telegram_id=message.from_user.id)
    auth_schema = AuthUserSchema(
        username=message.from_user.username,
        password=settings.telegram_client_password,
    )
    try:
        token_data = await authenticate(auth_schema)
        access_token = token_data['access_token']
    except HTTPException as e:
        await message.answer(е)
        await state.clear()
        return
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{settings.api_v1_url}/notes/',
            headers={'Authorization': f'Bearer {access_token}'}
        ) as response:
            if response.status != 200:
                await message.answer(
                    'Ошибка сервера. Попробуйте позже.',
                )
                await state.clear()
                return 
            response_data = await response.json()
            
            message_text = ''
            
            for data in response_data:
                tags_str = ' '.join([f'{tag} 'for tag in data['tags']])
                message_text += (
                data['title'] + '\n\n' +
                data['content'] + '\n\n' +
                'Теги:' + tags_str + '\n\n'
            )
            
            await message.answer(message_text) 
            await state.clear()
        