from pydantic_settings import BaseSettings
from pydantic import AnyUrl, ValidationError
from loguru import logger


class Settings(BaseSettings):
    db_url: AnyUrl

    # OIDC 服务商配置
    OIDC_NAME : str = ""
    OIDC_CLIENT_ID = ""
    OIDC_CLIENT_SECRET = ""
    # 发现地址
    OIDC_DISCOVERY_URL = ""
    # 回调地址，需要在 OIDC 控制台配置白名单
    REDIRECT_URI = "http://localhost:8000/auth/callback"
    OIDC_SCOPE = ["openid", "email", "profile"]  # 需要改

    # jwt访问令牌
    SECRET_KEY :str
    ALGORITHM= "HS256"
    
    # token过期时间（分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720

    class Config:
        env_file = "../.env"

try:
    # noinspection PyArgumentList
    SETTING = Settings()
except ValidationError as e:
    logger.error(e)
    exit()
