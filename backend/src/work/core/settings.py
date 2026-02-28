from pydantic_settings import BaseSettings
from pydantic import AnyUrl, ValidationError
from loguru import logger
from pathlib import Path


logger.debug(list(Path().glob("*")))

class Settings(BaseSettings):
    db_url: AnyUrl

    # OIDC 服务商配置
    # noinspection SpellCheckingInspection
    OIDC_NAME : str = "Authentik"
    OIDC_CLIENT_ID: str
    OIDC_CLIENT_SECRET: str
    # 发现地址
    OIDC_DISCOVERY_URL: str
    # 回调地址，需要在 OIDC 控制台配置白名单
    REDIRECT_URI: str
    OIDC_SCOPE: str = '["openid", "email", "profile"]'  # 需要改

    # jwt访问令牌
    SECRET_KEY :str
    ALGORITHM: str = "HS256"
    audience: str
    
    # token过期时间（分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720

    class Config:
        env_file = ".env"

try:
    # noinspection PyArgumentList
    SETTING = Settings()
except ValidationError as e:
    logger.error(e)
    exit()
