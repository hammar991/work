from work.schemas.entity import User
from sqlmodel import select
from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

TokenDependency = Annotated[str, Depends(oauth2_scheme)]


class MockUser:
    def __init__(self, session):
        self._s = session

    def get_user(self, token: str) -> User:
        _ = token
        statement = select(User).where(User.id == 1)
        return self._s.exec(statement).one()
