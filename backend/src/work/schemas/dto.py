from pydantic import BaseModel
from work.schemas.enums import TaskStatus


class CreateRequireDTO(BaseModel):
    title: str
    content: str


class CreateProjectDTO(BaseModel):
    title: str
    content: str
    link: int


class CreateTaskDTO(BaseModel):
    title: str
    content: str
    link: int


class UpdateTaskStatusDTO(BaseModel):
    serial: int
    status: TaskStatus