from pydantic_settings import BaseSettings
from pydantic import AnyUrl, ValidationError
from loguru import logger

class Settings(BaseSettings):
    db_url: AnyUrl = "postgresql://work:work@10.21.0.55:12345/work"

    # OIDC 服务商配置
    OIDC_NAME : str = ""
    OIDC_CLIENT_ID = ""
    OIDC_CLIENT_SECRET = ""
    # 发现地址
    OIDC_DISCOVERY_URL = ""
    # 回调地址，需要在 OIDC 控制台配置白名单
    REDIRECT_URI = "http://localhost:8000/auth/callback"


try:
    # noinspection PyArgumentList
    SETTING = Settings()
except ValidationError as e:
    logger.error(e)
    exit()
