import httpx
from loguru import logger
from fastapi import HTTPException
from starlette import status


class TelegramBotService:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        
    def get_user(self, telegram_id: int) -> dict:
        url = f'https://api.telegram.org/bot{self.bot_token}/getChat'
        
        exc = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        
        params = {
            'chat_id': str(telegram_id),
        }
    
        with httpx.Client() as client:
            response = client.get(url, params=params)
                
            if response.status_code != 200:
                exc.detail=f'Пользователь с telegram_id равным {telegram_id} не найден'
                raise exc
                       
        return response.json()
