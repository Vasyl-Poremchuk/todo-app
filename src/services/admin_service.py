from src.dependencies import db_dependency
from src.models import Todo
from src.schemas import TodoResponse
from src.utils import get_todo_not_found


class AdminService:
    def __init__(self, db: db_dependency) -> None:
        self.db = db

    def get_todos_from_users(self) -> list[TodoResponse]:
        """
        The method returns a list of all user `todos`.
        """
        todos = self.db.query(Todo).all()

        return todos

    def delete_todo_from_user(self, todo_id: int) -> None:
        """
        The method deletes the user's `todo`.
        """
        todo = self.db.query(Todo).filter(Todo.todo_id == todo_id).first()

        if todo is None:
            raise get_todo_not_found()

        self.db.query(Todo).filter(Todo.todo_id == todo_id).delete()
        self.db.commit()
