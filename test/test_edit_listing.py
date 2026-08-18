"""Тесты функциональности «Редактирование объявления»."""

import logging

import pytest

from data.data import EDITABLE_FIELDS, ERROR_401_EDIT_FORBIDDEN, MAX_RESPONSE_TIME
from data.schemas import ListingResponse
from helpers.generators import Generators
from helpers.listing_helper import ListingHelper

logger = logging.getLogger(__name__)


class TestEditListing:
    @pytest.mark.parametrize("field", EDITABLE_FIELDS)
    def test_edit_listing_success(self, registered_user_token, created_listing, field):
        """Редактирование каждого поля объявления.

        Given: существующее объявление и новое значение поля
        When: выполняется PATCH /api/update-offer/{id}
        Then: сервис возвращает 200, поле изменено в ответе и в профиле владельца
        """
        token = registered_user_token
        new_payload = Generators.edited_listing_payload(field)

        logger.info("Редактируем поле %s", field)
        response = ListingHelper.update_listing(
            token, created_listing["id"], new_payload
        )

        assert response.status_code == 200
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        listing = ListingResponse.model_validate(response.json())
        assert listing.id == created_listing["id"]
        assert listing.model_dump(exclude={"id"}) == new_payload

        profile_offer = ListingHelper.get_listing_from_profile(
            created_listing["id"], token
        )
        assert profile_offer is not None, "Объявление не найдено в профиле владельца"
        assert (
            ListingResponse.model_validate(profile_offer).model_dump(exclude={"id"})
            == new_payload
        )
        logger.info("Поле %s изменено и подтверждено в профиле владельца", field)

    def test_edit_foreign_listing_fails(
        self, foreign_user, registered_user_token, created_listing
    ):
        """Редактирование объявления, созданного другим пользователем.

        Given: «чужой» пользователь и объявление другого пользователя
        When: выполняется попытка редактирования
        Then: сервис возвращает 401 и сообщение об отсутствии прав
        """
        _, _, foreign_token = foreign_user

        logger.info("Пытаемся отредактировать чужое объявление")
        response = ListingHelper.update_listing(
            foreign_token, created_listing["id"], Generators.default_listing_payload()
        )

        assert response.status_code == 401
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME
        assert response.json()["message"] == ERROR_401_EDIT_FORBIDDEN
        logger.info("Сервис вернул ожидаемый отказ в редактировании")
