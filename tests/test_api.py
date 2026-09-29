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
        roles={"umm": {"roles": ["user"]}}
    )


@pytest.fixture
def mock_admin_user():
    return User(
        username="adminuser",
        family_name="Admin",
        given_name="User",
        name="Admin User",
        scope=["openid profile email"],
        roles={"umm": {"roles": ["user", "admin"]}}
    )


def test_public_endpoint(client):
    """Test that /public endpoint is accessible without authentication"""
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "Anyone can see this"}


def test_public_endpoint_cors(client):
    """Test that /public endpoint has proper CORS headers"""
    response = client.get("/public", headers={"Origin": "http://localhost:5174"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_user_endpoint_without_auth(client):
    """Test that /user endpoint returns 401 without authentication"""
    response = client.get("/user")
    assert response.status_code == 401


def test_user_endpoint_with_auth(client_with_auth):
    """Test that /user endpoint returns user data with valid authentication"""
    response = client_with_auth.get("/user")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello User testuser"}


def test_me_roles_endpoint(client_with_auth):
    """Test that /me/roles endpoint returns user roles"""
    response = client_with_auth.get("/me/roles")
    assert response.status_code == 200
    assert response.json() == ["user"]


def test_me_roles_endpoint_admin(client_with_auth, mock_admin_user):
    """Test that /me/roles endpoint returns admin roles for admin user"""
    app = app_maker()

    def override_get_current_user():
        return mock_admin_user

    from fastapi_keycloak.keycloak_integration import get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user

    test_client = TestClient(app)
    response = test_client.get("/me/roles")
    assert response.status_code == 200
    assert set(response.json()) == {"user", "admin"}

    app.dependency_overrides.clear()


def test_user_has_role(mock_user):
    """Test User.has_role method"""
    assert mock_user.has_role("umm", "user") is True
    assert mock_user.has_role("umm", "admin") is False
    assert mock_user.has_role("other-context", "user") is False


def test_user_has_role_admin(mock_admin_user):
    """Test User.has_role method with admin user"""
    assert mock_admin_user.has_role("umm", "user") is True
    assert mock_admin_user.has_role("umm", "admin") is True
    assert mock_admin_user.has_role("umm", "superadmin") is False


def test_user_roles_context(mock_user):
    """Test that user roles are context-specific"""
    assert "user" in mock_user.roles["umm"]
    assert mock_user.roles.get("other-context") is None


def test_public_endpoint_post(client):
    """Test that POST to /public is not allowed (if not implemented)"""
    response = client.post("/public")
    # Should return 405 Method Not Allowed or 404
    assert response.status_code in [405, 404]
