"""Тесты функциональности «Создание объявления»."""

import logging

import pytest

from data.data import MAX_RESPONSE_TIME, VALID_CATEGORIES
from helpers.generators import default_listing_payload
from helpers.listing_helper import create_listing, delete_listing, get_listing_from_feed

logger = logging.getLogger(__name__)


class TestCreateListing:

    @pytest.mark.parametrize("category", VALID_CATEGORIES)
    def test_create_listing_success(self, registered_user_token, category):
        """Создание объявления в заданной категории.

        Given: авторизованный пользователь и валидная категория
        When: создаётся объявление в этой категории
        Then: сервис возвращает 201, поля совпадают с переданными,
        объявление появляется в ленте
        """
        payload = default_listing_payload()
        payload["category"] = category

        logger.info("Создаём объявление в категории %s", category)
        response = create_listing(registered_user_token, payload)

        assert response.status_code == 201
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        body = response.json()
        assert body["category"] == category
        assert body["name"] == payload["name"]
        assert body["condition"] == payload["condition"]
        assert body["city"] == payload["city"]
        assert body["description"] == payload["description"]
        assert body["price"] == payload["price"]

        feed_offer = get_listing_from_feed(body["id"], registered_user_token)
        assert feed_offer is not None, "Объявление не появилось в ленте"
        assert feed_offer["name"] == payload["name"]
        logger.info("Объявление найдено в ленте")

        delete_listing(registered_user_token, body["id"])
