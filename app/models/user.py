from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Foreign keys
    tenant_id = Column(Integer, ForeignKey("tenant.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    role = relationship("Role", back_populates="users")
    tasks = relationship("Task", back_populates="assignee")
