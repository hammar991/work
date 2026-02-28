from fastapi import APIRouter, Request, Depends
from loguru import logger

from work.application.auth import AuthService, get_current_user
from work.adapter.sql import DBSessionDependency
from authlib.integrations.base_client.errors import MismatchingStateError

router = APIRouter(prefix="/auth")

# OIDC 认证路由

@router.get("/login/{provider_name}")
async def login_redirect(request: Request, session: DBSessionDependency, provider_name: str):
    """ 请求发给认证服务器 """
    auth_service = AuthService(session)

    return await auth_service.login(request, provider_name)

@router.get("/callback/{provider_name}")
async def auth_callback(request: Request, session: DBSessionDependency, provider_name: str):
    """ 处理oidc返回结果 """
    try:
        auth_service = AuthService(session)
        return await auth_service.callback(request, provider_name)
    except MismatchingStateError as e:
        logger.error(e)
        return {}


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """ 获取当前用户信息 """
    return current_user
