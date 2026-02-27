from typing import Annotated

from fastapi import Depends
from loguru import logger
from sqlmodel import create_engine
from sqlmodel import Session
from work.core.settings import SETTING
from work.schemas.entity import init_db

engine = create_engine(
    f"{SETTING.db_url}",
    echo=False,
    pool_size=256,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
)

init_db(engine)

def get_db_session():
    with Session(engine) as session:
        try:
            logger.trace(f"db session start")
            yield session

            logger.trace(f"db session end")
            session.commit()
            logger.trace(f"db session commit")
        except Exception as e:
            logger.error(e)
            session.rollback()
            raise
        finally:
            logger.trace(f"db session close")
            session.close()


DBSessionDependency: type[Session] = Annotated[Session, Depends(get_db_session)]
