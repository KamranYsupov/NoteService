import asyncio

from loguru import logger

from app.handlers.routing import get_all_routers

from app.middlewares.throttling import rate_limit_middleware



from loader import dp, bot


async def main():
    """Запуск бота."""
    try:
        dp.message.middleware(rate_limit_middleware)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logger.info("Bot is starting")
    asyncio.run(main())