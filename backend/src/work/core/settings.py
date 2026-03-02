from pathlib import Path

from loguru import logger
from pydantic import AnyUrl, ValidationError
from pydantic_settings import BaseSettings

logger.debug(list(Path().glob("*")))

class Settings(BaseSettings):
    db_url: AnyUrl

    # OIDC 服务商配置
    # noinspection SpellCheckingInspection
    oidc_name: str = "Authentik"
    oidc_client_id: str
    oidc_client_secret: str
    # 发现地址
    oidc_discovery_url: str
    # 回调地址，需要在 OIDC 控制台配置白名单
    redirect_uri: str
    oidc_scope: str = '["openid", "email", "profile"]'  # 需要改
    secret_key: str
    # jwt访问令牌
    secret_key:str
    algorithm: str = "HS256"
    audience: str
    
    # token过期时间（分钟）
    access_token_expire_minutes: int = 720

    class Config:
        env_file = ".env"

try:
    # noinspection PyArgumentList
    SETTING = Settings()
except ValidationError as e:
    logger.error(e)
    exit()
