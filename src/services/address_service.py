from src.dependencies import db_dependency
from src.models import Address, User
from src.schemas import AddressCreate


class AddressService:
    def __init__(self, db: db_dependency) -> None:
        self.db = db

    def create_address(self, address: AddressCreate, user_id: int) -> None:
        """
        The method creates a new `address` and associates it with the user.
        """
        created_address = Address(**address.dict())

        self.db.add(created_address)
        self.db.flush()

        user = self.db.query(User).filter(User.user_id == user_id).first()
        user.address_id = created_address.address_id

        self.db.add(user)
        self.db.commit()
