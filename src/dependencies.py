from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.oauth2 import get_current_user


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
