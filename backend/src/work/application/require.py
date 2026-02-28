from sqlmodel import Session, select

from work.schemas.dto import CreateRequireDTO
from typing import Iterable
from work.schemas.entity import Require, User


class RequireApplication:
    def __init__(self, db: Session):
        self._s = db

    def create(self, payload: CreateRequireDTO, user: User) -> Require:
        data = Require.model_validate(payload.model_dump())
        self._s.add(data)

    def list_all(self) -> Iterable[Require]:
        statement = select(Require)
        resp = self._s.exec(statement).all()
        return resp

    def search_by_title(self, title: str) -> Iterable[Require]:
        statement = select(Require).where(Require.name.ilike(f"%{title}%"))
        resp = self._s.exec(statement).all()
        return resp
