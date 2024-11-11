import asyncio

from datetime import datetime
from app.services.check_temperature import check_extreme_temperature, check_extreme_precipitation, check_prolonged_temperature, check_prolonged_pluvi
from app.models.location_model import LocationsDTO
from app.routers.location import find_all_locations

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
            task2 = check_extreme_precipitation(location)
            task3 = check_prolonged_temperature(location)
            task4 = check_prolonged_pluvi(location)

            tasks.append(task1)
            tasks.append(task2)
            tasks.append(task3)
            tasks.append(task4)

    # Executa todas as tarefas de uma vez
    await asyncio.gather(*tasks)

async def scheduled_task() -> None:
    """"Inicia a rotina pegando todas as localizações e chamando a função que as verifica"""
    print(f"Verificações iniciadas às: {datetime.now()}")

    locations = await find_all_locations()
    locationsDTO = LocationsDTO(**locations)
    await verify_locations(locationsDTO)