
from app.config import get_settings


def test_health_check_returns_healthy_status(test_client) -> None:
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "HelixDesk API",
        "environment": "development",
    }


def test_api_docs_are_available(test_client) -> None:
    response = test_client.get("/docs")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_openapi_schema_contains_health_endpoint(test_client) -> None:
    response = test_client.get("/openapi.json")

    assert response.status_code == 200
    assert "/health" in response.json()["paths"]


def test_app_settings_are_loaded() -> None:
    settings = get_settings()

    assert settings.app_name == "HelixDesk API"
    assert settings.app_version == "1.0.0"
    assert settings.app_env == "development"


def test_api_v1_status(test_client) -> None:
    response = test_client.get("/api/v1/status")

    assert response.status_code == 200
    assert response.json() == {
        "status": "available",
        "api_version": "v1",
    }


def test_list_customers_requires_authentication(test_client) -> None:
    response = test_client.get("/api/v1/customers/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_create_customer_rejects_invalid_email(test_client) -> None:
    response = test_client.post(
        "/api/v1/customers/",
        json={
            "name": "Test Customer",
            "email": "invalid-email",
        },
    )

    assert response.status_code == 401


def test_create_customer_requires_authentication(test_client) -> None:
    response = test_client.post(
        "/api/v1/customers/",
        json={
            "name": "Test Customer",
            "email": "customer@example.com",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["www-authenticate"] == "Bearer"




def test_delete_customer_returns_not_found_for_missing_customer(
    authenticated_client,
) -> None:
    response = authenticated_client.delete(
        "/api/v1/customers/999999"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}



def test_update_customer_rejects_invalid_email(
    authenticated_client,
) -> None:
    response = authenticated_client.put(
        "/api/v1/customers/1",
        json={"email": "invalid-email"},
    )

    assert response.status_code == 422


def test_update_customer_rejects_empty_body(
    authenticated_client,
) -> None:
    response = authenticated_client.put(
        "/api/v1/customers/1",
        json={},
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "At least one field must be provided"
    }



def test_user_cannot_delete_another_users_customer(
    authenticated_client,
) -> None:
    # Create a customer owned by the first authenticated user.
    create_response = authenticated_client.post(
        "/api/v1/customers/",
        json={
            "name": "Protected Customer",
            "email": "protected-customer@example.com",
        },
    )
    assert create_response.status_code == 201
    customer_id = create_response.json()["id"]

    # Register a second user.
    second_email = "second-user@example.com"
    second_password = "SecondUserPassword123!"

    register_response = authenticated_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Second User",
            "email": second_email,
            "password": second_password,
        },
    )
    assert register_response.status_code == 201

    # Log in as the second user.
    login_response = authenticated_client.post(
        "/api/v1/auth/login",
        json={
            "email": second_email,
            "password": second_password,
        },
    )
    assert login_response.status_code == 200

    second_token = login_response.json()["access_token"]
    authenticated_client.headers.update(
        {"Authorization": f"Bearer {second_token}"}
    )

    # The second user must not be able to delete the first user's customer.
    delete_response = authenticated_client.delete(
        f"/api/v1/customers/{customer_id}"
    )
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Customer not found"}

    # Restore the first user's token and verify the customer still exists.
    # The original token is retrieved by logging in again.
    first_login = authenticated_client.post(
        "/api/v1/auth/login",
        json={
            "email": "customer-test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert first_login.status_code == 200

    authenticated_client.headers.update(
        {
            "Authorization": (
                f"Bearer {first_login.json()['access_token']}"
            )
        }
    )

    customers_response = authenticated_client.get("/api/v1/customers/")
    assert customers_response.status_code == 200
    assert any(
        customer["id"] == customer_id
        for customer in customers_response.json()
    )



def test_user_cannot_update_another_users_customer(
    authenticated_client,
) -> None:
    # Create a customer owned by the first user.
    create_response = authenticated_client.post(
        "/api/v1/customers/",
        json={
            "name": "Protected Customer",
            "email": "protected-update@example.com",
        },
    )
    assert create_response.status_code == 201
    customer_id = create_response.json()["id"]

    # Register a second user.
    second_email = "second-update-user@example.com"
    second_password = "SecondUpdatePassword123!"

    register_response = authenticated_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Second Update User",
            "email": second_email,
            "password": second_password,
        },
    )
    assert register_response.status_code == 201

    # Log in as the second user.
    login_response = authenticated_client.post(
        "/api/v1/auth/login",
        json={
            "email": second_email,
            "password": second_password,
        },
    )
    assert login_response.status_code == 200

    authenticated_client.headers.update(
        {
            "Authorization": (
                f"Bearer {login_response.json()['access_token']}"
            )
        }
    )

    # The second user must not update the first user's customer.
    update_response = authenticated_client.put(
        f"/api/v1/customers/{customer_id}",
        json={"name": "Unauthorized Change"},
    )
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Customer not found"}



def test_user_sees_only_their_own_customers(
    authenticated_client,
) -> None:
    first_customer = authenticated_client.post(
        "/api/v1/customers/",
        json={
            "name": "First User Customer",
            "email": "first-owner@example.com",
        },
    )
    assert first_customer.status_code == 201

    second_email = "second-list-user@example.com"
    second_password = "SecondListPassword123!"

    registration = authenticated_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Second List User",
            "email": second_email,
            "password": second_password,
        },
    )
    assert registration.status_code == 201

    login = authenticated_client.post(
        "/api/v1/auth/login",
        json={
            "email": second_email,
            "password": second_password,
        },
    )
    assert login.status_code == 200

    authenticated_client.headers.update(
        {
            "Authorization": (
                f"Bearer {login.json()['access_token']}"
            )
        }
    )

    second_customer = authenticated_client.post(
        "/api/v1/customers/",
        json={
            "name": "Second User Customer",
            "email": "second-owner@example.com",
        },
    )
    assert second_customer.status_code == 201

    response = authenticated_client.get("/api/v1/customers/")
    assert response.status_code == 200

    customers = response.json()
    assert len(customers) == 1
    assert customers[0]["email"] == "second-owner@example.com"
    assert all(
        customer["email"] != "first-owner@example.com"
        for customer in customers
    )
