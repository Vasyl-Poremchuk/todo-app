from fastapi import APIRouter
from starlette import status

from src.dependencies import db_dependency, user_dependency
from src.schemas import UserResponse, UserVerification
from src.services.user_service import UserService
from src.utils import get_failed_response

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(
    user: user_dependency,
    db: db_dependency,
) -> UserResponse:
    user_service = UserService(db=db)

    if user is None:
        raise get_failed_response(detail="Authentication failed.")

    return user_service.get_user_by_id(user_id=user.user_id)


@router.put("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: UserVerification,
) -> None:
    user_service = UserService(db=db)

    if user is None:
        raise get_failed_response(detail="Authentication failed.")

    user_service.change_password(
        user_id=user.user_id, user_verification=user_verification
    )
