from typing import Optional
from sqlmodel import Session
from sqlmodel import select

from work.schemas.entity import User


class UserApplication:
    def __init__(self, session: Session):
        self.session = session

    def get_by_oidc_id(self, oidc_id: str) -> Optional[User]:
        statement = select(User).where(User.oidc_id == oidc_id)
        return self.session.exec(statement).first()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, serial: int) -> Optional[User]:
        statement = select(User).where(User.serial == serial)
        return self.session.exec(statement).first()

    def get_by_unique_id(self, unique_id: str) -> Optional[User]:
        statement = select(User).where(User.unique_id == unique_id)
        return self.session.exec(statement).first()
