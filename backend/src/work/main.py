from pathlib import Path

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from work.core.settings import SETTING
from work.api import require, auth, task, project

SELF_SIGN_CA = Path("cert/self.crt")


app = FastAPI(root_path="/api")
app.add_middleware(SessionMiddleware, secret_key=SETTING.secret_key)

for r_base in [require, auth, task, project]:
    app.include_router(r_base.router)


if __name__ == "__main__":
    import certifi
    logger.debug(certifi.where())

    from uvicorn import run
    run(app, host="0.0.0.0", port=8000)
