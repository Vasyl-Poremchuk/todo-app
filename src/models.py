from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, types
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Role(str, Enum):
    admin = "admin"
    user = "user"


class Priority(int, Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=50), unique=True, index=True, nullable=False)
    username = Column(String(length=30), unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(types.Enum(Role), nullable=False)
    first_name = Column(String(length=30), nullable=True)
    last_name = Column(String(length=30), nullable=True)
    phone_number = Column(String(length=15), nullable=True)
    address_id = Column(
        Integer,
        ForeignKey("address.address_id", ondelete="CASCADE"),
        nullable=True,
    )

    todos = relationship("Todo", back_populates="owner")
    address = relationship("Address", back_populates="user_address")

    def __repr__(self) -> str:
        """
        The method returns a string representation of the `User` instance class model.
        """
        return f"User(user_id={self.user_id!r}, username={self.username!r})"


class Todo(Base):
    __tablename__ = "todo"

    todo_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=30), index=True, nullable=False)
    description = Column(String(length=200), nullable=False)
    priority = Column(types.Enum(Priority), nullable=False)
    complete = Column(Boolean, default=False)
    owner_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User", back_populates="todos")

    def __repr__(self) -> str:
        """
        The method returns a string representation of the `Todo` instance class model.
        """
        return f"Todo(todo_id={self.todo_id}, title={self.title})"


class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, index=True)
    city = Column(String(length=30), nullable=False)
    state = Column(String(length=30), nullable=False)
    country = Column(String(length=30), nullable=False)
    postal_code = Column(String(length=5), nullable=True)

    user_address = relationship("User", back_populates="address")

    def __repr__(self) -> str:
        """
        The method returns a string representation of the `Address` instance class model.
        """
        return (
            f"Address(address_id={self.address_id!r}, "
            f"city={self.city!r}, "
            f"state={self.state!r}, "
            f"country={self.country!r})"
        )
