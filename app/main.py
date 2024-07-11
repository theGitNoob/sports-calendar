from fastapi import FastAPI

from app.src.application.infrastructure.db import Base, engine
from app.src.router import event

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(event.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
