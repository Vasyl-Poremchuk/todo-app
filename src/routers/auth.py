from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.dependencies import db_dependency
from src.oauth2 import ACCESS_TOKEN_EXPIRE, create_access_token
from src.schemas import Token, UserCreate, UserResponse
from src.services.auth_service import AuthService
from src.utils import get_invalid_credentials, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: UserCreate) -> UserResponse:
    auth_service = AuthService(db=db)

    created_user = auth_service.create_user(user=user)

    return created_user


@router.post(
    "/token", response_model=Token, status_code=status.HTTP_201_CREATED
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
) -> Token:
    auth_service = AuthService(db=db)

    user = auth_service.get_user_by_username(form_data.username)

    if not user:
        raise get_invalid_credentials()

    if not verify_password(
        plain_password=form_data.password, hashed_password=user.password
    ):
        raise get_invalid_credentials()

    token = create_access_token(
        username=user.username,
        user_id=user.user_id,
        role=user.role,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE),
    )

    return Token(access_token=token, token_type="bearer")
