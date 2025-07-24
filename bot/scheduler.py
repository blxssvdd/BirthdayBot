import sqlite3
from datetime import datetime, timedelta, time
import pytz
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)

async def send_birthday_countdown(bot: Bot):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT user_id, birthday, timezone FROM users WHERE birthday IS NOT NULL AND timezone IS NOT NULL')
    users = c.fetchall()
    conn.close()
    for user_id, birthday_str, tz_name in users:
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            next_birthday = birthday.replace(year=now.year)
            if next_birthday < now.date():
                next_birthday = next_birthday.replace(year=now.year + 1)
            days_left = (next_birthday - now.date()).days
            if now.time() >= time(0, 0) and now.time() < time(0, 5):  # отправлять только в первые 5 минут суток
                await bot.send_message(
                    user_id,
                    f'🎉 До вашего дня рождения осталось <b>{days_left}</b> дней!',
                    parse_mode='HTML'
                )
                logger.info(f'Уведомление отправлено user_id={user_id}, days_left={days_left}')
        except Exception as e:
            logger.error(f'Ошибка при отправке уведомления user_id={user_id}: {e}', exc_info=True)

def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    # Запускать задачу каждый час (чтобы не пропустить 00:00 в любом часовом поясе)
    scheduler.add_job(send_birthday_countdown, CronTrigger(minute='0,5', hour='*'), args=[bot])
    scheduler.start()
    logger.info('Планировщик ежедневных уведомлений запущен.') 