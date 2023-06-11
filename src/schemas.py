import re
from string import punctuation

from pydantic import BaseModel, EmailStr, validator


from src.models import Priority
from src.exceptions import (
    CityFormatException,
    CountryFormatException,
    DescriptionFormatException,
    FirstNameFormatException,
    LastNameFormatException,
    PasswordFormatException,
    PhoneNumberFormatException,
    PostalCodeFormatException,
    StateFormatException,
    TitleFormatException,
    UsernameFormatException,
)

PHONE_NUMBER_REGEX = re.compile(
    r"^(?:\+38|0)?\(?0?\d{2}\)?\s?\d{3}-?\d{2}-?\d{2}$"
)
PUNCTUATION_WITHOUT_UNDERSCORE = punctuation.replace("_", "")


class UserBase(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None

    @validator("username")
    def validate_username(cls, value) -> str:
        """
        The method checks if the `username` passes all validations.
        """
        if not (5 <= len(value) <= 30):
            raise UsernameFormatException(
                detail="The length of the `username` must be between 5 and 30 characters.",
            )

        if any(character.isupper() for character in value):
            raise UsernameFormatException(
                detail="The `username` must not contain uppercase characters.",
            )

        if any(character.isspace() for character in value):
            raise UsernameFormatException(
                detail="The `username` must not contain whitespaces.",
            )

        if any(
            character in PUNCTUATION_WITHOUT_UNDERSCORE for character in value
        ):
            raise UsernameFormatException(
                detail="The `username` must not contain any punctuation marks "
                "other than underscores.",
            )

        return value

    @validator("password")
    def validate_password(cls, value) -> str:
        """
        The method checks if the `password` passes all validations.
        """
        if len(value) < 8:
            raise PasswordFormatException(
                detail="The `password` must be at least 8 characters long.",
            )

        if not any(character.isupper() for character in value):
            raise PasswordFormatException(
                detail="The `password` must contain at least one uppercase letter.",
            )

        if not any(character.islower() for character in value):
            raise PasswordFormatException(
                detail="The `password` must contain at least one lowercase letter.",
            )

        if not any(character.isdigit() for character in value):
            raise PasswordFormatException(
                detail="The `password` must contain at least one digit.",
            )

        if not any(character in punctuation for character in value):
            raise PasswordFormatException(
                detail="The `password` must contain at least one punctuation mark "
                "such as !#$%&'\"()*+,-/:;<=>?@[\\]^_`{|}~.",
            )

        if any(character.isspace() for character in value):
            raise PasswordFormatException(
                detail="The `password` must not contain whitespaces.",
            )

        return value

    @validator("first_name")
    def validate_first_name(cls, value) -> str:
        """
        The method checks if the `first_name` passes all validations.
        """
        if any(character.isspace() for character in value):
            raise FirstNameFormatException(
                detail="The `first_name` must not contain whitespaces.",
            )

        if any(character.isdigit() for character in value):
            raise FirstNameFormatException(
                detail="The `first_name` must not contain digits.",
            )

        if any(character in punctuation for character in value):
            raise FirstNameFormatException(
                detail="The `first_name` must not contain punctuation marks.",
            )

        if not value.istitle():
            raise FirstNameFormatException(
                detail="The `first_name` must start with a capital letter.",
            )

        return value

    @validator("last_name")
    def validate_last_name(cls, value) -> str:
        """
        The method checks if the `last_name` passes all validations.
        """
        if any(character.isspace() for character in value):
            raise LastNameFormatException(
                detail="The `last_name` must not contain whitespaces.",
            )

        if any(character.isdigit() for character in value):
            raise LastNameFormatException(
                detail="The `last_name` must not contain digits.",
            )

        if any(character in punctuation for character in value):
            raise LastNameFormatException(
                detail="The `last_name` must not contain punctuation marks.",
            )

        if not value.istitle():
            raise LastNameFormatException(
                detail="The `last_name` must start with a capital letter.",
            )

        return value

    @validator("phone_number")
    def validate_phone_number(cls, value) -> str:
        """
        The method checks if the `phone_number` passes all validations.
        """
        if value:
            if not PHONE_NUMBER_REGEX.match(value):
                raise PhoneNumberFormatException(
                    detail="The `phone_number` is in the wrong format.",
                )

        return value


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    is_active: bool


class UserResponse(UserBase):
    user_id: int
    is_active: bool
    todos: list["TodoResponse"] = []
    address: "AddressResponse" = None

    class Config:
        orm_mode = True


class UserSummaryResponse(BaseModel):
    user_id: int
    email: EmailStr
    username: str

    class Config:
        orm_mode = True


class UserVerification(BaseModel):
    password: str
    new_password: str


class TokenPayload(BaseModel):
    username: str | None = None
    user_id: int | None = None
    role: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoBase(BaseModel):
    title: str
    description: str
    priority: Priority
    complete: bool = False

    @validator("title")
    def validate_title(cls, value) -> str:
        """
        The method checks if the `title` passes all validations.
        """
        if all(
            character.isdigit()
            or character.isspace()
            or character in punctuation
            for character in value
        ):
            raise TitleFormatException(
                detail="The `title` must contain letters.",
            )

        return value

    @validator("description")
    def validate_description(cls, value) -> str:
        """
        The method checks if the `description` passes all validations.
        """
        if all(
            character.isdigit()
            or character.isspace()
            or character in punctuation
            for character in value
        ):
            raise DescriptionFormatException(
                detail="The `description` must contain letters.",
            )
        return value


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class TodoResponse(TodoBase):
    todo_id: int
    owner: "UserSummaryResponse"

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    city: str
    state: str
    country: str
    postal_code: str | None = None

    @validator("city")
    def validate_city(cls, value) -> str:
        """
        The method checks if the `city` passes all validations.
        """
        if any(character in punctuation for character in value):
            raise CityFormatException(
                detail="The `city` must not contain punctuation marks.",
            )

        if any(character.isdigit() for character in value):
            raise CityFormatException(
                detail="The `city` must not contain digits.",
            )

        if not value.istitle():
            raise CityFormatException(
                detail="The `city` must start with a capital letter.",
            )

        return value

    @validator("state")
    def validate_state(cls, value) -> str:
        """
        The method checks if the `state` passes all validations.
        """
        if any(character in punctuation for character in value):
            raise StateFormatException(
                detail="The `state` must not contain punctuation marks.",
            )

        if any(character.isdigit() for character in value):
            raise StateFormatException(
                detail="The `state` must not contain digits.",
            )

        if not value.istitle():
            raise StateFormatException(
                detail="The `state` must start with a capital letter.",
            )

        return value

    @validator("country")
    def validate_country(cls, value) -> str:
        """
        The method checks if the `country` passes all validations.
        """
        if any(character in punctuation for character in value):
            raise CountryFormatException(
                detail="The `country` must not contain punctuation marks.",
            )

        if any(character.isdigit() for character in value):
            raise CountryFormatException(
                detail="The `country` must not contain digits.",
            )

        if not (value.istitle() or value.isupper()):
            raise CountryFormatException(
                detail="The `country` must start with a capital letter (except USA, UK, etc.).",
            )

        return value

    @validator("postal_code")
    def validate_postal_code(cls, value) -> str:
        """
        The method checks if the `postal_code` passes all validations.
        """
        if len(value) != 5:
            raise PostalCodeFormatException(
                detail="The length of the `postal_code` must be 5.",
            )

        if not all(digit for digit in value if digit.isdigit()):
            raise PostalCodeFormatException(
                detail="The `postal_code` must contain only digits."
            )

        return value


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressResponse(AddressBase):
    address_id: int

    class Config:
        orm_mode = True


UserResponse.update_forward_refs()
TodoResponse.update_forward_refs()
AddressResponse.update_forward_refs()
