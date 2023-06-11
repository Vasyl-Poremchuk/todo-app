from fastapi import APIRouter
from starlette import status

from src.dependencies import db_dependency, user_dependency
from src.schemas import AddressCreate
from src.services.address_service import AddressService
from src.utils import get_failed_response

router = APIRouter(prefix="/addresses", tags=["address"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_address(
    db: db_dependency,
    user: user_dependency,
    address: AddressCreate,
) -> None:
    address_service = AddressService(db=db)

    if user is None:
        raise get_failed_response(detail="Authentication failed.")

    address_service.create_address(address=address, user_id=user.user_id)
