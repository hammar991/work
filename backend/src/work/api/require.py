from fastapi import APIRouter

from work.adapter.sql import DBSessionDependency
from work.schemas.dto import CreateRequireDTO
from work.application.auth import AuthDependency
from work.application.require import RequireApplication

router = APIRouter(prefix="/require", tags=["require"])


@router.post("/create/", tags=["require"])
async def create_api(data: CreateRequireDTO, session: DBSessionDependency, user: AuthDependency):
    a = RequireApplication(session)
    a.create(data, user)
    return {"status": "ok"}


@router.get("/list/", tags=["require"])
async def list_api(session: DBSessionDependency):
    a = RequireApplication(session)
    return a.list_all()

@router.get("/search/serial/{serial}/", tags=["require"])
async def search_by_id(serial: int, session: DBSessionDependency):
    a = RequireApplication(session)
    return a.search_by_id(serial)



@router.get("/search/{keyword}/", tags=["require"])
async def search_api(keyword: str, session: DBSessionDependency):
    a = RequireApplication(session)
    return a.search_by_title(keyword)
