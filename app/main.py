from fastapi import FastAPI
from app.routes import router

# Inicializar app
app = FastAPI()
app.include_router(router)