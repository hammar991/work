from sqlmodel import Session, select

from work.schemas.dto import CreateTaskDTO, UpdateTaskStatusDTO
from typing import Iterable
from work.schemas.entity import Task, User


class TaskApplication:
    def __init__(self, db: Session):
        self._s = db

    def create(self, payload: CreateTaskDTO, user: User):
        data = Task(
            title=payload.title,
            content=payload.content,
            link=payload.link,
            owner=user.unique_id,
            create_by=user.unique_id,
        )
        self._s.add(data)

    def list_all(self) -> Iterable[Task]:
        statement = select(Task)
        resp = self._s.exec(statement).all()
        return resp

    def search_by_title(self, title: str) -> Iterable[Task]:
        statement = select(Task).where(Task.title.ilike(f"%{title}%"))
        resp = self._s.exec(statement).all()
        return resp

    def search_by_link(self, link: int) -> Iterable[Task]:
        statement = select(Task).where(Task.link == link)
        resp = self._s.exec(statement).all()
        return resp

    def update_status(self, data:UpdateTaskStatusDTO) -> Task:
        statement = select(Task).where(Task.serial == data.serial)
        task = self._s.exec(statement).one_or_none()
        if task:
            task.current_status = data.status
            self._s.add(task)
        return task