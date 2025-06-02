from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints

from app.types.enums import TaskPriority, TaskStatus

from .base import BaseSchema


class TaskBase(BaseModel):
    title: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: int
    tenant_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=1, max_length=200)]] = (
        None
    )
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[int] = None


class TaskInDB(TaskBase, BaseSchema):
    pass


class Task(TaskInDB):
    pass
