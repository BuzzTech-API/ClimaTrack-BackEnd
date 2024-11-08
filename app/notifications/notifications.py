import asyncio

from datetime import datetime

from app.services.check_temperature import check_extreme_temperature
from app.models.location_model import LocationDTO, LocationsDTO
from app.routers.location import find_all_locations
from app.routers.climate import get_current_climate_data
from app.database.firebase import get_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

async def verify_locations(
    locations: LocationsDTO
) -> None:
    """Pega todas as localizações do firebase e faz as verificações pra cada uma"""
    # Lista que armazena tarefas assíncronas para cada localização
    tasks = []

    # Itera sobre cada localização no firebase e cria uma ou mais tarefas
    for location in locations.locations:
        if not location.isOffline: # Verifica se a localização não está offline
            # Colocar mais verificações por location caso necessário
            task1 = check_extreme_temperature(location)

            tasks.append(task1)

    # Executa todas as tarefas de uma vez
    await asyncio.gather(*tasks)

def add_notification_to_firestore(
    message: str, 
    type: str, 
    id_local: str
) -> None:
    """Adiciona a notificação ao firebase"""
    db = get_db() # Pega a sessão do firebase

    doc_ref = db.collection("notifications").add({
        "timestamp": datetime.now(), # Pega a hora e data atual para mostrar quando a notificação foi criada
        "message": message,
        "type": type,
        "id_local": id_local,
        "is_active": True
    })
    # print("Notificação adicionada ao Firestore:", doc_ref) # para debug


async def scheduled_task() -> None:
    """"Inicia a rotina pegando todas as localizações e chamando a função que as verifica"""
    print(f"Verificações iniciadas às: {datetime.now()}")

    locations = await find_all_locations()
    locationsDTO = LocationsDTO(**locations)
    await verify_locations(locationsDTO)