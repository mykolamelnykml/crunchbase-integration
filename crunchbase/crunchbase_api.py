import logging
from typing import Any

import requests
from crunchbase.schemas.organization import Organization
from crunchbase.settings import settings

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)


class RateLimitError(Exception):
    pass


class CrunchBaseApi:
    """
    Class to interact with CrunchBase API.
    """

    ORGANIZATION_URL = "data/entities/organizations"

    def __init__(self, api_key: str, base_url: str) -> None:
        """Initialize CrunchBase API client."""
        logging.info("Initializing CrunchBase API client")
        if not api_key:
            raise ValueError("API key for CrunchBase not specified")
        if not base_url:
            raise ValueError("Base URL for CrunchBase not specified")
        self.api_key = api_key
        self.base_url = base_url

    def get_organization(self, entity_id: str) -> Organization:
        """Get organization info from CrunchBase API."""

        logging.info("Getting organization info from CrunchBase API")

        if entity_id is None:
            raise ValueError("Entity ID not specified")
        if not entity_id:
            raise ValueError("Entity ID cannot be empty")
        if len(entity_id) != 36:
            raise ValueError("Entity ID must be 36 characters long")

        url = f"{self.base_url}{self.ORGANIZATION_URL}/{entity_id}"

        headers = {"accept": "application/json"}

        @retry(
            retry=retry_if_exception_type(RateLimitError),
            wait=wait_random_exponential(min=1, max=settings.api_delay),
            stop=stop_after_attempt(settings.api_max_retry),
        )
        def request_get_with_backoff(*args: Any, **kwargs: Any):
            # Here we can also handle networks errors, timeouts, etc.
            return requests.get(*args, **kwargs)

        response = request_get_with_backoff(url, headers=headers)

        response.raise_for_status()

        return Organization.model_validate(response.json())
