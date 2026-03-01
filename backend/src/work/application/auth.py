from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Annotated, Optional

import jwt
from authlib.integrations.base_client.errors import OAuthError, MismatchingStateError
# noinspection PyUnresolvedReferences
from authlib.integrations.starlette_client import OAuth
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from loguru import logger
from sqlmodel import Session, select

from work.adapter.sql import get_db_session
from work.core.settings import SETTING
from work.schemas.entity import User


class UserAuthApplication:
    def __init__(self, session: Session):
        self.session = session

    def get_by_oidc_id(self, oidc_id: str) -> Optional[User]:
        statement = select(User).where(User.oidc_id == oidc_id)
        return self.session.exec(statement).first()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.refresh(user)
        return user


class AuthService:
    def __init__(self, session: Session):
        self.oauth = OAuth()
        self.user_adapter = UserAuthApplication(session)
        
        # 配置 OIDC 提供商
        self.oauth.register(
            name=SETTING.OIDC_NAME,
            client_id=SETTING.OIDC_CLIENT_ID,
            client_secret=SETTING.OIDC_CLIENT_SECRET,
            server_metadata_url=SETTING.OIDC_DISCOVERY_URL,
            scope=SETTING.OIDC_SCOPE
        )

    def decode_jwt_no_verify(self, token):
        _ = self
        return jwt.decode(token, options={"verify_signature": False}, audience=SETTING.audience, algorithms=["RS256"], key="")

    async def login(self, request: Request, provider_name: str):
        client = self.oauth.create_client(provider_name)
        redirect_url = "http://localhost:5173/login"
        return await client.authorize_redirect(request, redirect_url)

    async def callback(self, request: Request, provider_name: str) -> Dict[str, Any]:
        try:
            client = self.oauth.create_client(provider_name)
            # 获取用户信息
            token = await client.authorize_access_token(request)
            oidc_jwt = token.get('access_token')
            user_info = self.decode_jwt_no_verify(oidc_jwt)

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

            # 内部 token
            expire = datetime.now(timezone.utc) + timedelta(minutes=SETTING.ACCESS_TOKEN_EXPIRE_MINUTES)
            internal_token = jwt.encode(
                {
                    "sub": user.oidc_id,
                    "name": user.alias,
                    "exp": expire
                },
                SETTING.SECRET_KEY,
                algorithm=SETTING.ALGORITHM
            )

            return {
                'access_token': internal_token,
                'token_type': 'Bearer',
                'user': {
                    'serial': user.serial,
                    'unique_id': user.unique_id,
                    'alias': user.alias,
                    'oidc_id': user.oidc_id
                }
            }
        except MismatchingStateError as e:
            logger.error(e)
        except OAuthError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        return {}

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
        payload = jwt.decode(token, SETTING.SECRET_KEY, algorithms=[SETTING.ALGORITHM])
        oidc_id = payload.get('sub')
        # 这里需要根据实际的 OIDC 提供商配置来解码
        user_adapter = UserAuthApplication(session)
        user = user_adapter.get_by_oidc_id(oidc_id=oidc_id)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token 已过期！')
    except JWTError:
        raise HTTPException(status_code=401, detail='无法验证凭证！')


AuthDependency: type[User] = Annotated[User, Depends(get_current_user)]
