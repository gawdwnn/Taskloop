from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints

from .base import BaseSchema


class RoleBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    description: Optional[str] = None
    is_active: bool = True


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[Annotated[str, StringConstraints(min_length=1, max_length=50)]] = (
        None
    )
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleInDB(RoleBase, BaseSchema):
    pass


class Role(RoleInDB):
    pass
