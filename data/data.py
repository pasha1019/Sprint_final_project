"""Тестовые данные и вспомогательные методы для API-тестов.

Модуль централизует валидные значения, сообщения об ошибках
и генерацию данных через Faker. Эндпоинты сервиса вынесены
в отдельный модуль data/endpoints.py.
"""

import random

import requests
from faker import Faker

from data.endpoints import LISTINGS_ENDPOINT, LOGIN_ENDPOINT

REQUEST_TIMEOUT = 15
MAX_RESPONSE_TIME = 5

VALID_CATEGORIES = ["Авто", "Книги", "Садоводство", "Хобби", "Технологии"]
VALID_CITIES = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Нижний Новгород",
    "Казань",
]
VALID_CONDITIONS = ["Новый", "Б/У"]

# Тексты сообщений сервиса, на которые опираются ассерты
ERROR_400_DUPLICATE_EMAIL = "Почта уже используется"
ERROR_401_EDIT_FORBIDDEN = "Оффер не найден или у вас нет прав на его редактирование"
ERROR_404_DELETE_FORBIDDEN = "Объявление не найдено или у вас нет прав для его удаления"
DELETE_SUCCESS_MESSAGE = "Объявление удалено успешно"

# Поля, которые можно отредактировать в объявлении
EDITABLE_FIELDS = ["name", "category", "condition", "city", "description", "price"]

DEFAULT_USER_PASSWORD = "TestPass123!"

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


def get_user_token(email, password):
    """Возвращает access_token пользователя по email и паролю.

    Авторизация через POST /api/signin: токен лежит в `token.access_token`.
    """
    try:
        resp = requests.post(
            LOGIN_ENDPOINT,
            json={"email": email, "password": password},
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 201:
            return resp.json().get("token", {}).get("access_token")
    except requests.exceptions.RequestException:
        pass
    return None


def get_listing_from_feed(listing_id, token):
    """Ищет объявление в ленте по id на первых двух страницах.

    Используется для проверки, что созданное/отредактированное
    объявление появилось в ленте с актуальными данными.
    """
    for page in (1, 2):
        resp = requests.get(
            f"{LISTINGS_ENDPOINT}/{page}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code != 200:
            continue
        offers = resp.json().get("offers", [])
        for offer in offers:
            if str(offer["id"]) == str(listing_id):
                return offer
        if not offers:
            break
    return None
