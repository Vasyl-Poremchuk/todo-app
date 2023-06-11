from src.dependencies import db_dependency, user_dependency
from src.models import Todo, User
from src.schemas import (
    TodoCreate,
    TodoResponse,
    TodoUpdate,
    UserSummaryResponse,
)
from src.utils import (
    get_failed_response,
    get_todo_not_found,
)


class TodoService:
    def __init__(self, db: db_dependency, user: user_dependency) -> None:
        self.db = db
        self.user = user

    def get_todos(self) -> list[TodoResponse]:
        """
        The method returns a list of all `todos` by owner.
        """
        if self.user is None:
            raise get_failed_response(detail="Authentication failed.")

        result = (
            self.db.query(Todo, User)
            .join(User)
            .filter(Todo.owner_id == self.user.user_id)
            .all()
        )

        todos = [
            TodoResponse(
                **todo.__dict__, owner=UserSummaryResponse(**owner.__dict__)
            )
            for todo, owner in result
        ]

        return todos

    def get_todo(self, todo_id: int) -> TodoResponse:
        """
        The method returns the user's `todo`.
        """
        if self.user is None:
            raise get_failed_response(detail="Authentication failed.")

        result = (
            self.db.query(Todo, User)
            .join(User)
            .filter(Todo.todo_id == todo_id)
            .filter(Todo.owner_id == self.user.user_id)
            .first()
        )

        if result is not None:
            todo, owner = result

            return TodoResponse(
                **todo.__dict__, owner=UserSummaryResponse(**owner.__dict__)
            )

        raise get_todo_not_found()

    def create_todo(self, todo: TodoCreate) -> TodoResponse:
        """
        The method creates a new `todo`.
        """
        if self.user is None:
            raise get_failed_response(detail="Authentication failed.")

        created_todo = Todo(**todo.dict(), owner_id=self.user.user_id)

        self.db.add(created_todo)
        self.db.commit()

        return created_todo

    def update_todo(self, todo: TodoUpdate, todo_id: int) -> None:
        """
        The method updates an existing `todo`.
        """
        if self.user is None:
            raise get_failed_response(detail="Authentication failed.")

        todo_to_update = (
            self.db.query(Todo)
            .filter(Todo.todo_id == todo_id)
            .filter(Todo.owner_id == self.user.user_id)
            .first()
        )

        if todo_to_update is None:
            raise get_todo_not_found()

        todo_to_update.title = todo.title
        todo_to_update.description = todo.description
        todo_to_update.priority = todo.priority
        todo_to_update.complete = todo.complete

        self.db.add(todo_to_update)
        self.db.commit()

    def delete_todo(self, todo_id: int) -> None:
        """
        The method deletes an existing `todo`.
        """
        if self.user is None:
            raise get_failed_response(detail="Authentication failed.")

        todo = (
            self.db.query(Todo)
            .filter(Todo.todo_id == todo_id)
            .filter(Todo.owner_id == self.user.user_id)
            .first()
        )

        if todo is None:
            raise get_todo_not_found()

        self.db.query(Todo).filter(Todo.todo_id == todo_id).filter(
            Todo.owner_id == self.user.user_id
        ).delete()
        self.db.commit()
