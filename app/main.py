from fastapi import FastAPI
from app.routers import climate, location
from app.services.check_temperature import check_prolonged_temperature
from app.notifications.notifications import scheduled_task, scheduler
from apscheduler.triggers.cron import CronTrigger
from app.routers.climate import get_current_climate_data, get_climate_data
from app.notifications.notifications_firebase import add_notification_to_firestore
from app.models.location_model import LocationDTO
from app.models.climate_model import ApiResponse
from app.database.firebase import get_db
from fastapi import HTTPException
from google.cloud.firestore import FieldFilter
from datetime import datetime, timedelta

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

location_data = LocationDTO(
    nome="Tomate",
    latitude=-22.50394083489292,
    longitude=-44.109693858772516,
    isOffline=False,
    id="JGC3yS9n12ajQRr5Rpjh"
)

async def teste ():
    return await check_prolonged_temperature(location_data)


@app.get("/teste")
async def executar_teste():
    resultado = await teste()
    return resultado

@app.post("/testee")
async def check_prolonged_temperature(
    location: LocationDTO
) -> None:
    
    db = get_db()
    parametros_ref = db.collection("parametros")
   
    try:
        docs = (
            parametros_ref
            .where(filter=FieldFilter("location_id", "==", location.id))
            .stream()
        )

        parametro = None  # Inicializa a variável parametro

        # Verifica se existe algum documento correspondente
        for doc in docs:
            if doc.exists:
                parametro = doc.to_dict()  # Usa .to_dict() para pegar o conteúdo do documento
                
        # Verifica se encontrou o parâmetro
        if not parametro:
            raise HTTPException(status_code=404, detail="Parâmetro não encontrado para a localização.")

        # Agora você pode acessar o parametro com segurança
        data_criacao = parametro['data_criacao']  # Supondo que 'data_criacao' é um campo de datetime
        
        data_final = data_criacao + timedelta(days=parametro['duracao_max'])
        
        data_inicio_formatada = data_criacao.strftime("%Y%m%d")
        data_final_formatada = data_final.strftime("%Y%m%d")
        data_atual_formatada = datetime.now().strftime("%Y%m%d")

        if data_final_formatada == data_atual_formatada:
            data = await get_climate_data(location.longitude, location.latitude, data_inicio_formatada, data_final_formatada)
            climate = ApiResponse(**data)
        
        return climate
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao procurar localização pelo ID: {e}")
