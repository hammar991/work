from fastapi import FastAPI
from work.api import require


app = FastAPI()


for r_base in [require]:
    app.include_router(r_base.router)


if __name__ == "__main__":
    from uvicorn import run
    from os import environ
    run(app, host="0.0.0.0", port=8000)
