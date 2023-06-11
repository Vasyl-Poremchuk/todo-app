from fastapi import APIRouter, Path
from starlette import status

from src.dependencies import db_dependency, user_dependency
from src.schemas import TodoResponse
from src.services.admin_service import AdminService
from src.utils import get_invalid_credentials

router = APIRouter(prefix="/admin/todos", tags=["admin"])


@router.get("/", status_code=status.HTTP_200_OK)
async def read_todos(
    user: user_dependency,
    db: db_dependency,
) -> list[TodoResponse]:
    admin_service = AdminService(db=db)

    if user is None or user.role != "admin":
        raise get_invalid_credentials()

    return admin_service.get_todos_from_users()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
) -> None:
    admin_service = AdminService(db=db)

    if user is None or user.role != "admin":
        raise get_invalid_credentials()

    admin_service.delete_todo_from_user(todo_id=todo_id)
