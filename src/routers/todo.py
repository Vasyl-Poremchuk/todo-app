from fastapi import APIRouter, Path
from starlette import status

from src.dependencies import db_dependency, user_dependency
from src.schemas import (
    TodoCreate,
    TodoResponse,
    TodoUpdate,
)
from src.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todo"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[TodoResponse]
)
async def read_todos(
    user: user_dependency,
    db: db_dependency,
) -> list[TodoResponse]:
    todo_service = TodoService(db=db, user=user)

    todos = todo_service.get_todos()

    return todos


@router.get(
    "/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse
)
async def read_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
) -> TodoResponse:
    todo_service = TodoService(db=db, user=user)

    todo = todo_service.get_todo(todo_id=todo_id)

    return todo


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    db: db_dependency,
    todo: TodoCreate,
) -> TodoResponse:
    todo_service = TodoService(db=db, user=user)

    created_todo = todo_service.create_todo(todo=todo)

    return created_todo


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo: TodoUpdate,
    todo_id: int = Path(gt=0),
) -> None:
    todo_service = TodoService(db=db, user=user)

    todo_service.update_todo(todo=todo, todo_id=todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
) -> None:
    todo_service = TodoService(db=db, user=user)

    todo_service.delete_todo(todo_id=todo_id)
