from work.api import require, auth
from fastapi import FastAPI
from loguru import logger
from pathlib import Path

SELF_SIGN_CA = Path("cert/self.crt")


app = FastAPI(root_path="/api")


for r_base in [require, auth]:
    app.include_router(r_base.router)


if __name__ == "__main__":
    import certifi
    logger.debug(certifi.where())

    from uvicorn import run
    run(app, host="0.0.0.0", port=8000)
