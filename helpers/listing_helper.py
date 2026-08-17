"""Хелперы для работы с объявлениями: создание, редактирование, удаление, поиск в ленте.

Обратите внимание: create/update объявлений отправляются сервису
как multipart/form-data, а не как JSON.
"""

import requests

from data.data import REQUEST_TIMEOUT
from data.endpoints import (
    CREATE_LISTING_ENDPOINT,
    DELETE_LISTING_ENDPOINT,
    LISTINGS_ENDPOINT,
    UPDATE_OFFER_ENDPOINT,
)
from helpers.generators import Generators


class ListingHelper:
    """API-методы объявлений: создание, редактирование, удаление, поиск в ленте."""

    @staticmethod
    def _to_multipart(payload):
        """Преобразует dict-словарь в multipart/form-data для requests."""
        return {key: (None, str(value)) for key, value in payload.items()}

    @staticmethod
    def create_listing(token, payload=None):
        """Создаёт объявление и возвращает объект requests.Response.

        Статус, время ответа и состав тела проверяются в тестах.
        """
        form_data = ListingHelper._to_multipart(payload or Generators.default_listing_payload())
        return requests.post(
            CREATE_LISTING_ENDPOINT,
            files=form_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    def update_listing(token, listing_id, payload):
        """Обновляет объявление через PATCH /api/update-offer/{id}.

        Возвращает полный объект response — статус и тело проверяются в тестах.
        """
        response = requests.patch(
            f"{UPDATE_OFFER_ENDPOINT}/{listing_id}",
            files=ListingHelper._to_multipart(payload),
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT,
        )
        return response

    @staticmethod
    def delete_listing(token, listing_id):
        """Удаляет объявление по id и возвращает объект response."""
        return requests.delete(
            f"{DELETE_LISTING_ENDPOINT}/{listing_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
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