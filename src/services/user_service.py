from src.dependencies import db_dependency
from src.models import User
from src.schemas import UserVerification, UserResponse
from src.utils import verify_password, get_hashed_password, get_failed_response


class UserService:
    def __init__(self, db: db_dependency) -> None:
        self.db = db

    def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        The method returns the `user` by id.
        """
        user = self.db.query(User).filter(User.user_id == user_id).first()

        return user

    def change_password(
        self, user_id: int, user_verification: UserVerification
    ) -> None:
        """
        The method changes the `user's` password.
        """
        user = self.get_user_by_id(user_id=user_id)

        if not verify_password(
            plain_password=user_verification.password,
            hashed_password=user.password,
        ):
            raise get_failed_response(detail="Error on password change.")

        user.password = get_hashed_password(
            password=user_verification.new_password
        )

        self.db.add(user)
        self.db.commit()
