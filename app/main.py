from fastapi import FastAPI
from app.routers import climate, location
from app.notifications.notifications import scheduled_task, scheduler
from apscheduler.triggers.cron import CronTrigger

async def lifespan(app):
    # Inicia o agendamento para rodar todos os dias às 6h
    scheduler.add_job(scheduled_task, CronTrigger(hour=6, minute=0))
    scheduler.start()
    try:
        yield
    finally:
        # Fecha o scheduler ao final do ciclo de vida do app
        scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# Rota de clima
app.include_router(climate.router)
# Rotas relacionadas a localização
app.include_router(location.router)