from fastapi import APIRouter

from work.adapter.sql import DBSessionDependency
from work.schemas.dto import CreateProjectDTO
from work.application.auth import AuthDependency
from work.application.project import ProjectApplication

router = APIRouter(prefix="/project", tags=["project"])


@router.post("/create/", tags=["project"])
async def create_api(data: CreateProjectDTO, session: DBSessionDependency, user: AuthDependency):
    a = ProjectApplication(session)
    a.create(data, user)
    return {"status": "ok"}


@router.get("/list/", tags=["project"])
async def list_api(session: DBSessionDependency):
    a = ProjectApplication(session)
    return a.list_all()


@router.get("/search/{keyword}/", tags=["project"])
async def search_api(keyword: str, session: DBSessionDependency):
    a = ProjectApplication(session)
    return a.search_by_title(keyword)
