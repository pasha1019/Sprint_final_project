"""Хелперы для работы с пользователем: регистрация и авторизация через API."""

import requests

from data.data import REQUEST_TIMEOUT
from data.endpoints import LOGIN_ENDPOINT, SIGNUP_ENDPOINT
from helpers.generators import Generators


class UserHelper:
    """API-методы пользователя: регистрация и получение токена."""

    @staticmethod
    def register_new_user_and_return_creds():
        """Регистрирует нового пользователя и возвращает (email, password, token).

        Токен извлекается из `access_token.access_token` — такова структура
        ответа POST /api/signup. В случае неудачи возвращает None.
        """
        email = Generators.unique_email()
        password = Generators.random_password()

        payload = {
            "email": email,
            "password": password,
            "submitPassword": password,
        }

        response = requests.post(SIGNUP_ENDPOINT, json=payload, timeout=REQUEST_TIMEOUT)

        if response.status_code == 201:
            body = response.json()
            token = body.get("access_token", {}).get("access_token")
            return email, password, token
        return None

    @staticmethod
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
