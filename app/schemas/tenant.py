from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints

from .base import BaseSchema


class TenantBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    domain: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    is_active: bool = True


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: Optional[Annotated[str, StringConstraints(min_length=1, max_length=100)]] = (
        None
    )
    domain: Optional[
        Annotated[str, StringConstraints(min_length=1, max_length=100)]
    ] = None
    is_active: Optional[bool] = None


class TenantInDB(TenantBase, BaseSchema):
    pass


class Tenant(TenantInDB):
    pass
