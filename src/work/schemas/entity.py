from datetime import datetime
from work.utils import utils
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "user"

    serial: int | None = Field(primary_key=True, unique=True)
    alias: str = ""
    unique_id: str = Field(default_factory=utils.gen_uuid, nullable=False)
    oidc_id: str


class Require(SQLModel, table=True):
    __tablename__ = "require"

    serial: int | None = Field(primary_key=True, unique=True)

    content: str

    create_by: str
    create_time: datetime = Field(default_factory=datetime.now, nullable=False)


class Task(SQLModel, table=True):
    __tablename__ = "task"

    serial: int | None = Field(primary_key=True, unique=True)

    content: str
    create_time: datetime = Field(default_factory=datetime.now, nullable=False)
    start_time: datetime = Field(default_factory=datetime.now, nullable=False)
    end_time: datetime = Field(default_factory=datetime.now, nullable=False)
    current_status: str
