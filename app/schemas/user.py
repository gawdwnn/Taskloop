from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, StringConstraints

from .base import BaseSchema


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    tenant_id: int
    role_id: int


class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(min_length=8)]


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[Annotated[str, StringConstraints(min_length=8)]] = None
    role_id: Optional[int] = None


class UserInDB(UserBase, BaseSchema):
    pass


class User(UserInDB):
    pass
