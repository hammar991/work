from sqlmodel import Session, select, col

from work.schemas.dto import CreateProjectDTO
from typing import Iterable
from work.schemas.entity import Project, User


class ProjectApplication:
    def __init__(self, db: Session):
        self._s = db

    def create(self, payload: CreateProjectDTO, user: User):
        data = Project(
            title=payload.title,
            content=payload.content,
            link=payload.link,
            create_by=user.unique_id,
        )
        self._s.add(data)

    def list_all(self) -> Iterable[Project]:
        statement = select(Project)
        resp = self._s.exec(statement).all()
        return resp

    def search_by_title(self, title: str) -> Iterable[Project]:
        statement = select(Project).where(col(Project.title).ilike(f"%{title}%"))
        resp = self._s.exec(statement).all()
        return resp

    def search_by_id(self, search_id: int) :
        statement = select(Project).where(Project.serial == search_id)
        resp = self._s.exec(statement).one_or_none()
        return resp

    def search_by_link(self, link: int) :
        statement = select(Project).where(Project.link == link)
        resp = self._s.exec(statement).one_or_none()
        return resp
