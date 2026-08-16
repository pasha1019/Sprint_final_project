"""Хелперы для работы с объявлениями: создание, редактирование, удаление.

Обратите внимание: create/update объявлений отправляются сервису
как multipart/form-data, а не как JSON.
"""

import requests

from data.data import (
    CREATE_LISTING_ENDPOINT,
    DELETE_LISTING_ENDPOINT,
    REQUEST_TIMEOUT,
    UPDATE_OFFER_ENDPOINT,
    default_listing_payload,
)


def _to_multipart(payload):
    """Преобразует dict-словарь в multipart/form-data для requests."""
    return {key: (None, str(value)) for key, value in payload.items()}


def create_listing(token, payload=None):
    """Создаёт объявление и возвращает объект requests.Response.

    Статус, время ответа и состав тела проверяются в тестах.
    """
    form_data = _to_multipart(payload or default_listing_payload())
    return requests.post(
        CREATE_LISTING_ENDPOINT,
        files=form_data,
        headers={"Authorization": f"Bearer {token}"},
        timeout=REQUEST_TIMEOUT,
    )


def update_listing(token, listing_id, payload):
    """Обновляет объявление через PATCH /api/update-offer/{id}.

    Возвращает полный объект response — статус и тело проверяются в тестах.
    """
    response = requests.patch(
        f"{UPDATE_OFFER_ENDPOINT}/{listing_id}",
        files=_to_multipart(payload),
        headers={"Authorization": f"Bearer {token}"},
        timeout=REQUEST_TIMEOUT,
    )
    return response


def delete_listing(token, listing_id):
    """Удаляет объявление по id и возвращает объект response."""
    return requests.delete(
        f"{DELETE_LISTING_ENDPOINT}/{listing_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=REQUEST_TIMEOUT,
    )
