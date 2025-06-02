from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base
from app.types.enums import TaskStatus, TaskPriority


class Task(Base):
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)

    # Foreign keys
    assignee_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenant.id"), nullable=False)

    # Relationships
    assignee = relationship("User", back_populates="tasks")
    tenant = relationship("Tenant", back_populates="tasks")
