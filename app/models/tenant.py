from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import Base


class Tenant(Base):
    name = Column(String, nullable=False)
    domain = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    users = relationship("User", back_populates="tenant")
    tasks = relationship("Task", back_populates="tenant")
