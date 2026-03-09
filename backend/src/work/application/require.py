from sqlmodel import Session, select

from work.schemas.dto import CreateRequireDTO
from typing import Iterable
from work.schemas.entity import Require, User


class RequireApplication:
    def __init__(self, db: Session):
        self._s = db

    def create(self, payload: CreateRequireDTO, user: User):
        data = Require(
            title=payload.title,
            content=payload.content,
            create_by=user.unique_id,
        )
        self._s.add(data)

    def list_all(self) -> Iterable[Require]:
        statement = select(Require)
        resp = self._s.exec(statement).all()
        return resp

    def search_by_title(self, title: str) -> Iterable[Require]:
        statement = select(Require).where(Require.title.ilike(f"%{title}%"))
        resp = self._s.exec(statement).all()
        return resp

    def search_by_id(self, id: int) -> Iterable[Require]:
        statement = select(Require).where(Require.serial == id)
        resp = self._s.exec(statement).one_or_none()
        return resp
