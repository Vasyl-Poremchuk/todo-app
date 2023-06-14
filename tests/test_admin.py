from typing import Type

from fastapi.testclient import TestClient
from starlette import status

from src.models import Todo
from src.schemas import TodoResponse


def test_unauthorized_user_read_todos_from_users(
    client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = client.get(url="/admin/todos/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_read_todos_from_users(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_user_client.get(url="/admin/todos/")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_authorized_admin_read_todos_from_users(
    authorized_admin_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_admin_client.get("/admin/todos/")

    todos = [TodoResponse(**todo) for todo in response.json()]

    assert len(todos) == len(test_todos)
    assert response.status_code == status.HTTP_200_OK


def test_unauthorized_user_delete_todos_from_users(
    client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = client.delete(url=f"/admin/todos/{test_todos[2].todo_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_user_delete_todos_from_users(
    authorized_user_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_user_client.delete(
        url=f"/admin/todos/{test_todos[2].todo_id}"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_authorized_admin_delete_todos_from_users(
    authorized_admin_client: TestClient, test_todos: list[Type[Todo]]
) -> None:
    response = authorized_admin_client.delete(
        url=f"/admin/todos/{test_todos[2].todo_id}"
    )
    response_after_deletion = authorized_admin_client.get(url="/admin/todos")

    assert len(response_after_deletion.json()) == 2
    assert response.status_code == status.HTTP_204_NO_CONTENT
