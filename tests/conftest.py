from typing import Type

from pytest import fixture
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette import status

from src.config import settings
from src.database import get_db
from src.main import app
from src.models import Base, Todo
from src.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}_test"
)

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@fixture
def session() -> Session:
    """
    The function creates and closes the test session database,
    and deletes all and creates new values in the test database.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture
def client(session: Session) -> TestClient:
    """
    Test client initialization function.
    """

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app=app)


@fixture
def test_admin(client: TestClient) -> dict[str, int | str]:
    """
    The function creates an `admin` user.
    """
    admin_data = {
        "email": "vasyl.poremchuk@gmail.com",
        "username": "vasyl",
        "password": "It1smyv3rys3cur3p@ssw0rd!",
        "role": "admin",
        "first_name": "Vasyl",
        "last_name": "Poremchuk",
        "phone_number": "+380666222956",
    }
    response = client.post(url="/auth/", json=admin_data)

    assert response.status_code == status.HTTP_201_CREATED

    admin = response.json()
    admin["password"] = admin_data["password"]

    return admin


@fixture
def test_user(client: TestClient) -> dict[str, int | str]:
    """
    The function creates a `user`.
    """
    user_data = {
        "email": "lebron.james@gmail.com",
        "username": "lebron",
        "password": "L3br()nnn",
        "role": "user",
        "first_name": "Lebron",
        "last_name": "James",
        "phone_number": "+380503184923",
    }
    response = client.post(url="/auth/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED

    user = response.json()
    user["password"] = user_data["password"]

    return user


@fixture
def token_admin(test_admin: dict[str, int | str]) -> str:
    """
    The function creates an access token for the `admin` user.
    """
    return create_access_token(
        username=test_admin["username"],
        user_id=test_admin["user_id"],
        role=test_admin["role"],
    )


@fixture
def token_user(test_user: dict[str, int | str]) -> str:
    """
    The function creates an access token for the `user`.
    """
    return create_access_token(
        username=test_user["username"],
        user_id=test_user["user_id"],
        role=test_user["role"],
    )


@fixture
def authorized_admin_client(
    client: TestClient, token_admin: str
) -> TestClient:
    """
    The function that makes authorization for the `admin` user.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_admin}",
    }

    return client


@fixture
def authorized_user_client(client: TestClient, token_user: str) -> TestClient:
    """
    The function that makes authorization for the `user`.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_user}",
    }

    return client


@fixture
def test_todos(
    session: Session,
    test_admin: dict[str, int | str],
    test_user: dict[str, int | str],
) -> list[Type[Todo]]:
    """
    The function creates `todos` in the test database.
    """
    todos_data = [
        {
            "title": "Research Paper",
            "description": "Gather sources, take notes, and draft a research paper "
            "on the assigned topic. Follow formatting guidelines",
            "priority": 3,
            "complete": False,
            "owner_id": test_admin["user_id"],
        },
        {
            "title": "Plan Charity Event",
            "description": "Coordinate a charity event to support a local cause. "
            "Contact sponsors, find a venue, budget, and manage logistics",
            "priority": 5,
            "complete": False,
            "owner_id": test_admin["user_id"],
        },
        {
            "title": "Home Improvements",
            "description": "Paint the living room, fix the kitchen faucet, and organize "
            "the garage by decluttering and installing shelves.",
            "priority": 4,
            "complete": False,
            "owner_id": test_user["user_id"],
        },
    ]

    todos = [Todo(**todo) for todo in todos_data]

    session.add_all(todos)
    session.commit()

    return session.query(Todo).all()
