from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.src.application.infrastructure.db import Base, engine
from app.src.router import event
from app.src.router import sport

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Permitir solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todas las cabeceras
)

Base.metadata.create_all(bind=engine)

app.include_router(event.router)
app.include_router(sport.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
