from fastapi.testclient import TestClient
from jose import jwt
from pytest import mark
from starlette import status

from src.oauth2 import ALGORITHM, SECRET_KEY
from src.schemas import Token, UserResponse


def test_create_user(client: TestClient) -> None:
    response = client.post(
        url="/auth/",
        json={
            "email": "michael.jordan@gmail.com",
            "username": "michael",
            "password": "P@ssw0rd",
            "role": "user",
            "first_name": "Michael",
            "last_name": "Jordan",
            "phone_number": "+380503184759",
        },
    )
    user = UserResponse(**response.json())

    assert user.email == "michael.jordan@gmail.com"
    assert response.status_code == status.HTTP_201_CREATED


def test_login_user(
    client: TestClient, test_user: dict[str, int | str]
) -> None:
    response = client.post(
        url="/auth/token/",
        data={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )
    login_response = Token(**response.json())
    payload = jwt.decode(
        token=login_response.access_token,
        key=SECRET_KEY,
        algorithms=[ALGORITHM],
    )
    username = payload.get("sub")
    user_id = payload.get("user_id")
    role = payload.get("role")

    assert username == test_user["username"]
    assert user_id == test_user["user_id"]
    assert role == test_user["role"]
    assert response.status_code == status.HTTP_201_CREATED
    assert login_response.token_type == "bearer"


@mark.parametrize(
    "username, password, status_code",
    [
        (
            "michal",
            "P@ssw0rd",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "michael",
            "Password",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "michal",
            "Password",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            None,
            "P@ssw0rd",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "michael",
            None,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_invalid_credentials(
    client: TestClient,
    test_user: dict[str, int | str],
    username: str | None,
    password: str | None,
    status_code: int,
) -> None:
    response = client.post(
        url="/auth/token", data={"username": username, "password": password}
    )

    assert response.status_code == status_code
