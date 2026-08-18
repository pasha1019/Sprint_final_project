"""Статические данные и константы для API-тестов.

Модуль содержит только статику: валидные значения, сообщения об ошибках
и таймауты. Урлы вынесены в data/endpoints.py, генерация данных —
в helpers/generators.py, API-методы — в helpers/user_helper.py
и helpers/listing_helper.py.
"""

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
