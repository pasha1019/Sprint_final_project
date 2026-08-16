"""Тесты функциональности «Авторизация пользователя»."""

import logging

import requests

from data.data import LOGIN_ENDPOINT, MAX_RESPONSE_TIME, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class TestAuthorization:

    def test_login_user_success(self, registered_user):
        """Авторизация ранее зарегистрированного пользователя.

        Given: зарегистрированный пользователь
        When: выполняется POST /api/signin
        Then: сервис возвращает 201, email совпадает, в ответе есть access_token
        """
        email, password, _ = registered_user

        logger.info("Авторизуем пользователя с email %s", email)
        response = requests.post(
            LOGIN_ENDPOINT,
            json={"email": email, "password": password},
            timeout=REQUEST_TIMEOUT,
        )

        assert response.status_code == 201
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        body = response.json()
        assert "user" in body
        assert "token" in body
        assert body["user"]["email"] == email
        assert "access_token" in body["token"]
        logger.info("Пользователь успешно авторизован")
