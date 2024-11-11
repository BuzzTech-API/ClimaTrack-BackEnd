from datetime import datetime, timedelta

from fastapi import HTTPException
from google.cloud.firestore import FieldFilter

from app.database.firebase import get_db
from app.models.climate_model import ApiResponse
from app.models.location_model import LocationDTO
from app.notifications.notifications_firebase import add_notification_to_firestore
from app.routers.climate import get_climate_data, get_current_climate_data


async def check_extreme_temperature(location: LocationDTO) -> None:
    """ "Exemplo de função que checa determinado parâmetro"""
    type = "Temperatura Extrema"  # Tipo da notificação
    db = get_db()
    parametros_ref = db.collection("parametros")
    parametro = None

    try:
        docs = parametros_ref.where(
            filter=FieldFilter("location_id", "==", location.id)
        ).stream()

        for doc in docs:
            if doc.exists:
                parametro = doc.to_dict()

        if not parametro:
            raise HTTPException(
                status_code=404, detail="Parâmetro não encontrado para a localização."
            )

        current_data = await get_current_climate_data(
            location.latitude, location.longitude
        )

        # Temperatura do dia atual
        current_temp = current_data[1]
        print(current_temp)

        temperature_max_threshold = 20  # Define o limite maximo da temperatura. Pegar das preferencias de local do usuario posteriormente.
        temperature_min_threshold = 30  # Define o limite minimo da temperatura. Pegar das preferencias de local do usuario posteriormente.

        # Verifica se a temperatura excede o limite (ajuste conforme necessário)
        if current_temp["temperature_max (C°)"] > temperature_max_threshold:
            message = f"A temperatura em {location.nome} está a cima do limite estipulado!"  # Menagem da notificação
            await add_notification_to_firestore(message, type, location.id)
        if current_temp["temperature_min (C°)"] < temperature_min_threshold:
            message = f"A temperatura em {location.nome} está a baixo do limite estipulado!"  # Menagem da notificação
            await add_notification_to_firestore(message, type, location.id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao procurar verificar temperatura prolongada: {e}",
        )


async def check_extreme_precipitation(location: LocationDTO) -> None:
    """ "Exemplo de função que checa determinado parâmetro"""
    type = "Precipitacao Extrema"  # Tipo da notificação
    db = get_db()
    parametros_ref = db.collection("parametros")
    parametro = None
    try:
        docs = parametros_ref.where(
            filter=FieldFilter("location_id", "==", location.id)
        ).stream()

        for doc in docs:
            if doc.exists:
                parametro = doc.to_dict()

        if not parametro:
            raise HTTPException(
                status_code=404, detail="Parâmetro não encontrado para a localização."
            )

        current_data = await get_current_climate_data(
            location.latitude, location.longitude
        )

        # Precipitacao do dia atual
        current_prec = current_data[1]

        precipitation_max_threshold = 0  # Define o limite maximo da humidade. Pegar das preferencias de local do usuario posteriormente.
        precipitation_min_threshold = 1  # Define o limite minimo da humidade. Pegar das preferencias de local do usuario posteriormente.

        # Verifica se a precipitação excede o limite (ajuste conforme necessário)
        if current_prec["precipitation (mm)"] > precipitation_max_threshold:
            message = f"A precipitação em {location.nome} está a cima do limite estipulado!"  # Menagem da notificação
            await add_notification_to_firestore(message, type, location.id)
        if current_prec["precipitation (mm)"] < precipitation_min_threshold:
            message = f"A precipitação em {location.nome} está a baixo do limite estipulado!"  # Menagem da notificação
            await add_notification_to_firestore(message, type, location.id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao procurar verificar temperatura : {e}",
        )


async def check_prolonged_temperature(location: LocationDTO) -> None:
    type = "Temperatura Média Alta Prolongada"
    db = get_db()
    parametros_ref = db.collection("parametros")
    parametro = None

    try:
        docs = parametros_ref.where(
            filter=FieldFilter("location_id", "==", location.id)
        ).stream()

        for doc in docs:
            if doc.exists:
                parametro = doc.to_dict()

        if not parametro:
            raise HTTPException(
                status_code=404, detail="Parâmetro não encontrado para a localização."
            )

        data_inicial = datetime.now() - timedelta(days=parametro["duracao_max"])

        data_inicio_formatada = data_inicial.strftime("%Y%m%d")
        data_final_formatada = datetime.now().strftime("%Y%m%d")

        data = await get_climate_data(
            location.longitude,
            location.latitude,
            int(data_inicio_formatada),
            int(data_final_formatada),
        )
        climate = ApiResponse(**data)

        total_temperature = sum(item.temperature for item in climate.data)
        num_days = len(climate.data)

        average_temperature = total_temperature / num_days

        if average_temperature > parametro.max_temp:
            message = f"A temperatura média máxima de {parametro.max_temp}°C em {location.nome} ultrapassou o limite estipulado de {num_days} dias!"
            await add_notification_to_firestore(message, type, location.id)

        if average_temperature <= parametro.min_temp:
            message = f"A temperatura média mínima de {parametro.min_temp}°C em {location.nome} ultrapassou o limite estipulado de {num_days} dias!"
            await add_notification_to_firestore(message, type, location.id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao procurar verificar temperatura prolongada: {e}",
        )


async def check_prolonged_pluvi(location: LocationDTO) -> None:
    type = "Precipitação Média Alta Prolongada"
    db = get_db()
    parametros_ref = db.collection("parametros")
    parametro = None

    try:
        docs = parametros_ref.where(
            filter=FieldFilter("location_id", "==", location.id)
        ).stream()

        for doc in docs:
            if doc.exists:
                parametro = doc.to_dict()

        if not parametro:
            raise HTTPException(
                status_code=404, detail="Parâmetro não encontrado para a localização."
            )

        data_inicial = datetime.now() - timedelta(days=parametro["duracao_max"])

        data_inicio_formatada = data_inicial.strftime("%Y%m%d")
        data_final_formatada = datetime.now().strftime("%Y%m%d")

        data = await get_climate_data(
            location.longitude,
            location.latitude,
            int(data_inicio_formatada),
            int(data_final_formatada),
        )
        climate = ApiResponse(**data)

        total_precipitation = sum(item.precipitation for item in climate.data)
        num_days = len(climate.data)

        average_precipitation = total_precipitation / num_days

        if average_precipitation > parametro.max_pluvi:
            message = f"A precipitação média máxima de {parametro.max_pluvi}°C em {location.nome} ultrapassou o limite estipulado de{num_days} dias!"
            await add_notification_to_firestore(message, type, location.id)

        if average_precipitation <= parametro.min_pluvi:
            message = f"A precipitação média mínima de {parametro.min_pluvi}°C em {location.nome} ultrapassou o limite estipulado de{num_days} dias!"
            await add_notification_to_firestore(message, type, location.id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao procurar verificar temperatura prolongada: {e}",
        )

