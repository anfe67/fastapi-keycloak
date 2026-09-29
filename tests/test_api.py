import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from fastapi_keycloak.main import app_maker
from fastapi_keycloak.keycloak_integration import User


@pytest.fixture
def client():
    app = app_maker()
    return TestClient(app)


@pytest.fixture
def client_with_auth(mock_user):
    app = app_maker()
    
    def override_get_current_user():
        return mock_user
    
    from fastapi_keycloak.keycloak_integration import get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()


@pytest.fixture
def mock_user():
    return User(
        username="testuser",
        family_name="Test",
        given_name="User",
        name="Test User",
        scope=["openid profile email"],
        roles={"example-client": {"roles": ["user"]}}
    )


def test_public_endpoint(client):
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "Anyone can see this"}


def test_user_endpoint_without_auth(client):
    response = client.get("/user")
    assert response.status_code == 401


def test_user_endpoint_with_auth(client_with_auth):
    response = client_with_auth.get("/user")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello User testuser"}


def test_me_roles_endpoint(client_with_auth):
    response = client_with_auth.get("/me/roles")
    assert response.status_code == 200
    assert response.json() == ["user"]


@patch("fastapi_keycloak.keycloak_integration.get_current_user")
def test_user_has_role(mock_get_current_user, mock_user):
    mock_get_current_user.return_value = mock_user
    assert mock_user.has_role("example-client", "user") is True
    assert mock_user.has_role("example-client", "admin") is False
