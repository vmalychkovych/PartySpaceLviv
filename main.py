import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

# Імпорт роутерів
from handlers import user, admin, moderation, broadcast

load_dotenv()


async def main():
    # Ініціалізація бота
    bot = Bot(
        token=os.getenv('BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Ініціалізація диспатчера
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Підключення роутерів
    dp.include_router(user.router)
    dp.include_router(admin.router)
    dp.include_router(moderation.router)
    dp.include_router(broadcast.router)

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())