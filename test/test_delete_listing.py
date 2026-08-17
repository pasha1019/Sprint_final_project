"""Тесты функциональности «Удаление объявления»."""

import logging

import requests

from data.data import DELETE_SUCCESS_MESSAGE, MAX_RESPONSE_TIME, REQUEST_TIMEOUT
from data.endpoints import LISTINGS_ENDPOINT, PROFILE_LISTINGS_ENDPOINT
from helpers.listing_helper import ListingHelper

logger = logging.getLogger(__name__)


class TestDeleteListing:
    def test_delete_listing_success(self, registered_user_token, created_listing):
        """Удаление объявления: сервис возвращает 200 и сообщение об удалении.

        Given: существующее объявление
        When: выполняется DELETE /api/listings/{id}
        Then: сервис возвращает 200 и сообщение об успешном удалении
        """
        token = registered_user_token
        listing_id = created_listing["id"]

        logger.info("Удаляем объявление с id %s", listing_id)
        response = ListingHelper.delete_listing(token, listing_id)

        assert response.status_code == 200
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        assert response.json()["message"] == DELETE_SUCCESS_MESSAGE

    def test_deleted_listing_absent_from_feed(
        self, registered_user_token, created_listing
    ):
        """После удаления объявления нет в ленте.

        Given: существующее объявление
        When: объявление удаляется, затем запрашивается лента
        Then: объявления с удалённым id нет в ленте
        """
        token = registered_user_token
        listing_id = created_listing["id"]

        logger.info("Удаляем объявление с id %s", listing_id)
        ListingHelper.delete_listing(token, listing_id)

        feed_response = requests.get(
            f"{LISTINGS_ENDPOINT}/1",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT,
        )
        assert feed_response.status_code == 200
        assert feed_response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        feed = feed_response.json()
        assert "offers" in feed
        assert all(str(offer["id"]) != str(listing_id) for offer in feed["offers"])
        logger.info("Объявление отсутствует в ленте")

    def test_deleted_listing_absent_from_profile(
        self, registered_user_token, created_listing
    ):
        """После удаления объявления нет в профиле пользователя.

        Given: существующее объявление
        When: объявление удаляется, затем запрашивается профиль пользователя
        Then: объявления с удалённым id нет в профиле
        """
        token = registered_user_token
        listing_id = created_listing["id"]

        logger.info("Удаляем объявление с id %s", listing_id)
        ListingHelper.delete_listing(token, listing_id)

        profile_response = requests.get(
            f"{PROFILE_LISTINGS_ENDPOINT}/1",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT,
        )
        assert profile_response.status_code == 200
        assert profile_response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        profile = profile_response.json()
        assert "offers" in profile
        assert all(str(offer["id"]) != str(listing_id) for offer in profile["offers"])
        logger.info("Объявление отсутствует в профиле")
