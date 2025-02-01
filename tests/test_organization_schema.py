from crunchbase.schemas.organization import Organization


def test_organization(organization_json):
    """Test organization model."""
    Organization.model_validate_json(organization_json)
