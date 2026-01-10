from fastapi import FastAPI
from app.api import router
from app.worker import start_worker

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup():
    start_worker()
