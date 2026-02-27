from pydantic_settings import BaseSettings
from pydantic import AnyUrl, ValidationError
from loguru import logger

class Settings(BaseSettings):
    db_url: AnyUrl = "postgresql://work:work@10.21.0.55:12345/work"


try:
    # noinspection PyArgumentList
    SETTING = Settings()
except ValidationError as e:
    logger.error(e)
    exit()
