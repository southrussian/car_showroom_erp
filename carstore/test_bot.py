import pytest
from aiogram import Dispatcher, Bot
from aiogram.types import Message, User, Chat
from unittest.mock import AsyncMock, MagicMock
from bot import (
    get_cars,
    get_orders,
    start_handler,
    cars_handler,
    orders_handler,
    handle_message,
    DATABASE
)
import sqlite3
import os


# Фикстуры для тестов
@pytest.fixture
def bot():
    return Bot(token="test_token")


@pytest.fixture
def dispatcher():
    return Dispatcher()


@pytest.fixture
def message():
    user = User(id=123, first_name="Test", is_bot=False, username="test_user")
    chat = Chat(id=123, type="private")
    return Message(message_id=1, from_user=user, chat=chat, date=None, text="")


# Тестовые данные
TEST_CARS = [
    ("Toyota", "Camry", "В наличии", 2000000),
    ("Honda", "Accord", "В наличии", 1800000)
]

TEST_ORDERS = [
    ("Toyota", "Camry", "В обработке", "Иван", "Иванов", "2023-12-31")
]


# Моки для базы данных
@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    # Создаем временную базу данных для тестов
    test_db = "test_autosalon.db"
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Создаем тестовые таблицы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id INTEGER PRIMARY KEY,
            make TEXT,
            model TEXT,
            status TEXT,
            price INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            car_id INTEGER,
            client_id INTEGER,
            status TEXT,
            expected_delivery_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT
        )
    """)

    # Заполняем тестовыми данными
    cursor.executemany("INSERT INTO cars (make, model, status, price) VALUES (?, ?, ?, ?)", TEST_CARS)
    cursor.executemany("""
        INSERT INTO orders (car_id, client_id, status, expected_delivery_date)
        VALUES (
            (SELECT car_id FROM cars WHERE make=? AND model=?),
            (SELECT client_id FROM clients WHERE first_name=? AND last_name=?),
            ?, ?
        )
    """, [(*order[:2], order[3], order[4], order[2], order[5]) for order in TEST_ORDERS])

    cursor.executemany("INSERT INTO clients (first_name, last_name) VALUES (?, ?)",
                       [(order[3], order[4]) for order in TEST_ORDERS])

    conn.commit()
    conn.close()

    # Монкипатчим путь к базе данных
    monkeypatch.setattr("bot.DATABASE", test_db)

    yield

    # Удаляем временную базу после тестов
    if os.path.exists(test_db):
        os.remove(test_db)


# Тесты для функций работы с базой данных
def test_get_cars():
    cars = get_cars()
    assert len(cars) == 2
    assert cars[0][0] == "Toyota"
    assert cars[1][1] == "Accord"


def test_get_orders():
    orders = get_orders()
    assert len(orders) == 1
    assert orders[0][0] == "Toyota"
    assert orders[0][2] == "В обработке"


# Тесты для обработчиков команд
@pytest.mark.asyncio
async def test_start_handler(message: Message):
    await start_handler(message)
    assert "Добро пожаловать в автосалон" in message.reply.call_args[0][0]


@pytest.mark.asyncio
async def test_cars_handler(message: Message):
    await cars_handler(message)
    response = message.reply.call_args[0][0]
    assert "Список автомобилей" in response
    assert "Toyota Camry" in response
    assert "Honda Accord" in response


@pytest.mark.asyncio
async def test_orders_handler(message: Message):
    await orders_handler(message)
    response = message.reply.call_args[0][0]
    assert "Список заказов" in response
    assert "Toyota Camry" in response
    assert "Иван Иванов" in response


@pytest.mark.asyncio
async def test_handle_message(message: Message, monkeypatch):
    # Мокаем функцию yandex
    monkeypatch.setattr("bot.yandex", lambda x: "Тестовый ответ")

    message.text = "Привет"
    await handle_message(message)
    assert "Тестовый ответ" in message.reply.call_args[0][0]


@pytest.mark.asyncio
async def test_handle_message_error(message: Message, monkeypatch):
    # Мокаем функцию yandex чтобы вызвать ошибку
    def mock_yandex(x):
        raise Exception("Test error")

    monkeypatch.setattr("bot.yandex", mock_yandex)

    message.text = "Привет"
    await handle_message(message)
    assert "Произошла ошибка" in message.reply.call_args[0][0]
