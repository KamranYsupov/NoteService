from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)


reply_note_actions_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Создать запись 📝'
            ),
        ],
        [
            KeyboardButton(
                text='Мои записи 📃'
            ),
        ],
        [
            KeyboardButton(
                text='Поиск по тегам 🔍'
            ),
        ],
    ],
    resize_keyboard=True
)

reply_cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Отмена ❌'
            ),
        ],
    ],
    resize_keyboard=True
)

reply_keyboard_remove = ReplyKeyboardRemove()