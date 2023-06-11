from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.config import settings
from src.models import User
from src.schemas import TokenPayload
from src.utils import verify_password, get_credentials_exception

ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username: str, password: str, db) -> bool:
    """
    The function checks whether the `user` is authenticated.
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    if not verify_password(
        plain_password=password, hashed_password=user.password
    ):
        return False

    return True


def create_access_token(
    username: str,
    user_id: int,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    The function creates an `access token`.
    """
    encode = {"sub": username, "user_id": user_id, "role": role}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    encode.update({"exp": expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    """
    The function returns a `TokenPayload` schema of the user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")

        if username is None or user_id is None:
            raise get_credentials_exception()

        return TokenPayload(username=username, user_id=user_id, role=role)
    except JWTError:
        raise get_credentials_exception()
