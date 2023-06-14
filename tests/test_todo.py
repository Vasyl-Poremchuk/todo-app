from typing import Type

from fastapi.testclient import TestClient
from pytest import mark
from starlette import status

from src.models import Todo
from src.schemas import TodoResponse


def test_unauthorized_user_read_todos(
    client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = client.get(url="/todos/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_read_todos(
    authorized_user_client: TestClient, test_todos: dict[Type[Todo]]
) -> None:
    response = authorized_user_client.get(url="/todos/")

    todos = [TodoResponse(**todo) for todo in response.json()]

    assert len(todos) == 1
    assert response.status_code == status.HTTP_200_OK


def test_unauthorized_user_read_todo(
    client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = client.get(url=f"/todos/{test_todos[2]}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_read_not_existent_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_user_client.get(url="/todos/7")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authorized_user_read_not_own_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_user_client.get(
        url=f"/todos/{test_todos[0].todo_id}"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authorized_user_read_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_user_client.get(
        url=f"/todos/{test_todos[2].todo_id}"
    )

    todo = TodoResponse(**response.json())

    assert todo.title == test_todos[2].title
    assert todo.description == test_todos[2].description
    assert todo.priority == test_todos[2].priority
    assert todo.complete == test_todos[2].complete
    assert todo.owner.user_id == test_todos[2].owner_id
    assert response.status_code == status.HTTP_200_OK


@mark.parametrize(
    "title, description, priority, complete",
    [
        (
            "Buy Groceries",
            "Get essential items from the store.",
            4,
            False,
        ),
        (
            "Prepare Presentation",
            "Research, create slides, rehearse.",
            2,
            True,
        ),
    ],
)
def test_unauthorized_user_create_todo(
    client: TestClient,
    title: str,
    description: str,
    priority: int,
    complete: bool,
) -> None:
    response = client.post(
        url="/todos/",
        json={
            "title": title,
            "description": description,
            "priority": priority,
            "complete": complete,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@mark.parametrize(
    "title, description, priority, complete",
    [
        (
            "Buy Groceries",
            "Get essential items from the store.",
            4,
            False,
        ),
        (
            "Prepare Presentation",
            "Research, create slides, rehearse.",
            2,
            True,
        ),
    ],
)
def test_authorized_user_create_todo(
    authorized_user_client: TestClient,
    title: str,
    description: str,
    priority: int,
    complete: bool,
) -> None:
    response = authorized_user_client.post(
        url="/todos/",
        json={
            "title": title,
            "description": description,
            "priority": priority,
            "complete": complete,
        },
    )

    todo = TodoResponse(**response.json())

    assert todo.title == title
    assert todo.description == description
    assert todo.priority == priority
    assert todo.complete == complete
    assert response.status_code == status.HTTP_201_CREATED


def test_unauthorized_user_update_todo(
    client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    data = {
        "title": "Exercise Routine",
        "description": "Set a workout routine. Stay consistent.",
        "priority": 5,
        "complete": False,
    }

    response = client.put(url=f"/todos/{test_todos[2].todo_id}", json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_update_not_existent_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    data = {
        "title": "Exercise Routine",
        "description": "Set a workout routine. Stay consistent.",
        "priority": 5,
        "complete": False,
    }

    response = authorized_user_client.put(url="/todos/7", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authorized_user_update_not_own_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    data = {
        "title": "Exercise Routine",
        "description": "Set a workout routine. Stay consistent.",
        "priority": 5,
        "complete": False,
    }

    response = authorized_user_client.put(
        url=f"/todos{test_todos[0].todo_id}", json=data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authorized_user_update_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    data = {
        "title": "Exercise Routine",
        "description": "Set a workout routine. Stay consistent.",
        "priority": 5,
        "complete": False,
    }

    response = authorized_user_client.put(
        url=f"/todos/{test_todos[2].todo_id}", json=data
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_unauthorized_user_delete_todo(
    client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = client.delete(url=f"/todos/{test_todos[2].todo_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_delete_not_existent_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_user_client.delete(url="/todos/7")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authorized_user_delete_not_own_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_user_client.delete(
        url=f"/todos/{test_todos[0].todo_id}"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authorized_user_delete_todo(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_user_client.delete(
        url=f"/todos/{test_todos[2].todo_id}"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
