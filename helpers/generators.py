"""Генерация тестовых данных через Faker и payload-билдеры.

Модуль изолирует динамические данные от статики (data/data.py)
и от API-методов (helpers/user_helper.py, helpers/listing_helper.py).
"""

import random

from faker import Faker

from data.data import VALID_CATEGORIES, VALID_CITIES, VALID_CONDITIONS

# Русская локаль Faker: генерирует реалистичные имена, слова и города
faker = Faker("ru_RU")


class Generators:
    """Генераторы тестовых данных и payload-билдеры."""

    @staticmethod
    def unique_email():
        """Возвращает уникальный email — гарантирует независимость тестов."""
        return faker.unique.email()

    @staticmethod
    def random_password():
        """Возвращает случайный пароль длиной 10 символов."""
        return faker.password(length=10)

    @staticmethod
    def random_listing_name():
        """Возвращает случайное название объявления из двух слов."""
        return f"{faker.word()} {faker.word()}"

    @staticmethod
    def random_listing_description():
        """Возвращает случайное описание объявления из шести слов."""
        return faker.sentence(nb_words=6)

    @staticmethod
    def random_price():
        """Возвращает случайную цену в диапазоне от 100 до 1 000 000."""
        return faker.random_int(min=100, max=1_000_000)

    @staticmethod
    def random_category():
        """Возвращает случайную категорию из валидного списка."""
        return random.choice(VALID_CATEGORIES)

    @staticmethod
    def random_city():
        """Возвращает случайный город из валидного списка."""
        return random.choice(VALID_CITIES)

    @staticmethod
    def random_condition():
        """Возвращает случайное состояние товара из валидного списка."""
        return random.choice(VALID_CONDITIONS)

    @staticmethod
    def default_listing_payload():
        """Возвращает payload для создания объявления со случайными данными."""
        return {
            "name": Generators.random_listing_name(),
            "category": Generators.random_category(),
            "condition": Generators.random_condition(),
            "city": Generators.random_city(),
            "description": Generators.random_listing_description(),
            "price": Generators.random_price(),
        }

    @staticmethod
    def edited_listing_payload(field):
        """Возвращает payload для редактирования объявления.

        Для поля price задаётся новая случайная цена, для остальных полей —
        значение с суффиксом `_edited`, чтобы гарантированно отличаться от исходного.
        """
        payload = Generators.default_listing_payload()
        if field == "price":
            payload[field] = Generators.random_price()
        else:
            payload[field] = f"{payload[field]}_edited"
        return payload