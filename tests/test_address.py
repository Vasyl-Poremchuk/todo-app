from fastapi.testclient import TestClient
from pytest import mark
from starlette import status

from src.schemas import UserResponse


@mark.parametrize(
    "city, state, country, postal_code",
    [
        ("Kyiv", "Kyiv", "Ukraine", "01001"),
        ("Odessa", "Odessa", "Ukraine", "65037"),
        ("Lviv", "Lviv", "Ukraine", "79007"),
    ],
)
def test_unauthorized_user_create_address(
    client: TestClient, city: str, state: str, country: str, postal_code: str
) -> None:
    response = client.post(
        url="/addresses/",
        json={
            "city": city,
            "state": state,
            "country": country,
            "postal_code": postal_code,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@mark.parametrize(
    "city, state, country, postal_code",
    [
        ("Kyiv", "Kyiv", "Ukraine", "01001"),
        ("Odessa", "Odessa", "Ukraine", "65037"),
        ("Lviv", "Lviv", "Ukraine", "79007"),
    ],
)
def test_authorized_user_create_address(
    authorized_user_client: TestClient,
    city: str,
    state: str,
    country: str,
    postal_code: str,
) -> None:
    response = authorized_user_client.post(
        url="/addresses/",
        json={
            "city": city,
            "state": state,
            "country": country,
            "postal_code": postal_code,
        },
    )

    response_after_creation = authorized_user_client.get(url="/users/me")

    user = UserResponse(**response_after_creation.json())

    assert user.address.city == city
    assert user.address.state == state
    assert user.address.country == country
    assert user.address.postal_code == postal_code
    assert response.status_code == status.HTTP_201_CREATED
