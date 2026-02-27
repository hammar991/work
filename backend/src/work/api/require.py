from typing import List

from fastapi import APIRouter

from work.adapter.sql import DBSessionDependency
from work.schemas.dto import CreateRequireDTO
from work.application.require import RequireApplication

router = APIRouter(prefix="/require", tags=["require"])


@router.post("/create/")
async def require(data: CreateRequireDTO, session: DBSessionDependency):
    a = RequireApplication(session)
    a.create(data)
    return {"status": "ok"}


@router.get("/list/")
async def create(session: DBSessionDependency):
    a = RequireApplication(session)
    return a.list_all()


@router.get("/search/{keyword}/")
async def create(keyword: str, session: DBSessionDependency):
    a = RequireApplication(session)
    return a.search_by_title(keyword)
