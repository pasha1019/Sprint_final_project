"""Pydantic-модели ответов API для валидации в тестах.

Модели описывают структуру ответов сервиса и заменяют поштучные
ассерты по полям ответа в тестах.
"""

from pydantic import BaseModel


class ListingResponse(BaseModel):
    """Объявление в ответе сервиса (создание/редактирование, лента).

    Поля выверены по реальным ответам сервиса: id и price — целые числа,
    остальные поля — строки. Лишние поля ответа (owner, createdAt и т.п.)
    pydantic игнорирует по умолчанию.
    """

    id: int
    name: str
    category: str
    condition: str
    city: str
    description: str
    price: int
