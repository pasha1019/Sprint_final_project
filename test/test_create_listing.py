"""Тесты функциональности «Создание объявления»."""

import logging

import pytest

from data.data import MAX_RESPONSE_TIME, VALID_CATEGORIES
from data.schemas import ListingResponse
from helpers.generators import Generators
from helpers.listing_helper import ListingHelper

logger = logging.getLogger(__name__)


class TestCreateListing:
    @pytest.mark.parametrize("category", VALID_CATEGORIES)
    def test_create_listing_success(self, registered_user_token, category):
        """Создание объявления в заданной категории.

        Given: авторизованный пользователь и валидная категория
        When: создаётся объявление в этой категории
        Then: сервис возвращает 201, поля совпадают с переданными,
        объявление появляется в профиле владельца
        """
        payload = Generators.default_listing_payload()
        payload["category"] = category

        logger.info("Создаём объявление в категории %s", category)
        response = ListingHelper.create_listing(registered_user_token, payload)

        assert response.status_code == 201
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        listing = ListingResponse.model_validate(response.json())
        assert listing.model_dump(exclude={"id"}) == payload

        profile_offer = ListingHelper.get_listing_from_profile(
            listing.id, registered_user_token
        )
        assert profile_offer is not None, "Объявление не появилось в профиле владельца"
        assert (
            ListingResponse.model_validate(profile_offer).model_dump(exclude={"id"})
            == payload
        )
        logger.info("Объявление найдено в профиле владельца")

        ListingHelper.delete_listing(registered_user_token, listing.id)
