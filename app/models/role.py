from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import Base


class Role(Base):
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)

    # Relationships
    users = relationship("User", back_populates="role")
