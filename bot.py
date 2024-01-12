import logging
import asyncio
from aiogram import Bot, Dispatcher
from database.database import db_start
from config.bot_config import load_config
from handlers import user_handlers, create_profile, edit_profile, delete_profile, search
from keyboards.keyboards import set_commands


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    config = load_config()
    bot = Bot(token=config.token)
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(create_profile.router)
    dp.include_router(edit_profile.router)
    dp.include_router(delete_profile.router)
    dp.include_router(search.router)

    await db_start()
    await bot.set_my_commands(set_commands())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
