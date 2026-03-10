from datetime import datetime
from typing import List
from sqlalchemy import VARCHAR

from work.schemas.enums import TaskStatus
from work.utils import utils
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    __tablename__ = "user"

    serial: int | None = Field(primary_key=True, unique=True)
    alias: str = ""
    unique_id: str = Field(default_factory=utils.gen_nuid, nullable=False)
    oidc_id: str


class Require(SQLModel, table=True):
    __tablename__ = "require"

    serial: int | None = Field(primary_key=True, unique=True)

    title: str
    content: str

    create_by: str
    create_time: datetime = Field(default_factory=datetime.now, nullable=False)

    project: List["Project"] = Relationship(back_populates="require")


class Project(SQLModel, table=True):
    __tablename__ = "project"

    serial: int | None = Field(primary_key=True, unique=True)
    link: int = Field(foreign_key="require.serial", nullable=False)

    title: str
    content: str

    create_by: str
    create_time: datetime = Field(default_factory=datetime.now, nullable=False)

    require: Require = Relationship(back_populates="project")
    tasks: List["Task"] = Relationship(back_populates="project")


class Task(SQLModel, table=True):
    __tablename__ = "task"

    serial: int | None = Field(primary_key=True, unique=True)
    link: int = Field(foreign_key="project.serial", nullable=False)

    owner: str

    title: str
    content: str
    create_by: str
    create_time: datetime = Field(default_factory=datetime.now, nullable=False)
    start_time: datetime = Field(default_factory=datetime.now, nullable=False)
    end_time: datetime = Field(default_factory=datetime.now, nullable=False)
    current_status: TaskStatus = Field(default=TaskStatus.PLANNED, sa_type=VARCHAR)

    project: Project = Relationship(back_populates="tasks")


def init_db(engine):
    SQLModel.metadata.create_all(engine)
