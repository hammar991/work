from pydantic import BaseModel


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
