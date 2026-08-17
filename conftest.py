"""Общие фикстуры pytest для всех тестов проекта.

Фикстуры инкапсулируют предусловия: регистрацию пользователя,
получение токена и создание объявления. Каждый тест получает
свежие данные, поэтому тесты не зависят друг от друга.
"""

import logging

import pytest

from helpers.listing_helper import ListingHelper
from helpers.user_helper import UserHelper

logger = logging.getLogger(__name__)


@pytest.fixture
def registered_user():
    """Создаёт нового пользователя и возвращает (email, password, token)."""
    logger.info("Регистрируем нового пользователя")
    creds = UserHelper.register_new_user_and_return_creds()
    if creds is None:
        pytest.fail("Пользователь не создался")
    yield creds


@pytest.fixture
def registered_user_token(registered_user):
    """Возвращает access_token авторизованного пользователя."""
    email, password, _ = registered_user
    logger.info("Получаем токен для пользователя %s", email)
    token = UserHelper.get_user_token(email, password)
    if token is None:
        pytest.fail("Не удалось получить токен пользователя")
    return token


@pytest.fixture
def foreign_user():
    """Создаёт «чужого» пользователя и возвращает (email, password, token)."""
    logger.info("Регистрируем «чужого» пользователя")
    creds = UserHelper.register_new_user_and_return_creds()
    if creds is None:
        pytest.fail("Пользователь не создался")
    email, password, _ = creds
    logger.info("Получаем токен для пользователя %s", email)
    token = UserHelper.get_user_token(email, password)
    if token is None:
        pytest.fail("Не удалось получить токен пользователя")
    yield email, password, token


@pytest.fixture
def created_listing(registered_user_token):
    """Создаёт объявление и гарантированно удаляет его после теста."""
    token = registered_user_token
    logger.info("Создаём объявление")
    response = ListingHelper.create_listing(token)
    if response.status_code != 201:
        pytest.fail(f"Объявление не создалось: {response.status_code}")
    listing = response.json()
    yield listing
    logger.info("Удаляем объявление с id %s", listing["id"])
    ListingHelper.delete_listing(token, listing["id"])
