"""Эндпоинты сервиса «Доска».

Модуль изолирует урлы API от тестовых данных.
"""

BASE_URL = "https://qa-desk.education-services.ru/api"

SIGNUP_ENDPOINT = f"{BASE_URL}/signup"
LOGIN_ENDPOINT = f"{BASE_URL}/signin"
CREATE_LISTING_ENDPOINT = f"{BASE_URL}/create-listing"
LISTINGS_ENDPOINT = f"{BASE_URL}/listings"
DELETE_LISTING_ENDPOINT = LISTINGS_ENDPOINT
UPDATE_OFFER_ENDPOINT = f"{BASE_URL}/update-offer"
PROFILE_LISTINGS_ENDPOINT = f"{BASE_URL}/profile/listings"
