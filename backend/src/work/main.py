from pathlib import Path
import certifi
from loguru import logger


SELF_SIGN_CA = Path("src/cert/self.crt")
logger.debug(list(Path(".").glob("*")))
cert_path = certifi.where()

# 添加自签名的SSL证书
with SELF_SIGN_CA.open(mode="rb") as f:
    certificate = f.read()
    with open(cert_path, 'ab') as cert_file:
        cert_file.write(certificate)


from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from work.core.settings import SETTING
from work.api import require, auth, task, project,query


app = FastAPI(root_path="/api")
app.add_middleware(SessionMiddleware, secret_key=SETTING.secret_key)

for r_base in [require, auth, task, project, query]:
    app.include_router(r_base.router)


if __name__ == "__main__":
    import certifi
    logger.debug(certifi.where())

    from uvicorn import run
    run(app, host="127.0.0.1", port=8000)
