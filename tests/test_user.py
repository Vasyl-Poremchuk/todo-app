from fastapi.testclient import TestClient
from starlette import status

from src.schemas import UserResponse


def test_unauthorized_user_get_info(client: TestClient) -> None:
    response = client.get(url="/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_get_info(authorized_user_client: TestClient) -> None:
    response = authorized_user_client.get(url="/users/me/")
    user = UserResponse(**response.json())

    assert user.email == "lebron.james@gmail.com"
    assert user.username == "lebron"
    assert user.role == "user"
    assert user.first_name == "Lebron"
    assert user.last_name == "James"
    assert user.phone_number == "+380503184923"
    assert response.status_code == status.HTTP_200_OK


def test_unauthorized_user_reset_password(client: TestClient) -> None:
    response = client.put(
        url="/users/reset-password",
        json={"password": "L3br()nnn", "new_password": "N3wp@ssw0rd"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_reset_password(
    authorized_user_client: TestClient,
) -> None:
    response = authorized_user_client.put(
        url="/users/reset-password",
        json={"password": "L3br()nnn", "new_password": "N3wp@ssw0rd"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
