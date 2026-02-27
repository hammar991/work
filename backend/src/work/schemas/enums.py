from enum import Enum


class TaskStatus(str, Enum):
    PLANNED = "planned"
    PROGRESS = "progress"
    COMPLETED = "completed"
    HALTED = "halted"
