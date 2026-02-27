from pydantic import BaseModel


class CreateRequireDTO(BaseModel):
    title: str
    content: str
