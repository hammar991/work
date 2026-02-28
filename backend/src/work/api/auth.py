from fastapi import APIRouter, Request, Depends
from work.application.auth import AuthService, get_current_user
from work.adapter.sql import DBSessionDependency

router = APIRouter(prefix="/auth")

# OIDC 认证路由

@router.get("/login")
async def login_redirect(request: Request, session: DBSessionDependency):
    """ 请求发给认证服务器 """
    auth_service = AuthService(session)
    return await auth_service.login(request)

@router.get("/callback")
async def auth_callback(request: Request, session: DBSessionDependency):
    """ 处理oidc返回结果 """
    auth_service = AuthService(session)
    return await auth_service.callback(request)

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """ 获取当前用户信息 """
    return current_user
