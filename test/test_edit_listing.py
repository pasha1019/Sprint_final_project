"""Тесты функциональности «Редактирование объявления»."""

import logging

import pytest
import requests

from data.data import (
    EDITABLE_FIELDS,
    ERROR_401_EDIT_FORBIDDEN,
    MAX_RESPONSE_TIME,
    REQUEST_TIMEOUT,
)
from data.endpoints import LOGIN_ENDPOINT
from helpers.generators import default_listing_payload, edited_listing_payload
from helpers.listing_helper import get_listing_from_feed, update_listing

logger = logging.getLogger(__name__)


class TestEditListing:

    @pytest.mark.parametrize("field", EDITABLE_FIELDS)
    def test_edit_listing_success(self, registered_user_token, created_listing, field):
        """Редактирование каждого поля объявления.

        Given: существующее объявление и новое значение поля
        When: выполняется PATCH /api/update-offer/{id}
        Then: сервис возвращает 200, поле изменено в ответе и в ленте
        """
        token = registered_user_token
        new_payload = edited_listing_payload(field)

        logger.info("Редактируем поле %s", field)
        response = update_listing(token, created_listing["id"], new_payload)

        assert response.status_code == 200
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        body = response.json()
        assert body["id"] == created_listing["id"]
        assert body[field] == new_payload[field]

        feed_offer = get_listing_from_feed(created_listing["id"], token)
        assert feed_offer is not None, "Объявление не найдено в ленте"
        assert feed_offer[field] == new_payload[field]
        logger.info("Поле %s изменено и подтверждено в ленте", field)

    def test_edit_foreign_listing_fails(self, foreign_user, registered_user_token, created_listing):
        """Редактирование объявления, созданного другим пользователем.

        Given: «чужой» пользователь и объявление другого пользователя
        When: выполняется попытка редактирования
        Then: сервис возвращает 401 и сообщение об отсутствии прав
        """
        foreign_email, foreign_password, _ = foreign_user
        login_response = requests.post(
            LOGIN_ENDPOINT,
            json={"email": foreign_email, "password": foreign_password},
            timeout=REQUEST_TIMEOUT,
        )
        if login_response.status_code != 201:
            pytest.fail("Не удалось авторизовать «чужого» пользователя")
        foreign_token = login_response.json()["token"]["access_token"]

        logger.info("Пытаемся отредактировать чужое объявление")
        response = update_listing(foreign_token, created_listing["id"], default_listing_payload())

        assert response.status_code == 401
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        assert response.json()["message"] == ERROR_401_EDIT_FORBIDDEN
        logger.info("Сервис вернул ожидаемый отказ в редактировании")
