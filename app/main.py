from fastapi import FastAPI
from app.routers import climate, location
app = FastAPI()

# Rota de clima
app.include_router(climate.router)
# Rotas relacionadas a localização
app.include_router(location.router)