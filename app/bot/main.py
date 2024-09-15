import asyncio

from loguru import logger
from app.bot.handlers.routing import get_main_router
from app.bot.middlewares.throttling import rate_limit_middleware
from app.core.container import Container
from app.bot import handlers
from loader import dp, bot


async def main():
    """Запуск бота."""
    try:
        dp.message.middleware(rate_limit_middleware)
        dp.include_router(get_main_router())
        dp.message.middleware(rate_limit_middleware)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[
        handlers.note,
    ])
    logger.info("Bot is starting")
    asyncio.run(main())