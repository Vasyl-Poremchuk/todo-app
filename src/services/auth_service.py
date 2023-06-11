from src.dependencies import db_dependency
from src.models import User
from src.schemas import UserCreate, UserResponse
from src.utils import get_hashed_password


class AuthService:
    def __init__(self, db: db_dependency) -> None:
        self.db = db

    def get_user_by_username(self, username: str) -> User:
        """
        The method returns the `user` by username.
        """
        user = self.db.query(User).filter(User.username == username).first()

        return user

    def create_user(self, user: UserCreate) -> UserResponse:
        """
        The method creates a new `user`.
        """
        hashed_password = get_hashed_password(password=user.password)
        user.password = hashed_password

        created_user = User(
            is_active=True,
            **user.dict(),
        )

        self.db.add(created_user)
        self.db.commit()

        return created_user
