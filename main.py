import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import logging
from bot.routes import router
from db import init_db
from bot.scheduler import setup_scheduler
from aiogram.types import BotCommand

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    logger.info('Запуск BirthdayBot...')
    logger.info(f'Токен: {API_TOKEN[:6]}***... (скрыт)')
    init_db()
    setup_scheduler(bot)
    await bot.set_my_commands([
        BotCommand(command='menu', description='Главное меню'),
        BotCommand(command='start', description='Начать регистрацию'),
        BotCommand(command='timezone', description='Изменить часовой пояс'),
    ])
    logger.info('Бот успешно запущен. Ожидание событий...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
