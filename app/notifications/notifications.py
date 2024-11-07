import asyncio

from app.routers.location import find_all_locations
from app.routers.climate import get_current_climate_data
from app.database.firebase import get_db
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

async def verify_locations():
    # Lista que armazena tarefas assíncronas para cada localização
    tasks = []

    # Obtem todas as localizações
    locations = await find_all_locations()

    # Itera sobre cada localização no firebase e cria uma ou mais tarefas
    for location in locations["locations"]:
        if not location['isOffline']: # Verifica se a localização não está offline
            # Colocar mais verificações por location caso necessário
            task1 = check_extreme_temperature(location)

            tasks.append(task1)

    # Executa todas as tarefas de uma vez
    await asyncio.gather(*tasks)


async def check_extreme_temperature(location):
    """"Exemplo de função que checa determinado parâmetro"""
    latitude = location['latitude']
    longitude = location['longitude']

    current_data = await get_current_climate_data(latitude, longitude)

    # Temperatura do dia atual
    current_temp = current_data[1]['temperature_max (C°)']

    temperature_threshold = 20  # Define o limite. Pegar das preferencias de local do usuario posteriormente.

    # Verifica se a temperatura excede o limite (ajuste conforme necessário)
    # É possivel colocar mais verificações como temperatura mínima
    if current_temp > temperature_threshold:
        message = f"A temperatura em {location['nome']} ultrapassou o limite estipulado!" # Mnesagem da notificação
        add_notification_to_firestore(message, type="Temperatura Extrema")


def add_notification_to_firestore(message, type):
    db = get_db() # Pega a sessão do firebase

    doc_ref = db.collection("notifications").add({
        "timestamp": datetime.now(), # Pega a hora e data atual para mostrar quando a notificação foi criada
        "message": message,
        "type": type,
        "is_active": True
    })
    # print("Notificação adicionada ao Firestore:", doc_ref) # para debug


async def scheduled_task():
    print(f"Verificações iniciadas às: {datetime.now()}")
    await verify_locations()
