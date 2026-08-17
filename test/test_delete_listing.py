"""Тесты функциональности «Удаление объявления»."""

import logging

import requests

from data.data import DELETE_SUCCESS_MESSAGE, MAX_RESPONSE_TIME, REQUEST_TIMEOUT
from data.endpoints import LISTINGS_ENDPOINT, PROFILE_LISTINGS_ENDPOINT
from helpers.listing_helper import delete_listing

logger = logging.getLogger(__name__)


class TestDeleteListing:

    def test_delete_listing_success(self, registered_user_token, created_listing):
        """Удаление объявления.

        Given: существующее объявление
        When: выполняется DELETE /api/listings/{id}
        Then: сервис возвращает 200, объявления нет в ленте и в профиле
        """
        token = registered_user_token
        listing_id = created_listing["id"]

        logger.info("Удаляем объявление с id %s", listing_id)
        response = delete_listing(token, listing_id)

        assert response.status_code == 200
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        assert response.json()["message"] == DELETE_SUCCESS_MESSAGE

        # Объявления не должно быть ни в ленте, ни в профиле пользователя
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
        logger.info("Объявление отсутствует в ленте и в профиле")
