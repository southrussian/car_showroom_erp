from __future__ import annotations
from yandex_cloud_ml_sdk import YCloudML
from dotenv import load_dotenv
import os

load_dotenv()


def yandex(prompt: str) -> str:
    """Функция для взаимодействия с YandexGPT.

    Args:
        prompt: Текст запроса пользователя.

    Returns:
        Ответ от YandexGPT.
    """
    sdk = YCloudML(
        folder_id=os.getenv('FOLDER_ID'),
        auth=os.getenv('AUTH'),
    )

    messages = [
        {
            "role": "system",
            "text": "Ты - полезный ассистент автосалона. Отвечай вежливо и по делу, характеристики моделей "
                    "указывай максимально точно"
        },
        {
            "role": "user",
            "text": prompt
        }
    ]

    result = (
        sdk.models.completions("yandexgpt").configure(temperature=0.1).run(messages)
    )

    for alternative in result:
        return str(filter_text(alternative.text))

    return "Не удалось получить ответ от YandexGPT."


def filter_text(text):
    return text.replace('*', '').replace('#', '')
