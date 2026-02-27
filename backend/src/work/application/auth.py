from typing import Optional, Dict, Any
from authlib.integrations.starlette_client import OAuth
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from jose import JWTError

from work.adapter.user import UserAdapter
from work.schemas.entity import User
from work.core.settings import SETTING
from work.adapter.sql import get_db_session


class AuthService:
    def __init__(self, session: Session):
        self.oauth = OAuth()
        self.user_adapter = UserAdapter(session)
        
        # 配置 OIDC 提供商
        self.oauth.register(
            name=SETTING.OIDC_NAME,
            server_metadata_url=SETTING.OIDC_DISCOVERY_URL,
            client_id=SETTING.OIDC_CLIENT_ID,
            client_secret=SETTING.OIDC_CLIENT_SECRET,
            redirect_uri=SETTING.REDIRECT_URI,
            scope='openid profile email'
        )

    async def login(self, request: Request):
        return await self.oauth.oidc.authorize_redirect(request, SETTING.REDIRECT_URI)

    async def callback(self, request: Request) -> Dict[str, Any]:

        # 获取用户信息
        token = await self.oauth.oidc.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(status_code=401, detail='获取用户信息！')

        # 获取唯一身份标识
        oidc_id = user_info.get('sub')
        if not oidc_id:
            raise HTTPException(status_code=401, detail='OIDC获取身份标识失败！')
        
        # 查找或创建用户
        user = self.user_adapter.get_by_oidc_id(oidc_id)

        if not user:
            user = User(
                oidc_id=oidc_id,
                alias=user_info.get('name', '')
            )
            user = self.user_adapter.create(user)
        
        return {
            'access_token': token.get('access_token'),
            'token_type': 'Bearer',
            'user': {
                'serial': user.serial,
                'unique_id': user.unique_id,
                'alias': user.alias,
                'oidc_id': user.oidc_id
            }
        }

    def get_user_by_oidc_id(self, oidc_id: str) -> Optional[User]:
        return self.user_adapter.get_by_oidc_id(oidc_id)


# 依赖项
def get_auth_service(session: Session):
    return AuthService(session)

# 安全方案
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_db_session)):
    token = credentials.credentials     # 提取jwt
    try:
        # 解码 token 获取用户信息
        # 这里需要根据实际的 OIDC 提供商配置来解码
        # 使用 JWKS 或公钥验证 token
        auth_service = AuthService(session)
        # 这里简化处理，实际应该验证 token 并获取用户信息
        return {"token": token}
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid authentication credentials')



