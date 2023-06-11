from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    The function hashes the user's `password`.
    """
    return bcrypt_context.hash(secret=password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    The function checks whether the entered password matches an existing one.
    """
    return bcrypt_context.verify(secret=plain_password, hash=hashed_password)


def get_credentials_exception() -> HTTPException:
    """
    The function returns `credentials_exception` response.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_failed_response(detail: str) -> HTTPException:
    """
    The function returns a `unauthorized` response.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )


def get_invalid_credentials() -> HTTPException:
    """
    The function returns an `access denial` response.
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credentials.",
    )


def get_todo_not_found() -> HTTPException:
    """
    The function returns a response if `todo` is not found.
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found.",
    )
