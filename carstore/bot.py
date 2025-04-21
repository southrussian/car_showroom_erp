import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio
from dotenv import load_dotenv
from yandexgpt import yandex
from logger import logger


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DATABASE = 'instance/autosalon.db'


def get_cars():
    """Функция для получения списка автомобилей из базы данных."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT make, model, status, price FROM cars")
    cars = cursor.fetchall()
    conn.close()
    return cars


@dp.message(Command('start'))
async def start_handler(message: types.Message):
    """Обработчик команды /start."""
    logger.info(f"User {message.from_user.id} ({message.from_user.username}) used /start")
    welcome_text = (
        "Добро пожаловать в автосалон!\n\n"
        "Доступные команды:\n"
        "/start - Начало работы\n"
        "/cars - Показать список автомобилей\n\n"
        "Также вы можете задать любой вопрос, и я постараюсь на него ответить!"
    )
    await message.reply(welcome_text)
    logger.info("Bot replied to /start")


@dp.message(Command('cars'))
async def cars_handler(message: types.Message):
    """Обработчик команды /cars для вывода списка автомобилей."""
    logger.info(f"User {message.from_user.id} ({message.from_user.username}) used /cars")
    cars = get_cars()
    if cars:
        response = "Список автомобилей:\n\n"
        for car in cars:
            response += f"{car[0]} {car[1]} | Статус: {car[2]} | Цена: {int(car[3])} руб.\n"
    else:
        response = "Автомобили не найдены."
    await message.reply(response)
    logger.info(f"Bot sent list of {len(cars)} cars")


@dp.message()
async def handle_message(message: types.Message):
    """Обработчик всех текстовых сообщений, не являющихся командами."""
    try:
        user_info = f"{message.from_user.id} ({message.from_user.username})"
        logger.info(f"Message from {user_info}: {message.text}")

        response = yandex(message.text)

        await message.reply(response)
        logger.info(f"Bot replied to {user_info}: {response[:50]}...")
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        logger.error(error_msg)
        await message.reply("Произошла ошибка при обработке запроса.")


async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)
    logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
