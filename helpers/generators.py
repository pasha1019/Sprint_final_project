"""Генерация тестовых данных через Faker и payload-билдеры.

Модуль изолирует динамические данные от статики (data/data.py)
и от API-методов (helpers/user_helper.py, helpers/listing_helper.py).
"""

import random

from faker import Faker

from data.data import VALID_CATEGORIES, VALID_CITIES, VALID_CONDITIONS

# Русская локаль Faker: генерирует реалистичные имена, слова и города
faker = Faker("ru_RU")


def unique_email():
    """Возвращает уникальный email — гарантирует независимость тестов."""
    return faker.unique.email()


def random_password():
    """Возвращает случайный пароль длиной 10 символов."""
    return faker.password(length=10)


def random_listing_name():
    """Возвращает случайное название объявления из двух слов."""
    return f"{faker.word()} {faker.word()}"


def random_listing_description():
    """Возвращает случайное описание объявления из шести слов."""
    return faker.sentence(nb_words=6)


def random_price():
    """Возвращает случайную цену в диапазоне от 100 до 1 000 000."""
    return faker.random_int(min=100, max=1_000_000)


def random_category():
    """Возвращает случайную категорию из валидного списка."""
    return random.choice(VALID_CATEGORIES)


def random_city():
    """Возвращает случайный город из валидного списка."""
    return random.choice(VALID_CITIES)


def random_condition():
    """Возвращает случайное состояние товара из валидного списка."""
    return random.choice(VALID_CONDITIONS)


def default_listing_payload():
    """Возвращает payload для создания объявления со случайными данными."""
    return {
        "name": random_listing_name(),
        "category": random_category(),
        "condition": random_condition(),
        "city": random_city(),
        "description": random_listing_description(),
        "price": random_price(),
    }


def edited_listing_payload(field):
    """Возвращает payload для редактирования объявления.

    Для поля price задаётся новая случайная цена, для остальных полей —
    значение с суффиксом `_edited`, чтобы гарантированно отличаться от исходного.
    """
    payload = default_listing_payload()
    if field == "price":
        payload[field] = random_price()
    else:
        payload[field] = f"{payload[field]}_edited"
    return payload
