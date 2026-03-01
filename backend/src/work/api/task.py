from fastapi import APIRouter

from work.adapter.sql import DBSessionDependency
from work.schemas.dto import CreateTaskDTO
from work.application.auth import AuthDependency
from work.application.task import TaskApplication

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/create/", tags=["task"])
async def create_api(data: CreateTaskDTO, session: DBSessionDependency, user: AuthDependency):
    a = TaskApplication(session)
    a.create(data, user)
    return {"status": "ok"}


@router.get("/list/", tags=["task"])
async def list_api(session: DBSessionDependency):
    a = TaskApplication(session)
    return a.list_all()


@router.get("/search/{keyword}/", tags=["task"])
async def search_api(keyword: str, session: DBSessionDependency):
    a = TaskApplication(session)
    return a.search_by_title(keyword)
