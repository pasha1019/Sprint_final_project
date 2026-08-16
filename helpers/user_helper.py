"""Хелперы для работы с пользователем: регистрация через API."""

import requests

from data.data import (
    REQUEST_TIMEOUT,
    SIGNUP_ENDPOINT,
    random_password,
    unique_email,
)


def register_new_user_and_return_creds():
    """Регистрирует нового пользователя и возвращает (email, password, token).

    Токен извлекается из `access_token.access_token` — такова структура
    ответа POST /api/signup. В случае неудачи возвращает None.
    """
    email = unique_email()
    password = random_password()

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
