# 级联查询
from fastapi import APIRouter
from typing import List
from loguru import logger
from work.application.auth import AuthDependency
from work.adapter.sql import DBSessionDependency
from work.schemas.entity import Require
from work.application.task import TaskApplication
from work.application.require import RequireApplication
from work.application.project import ProjectApplication

router = APIRouter(prefix="/detail", tags=["query"])


@router.get('/{serial}')
async def query_by_series(session: DBSessionDependency, serial:int, type_str: str, user: AuthDependency = AuthDependency):
    logger.debug(f"serial: {serial} ，type_str: {type_str}")
    if type_str == "project":
        p = ProjectApplication(session)
        project = p.search_by_id(serial)
        require_data = project.require
        final_project_lis = require_data.project
        final_task_lis = [i.tasks for i in final_project_lis]
    elif type_str == "require":
        r = RequireApplication(session)
        require = r.search_by_id(serial)
        require_data = require
        final_project_lis = require_data.project
        final_task_lis = [i.tasks for i in final_project_lis]
    elif type_str == "task":
        t = TaskApplication(session)
        task = t.search_by_id(serial)
        require_data = task.project.require
        final_project_lis = require_data.project
        final_task_lis = [i.tasks for i in final_project_lis]
    else:
        final_project_lis = []
        require_data = []
        final_task_lis = []
    logger.debug(f"project_lis: {final_project_lis}\nrequire_data: {require_data}")
    return {"project": final_project_lis, "require": require_data, 'task': final_task_lis}
