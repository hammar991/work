from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from work.api import require, auth


app = FastAPI(root_path="/api")



for r_base in [require, auth]:
    app.include_router(r_base.router)


if __name__ == "__main__":
    from uvicorn import run
    from os import environ
    run(app, host="0.0.0.0", port=8000)
