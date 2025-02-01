import pytest
import requests
from requests import HTTPError

from crunchbase.settings import settings
from crunchbase.crunchbase_api import CrunchBaseApi
from crunchbase.schemas.organization import Organization


FAKE_API_KEY = "test"
TEST_ENTITY_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
TEST_URL = f"{settings.base_url}{CrunchBaseApi.ORGANIZATION_URL}/{TEST_ENTITY_ID}"


def test_crunchbase_api():
    """Test CrunchBase API."""

    # Test API key and base URL not specified
    with pytest.raises(ValueError, match="API key for CrunchBase not specified"):
        CrunchBaseApi(api_key="", base_url="")
    with pytest.raises(ValueError, match="Base URL for CrunchBase not specified"):
        CrunchBaseApi(api_key="test", base_url="")

    CrunchBaseApi(api_key=FAKE_API_KEY, base_url=settings.base_url)


def test_crunchbase_get_organisation(requests_mock, crunchbase_api, organization_json):
    """Test get organization from CrunchBase API."""

    requests_mock.get(TEST_URL, text=organization_json)

    # Test get organization
    org = crunchbase_api.get_organization(TEST_ENTITY_ID)
    assert org == Organization.model_validate_json(organization_json)

    # Test entity ID not specified
    with pytest.raises(ValueError, match="Entity ID not specified"):
        crunchbase_api.get_organization(entity_id=None)

    # Test entity ID cannot be empty
    with pytest.raises(ValueError, match="Entity ID cannot be empty"):
        crunchbase_api.get_organization("")

    # Test entity ID must be 36 characters long
    with pytest.raises(ValueError, match="Entity ID must be 36 characters long"):
        crunchbase_api.get_organization("test")


def test_crunchbase_get_organisation_http_errors(requests_mock, crunchbase_api):
    """Test get organization from CrunchBase API with HTTP errors."""

    # Test 404 error
    requests_mock.register_uri(
        "GET",
        TEST_URL,
        exc=requests.exceptions.HTTPError("404 Client Error: Not Found"),
    )
    with pytest.raises(HTTPError, match="404 Client Error: Not Found"):
        crunchbase_api.get_organization(TEST_ENTITY_ID)

    # Test 500 error
    requests_mock.register_uri(
        "GET",
        TEST_URL,
        exc=requests.exceptions.HTTPError("500 Server Error: Internal Server Error"),
    )
    with pytest.raises(HTTPError, match="500 Server Error: Internal Server Error"):
        crunchbase_api.get_organization(TEST_ENTITY_ID)
