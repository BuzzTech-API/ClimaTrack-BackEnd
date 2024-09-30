from fastapi import FastAPI
from app.routers import climate

app = FastAPI()

# Rota de clima
app.include_router(climate.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}