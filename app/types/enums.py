from enum import Enum


class TaskStatus(str, Enum):
    """Represents the status of a task."""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, Enum):
    """Represents the priority level of a task."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
