from authlib.integrations.base_client.errors import MismatchingStateError
from fastapi import APIRouter, Request
from loguru import logger

from work.adapter.sql import DBSessionDependency
from work.application.auth import AuthService, AuthDependency

router = APIRouter(prefix="/auth")


# OIDC 认证路由
@router.get("/login/{provider_name}", tags=["oidc"])
async def login_redirect(request: Request, session: DBSessionDependency, provider_name: str):
    """ 请求发给认证服务器 """
    auth_service = AuthService(session)
    return await auth_service.login(request, provider_name)


@router.get("/callback/{provider_name}", tags=["oidc"])
async def auth_callback(request: Request, session: DBSessionDependency, provider_name: str):
    """ 处理oidc返回结果 """
    try:
        auth_service = AuthService(session)
        return await auth_service.callback(request, provider_name)
    except MismatchingStateError as e:
        logger.error(e)
        return {}


@router.get("/me", tags=["oidc"])
async def get_current_user_info(current_user: AuthDependency):
    """ 获取当前用户信息 """
    return current_user
