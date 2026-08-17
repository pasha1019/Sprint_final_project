"""Тесты функциональности «Регистрация пользователя»."""

import logging

import requests

from data.data import ERROR_400_DUPLICATE_EMAIL, MAX_RESPONSE_TIME, REQUEST_TIMEOUT
from data.endpoints import SIGNUP_ENDPOINT
from helpers.generators import Generators

logger = logging.getLogger(__name__)


class TestRegistration:

    def test_register_user_success(self):
        """Регистрация нового пользователя с уникальным email.

        Given: данные нового пользователя
        When: выполняется POST /api/signup
        Then: сервис возвращает 201, email совпадает, в ответе есть access_token
        """
        logger.info("Генерируем данные нового пользователя")
        email = Generators.unique_email()
        password = Generators.random_password()
        payload = {"email": email, "password": password, "submitPassword": password}

        logger.info("Регистрируем пользователя с email %s", email)
        response = requests.post(SIGNUP_ENDPOINT, json=payload, timeout=REQUEST_TIMEOUT)

        assert response.status_code == 201
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        body = response.json()
        assert "user" in body
        assert "access_token" in body
        assert body["user"]["email"] == email
        assert "access_token" in body["access_token"]
        logger.info("Пользователь успешно зарегистрирован")

    def test_register_duplicate_email_fails(self, registered_user):
        """Повторная регистрация уже существующего email.

        Given: зарегистрированный пользователь
        When: отправляется повторный запрос на регистрацию с тем же email
        Then: сервис возвращает 400 и сообщение «Почта уже используется»
        """
        email, password, _ = registered_user
        payload = {"email": email, "password": password, "submitPassword": password}

        logger.info("Повторно регистрируем email %s", email)
        response = requests.post(SIGNUP_ENDPOINT, json=payload, timeout=REQUEST_TIMEOUT)

        assert response.status_code == 400
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        assert response.json()["message"] == ERROR_400_DUPLICATE_EMAIL
        logger.info("Сервис вернул ожидаемую ошибку дублирующего email")
