from pathlib import Path
import pytest

from crunchbase.crunchbase_api import CrunchBaseApi
from crunchbase.settings import settings


@pytest.fixture
def organization_json(resource_path_root: Path) -> str:
    """Fixture with fake organization json file."""
    return (
        (resource_path_root / "crunchbase" / "organizations" / "test_organization.json")
        .open("r")
        .read()
    )


@pytest.fixture
def crunchbase_api():
    """Test CrunchBase API."""
    return CrunchBaseApi(api_key="FAKE_API_KEY", base_url=settings.base_url)
