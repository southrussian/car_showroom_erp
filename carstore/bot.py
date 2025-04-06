import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio

BOT_TOKEN = '7967426961:AAGsutHhzaYjA29UX2PSwt2qVLGbvMcvuZg'

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
    welcome_text = (
        "Добро пожаловать в автосалон!\n\n"
        "Доступные команды:\n"
        "/start - Начало работы\n"
        "/cars - Показать список автомобилей"
    )
    await message.reply(welcome_text)


@dp.message(Command('cars'))
async def cars_handler(message: types.Message):
    """Обработчик команды /cars для вывода списка автомобилей."""
    cars = get_cars()
    if cars:
        response = "Список автомобилей:\n\n"
        for car in cars:
            # Форматирование строки для каждого автомобиля
            response += f"ID: {car[0]} | Модель: {car[1]} | Цена: {car[2]}\n"
    else:
        response = "Автомобили не найдены."
    await message.reply(response)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
