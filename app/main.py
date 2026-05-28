from fastapi import FastAPI
from app.routes import router
from app.database import engine
from app.models import Base

# Inicializar app
app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)