from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from work.schemas.dto import CreateTaskDTO,UpdateTaskStatusDTO
from typing import Iterable
from work.schemas.entity import Task, User
from loguru import logger


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

    def search_by_id(self, search_id: int):
        statement = select(Task).where(Task.serial == search_id)
        resp = self._s.exec(statement).one_or_none()
        return resp

    def search_by_title(self, title: str):
        statement = select(Task).where(Task.title.ilike(f"%{title}%"))
        resp = self._s.exec(statement).all()
        return resp

    def search_by_link(self, link: int) :
        statement = select(Task).where(Task.link == link)
        resp = self._s.exec(statement).all()
        return resp


    def update_state(self, payload:UpdateTaskStatusDTO):
        statement = select(Task).where(Task.serial == payload.serial)
        try:
            resp = self._s.exec(statement).one()
            resp.current_status = payload.status
            self._s.add(resp)
            return {'status': '状态修改成功！'}
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Task not found")
