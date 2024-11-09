from app.routers.climate import get_current_climate_data, get_climate_data
from app.notifications.notifications_firebase import add_notification_to_firestore
from app.models.location_model import LocationDTO
from app.models.climate_model import ApiResponse

async def check_extreme_temperature(
    location: LocationDTO
) -> None:
    """"Exemplo de função que checa determinado parâmetro"""
    type = "Temperatura Extrema" # Tipo da notificação
    current_data = await get_current_climate_data(location.latitude, location.longitude)

    # Temperatura do dia atual
    current_temp = current_data[1]

    temperature_max_threshold = 20  # Define o limite maximo da temperatura. Pegar das preferencias de local do usuario posteriormente.
    temperature_min_threshold = 30  # Define o limite minimo da temperatura. Pegar das preferencias de local do usuario posteriormente.

    # Verifica se a temperatura excede o limite (ajuste conforme necessário)
    if current_temp > temperature_max_threshold:
        message = f"A temperatura em {location.nome} está a cima do limite estipulado!" # Menagem da notificação
        await add_notification_to_firestore(message, type, location.id)
    if current_temp < temperature_min_threshold:
        message = f"A temperatura em {location.nome} está a baixo do limite estipulado!" # Menagem da notificação
        await add_notification_to_firestore(message, type, location.id)


async def check_extreme_precipitation(
    location: LocationDTO
) -> None:
    """"Exemplo de função que checa determinado parâmetro"""
    type = "Precipitacao Extrema" #Tipo da notificação
    current_data = await get_current_climate_data(location.latitude, location.longitude)

    # Precipitacao do dia atual
    current_prec = current_data[2]

    precipitation_max_threshold = 0  # Define o limite maximo da humidade. Pegar das preferencias de local do usuario posteriormente.
    precipitation_min_threshold = 1  # Define o limite minimo da humidade. Pegar das preferencias de local do usuario posteriormente.

    # Verifica se a precipitação excede o limite (ajuste conforme necessário)
    if current_prec > precipitation_max_threshold:
        message = f"A precipitação em {location.nome} está a cima do limite estipulado!" # Menagem da notificação
        await add_notification_to_firestore(message, type, location.id)
    if current_prec < precipitation_min_threshold:
        message = f"A precipitação em {location.nome} está a baixo do limite estipulado!" # Menagem da notificação
        await add_notification_to_firestore(message, type, location.id)


async def check_prolonged_temperature(
    location: LocationDTO
) -> None:
    """"Exemplo de função que checa determinado parâmetro"""
    type = "Precipitação Extrema Prolongada" # Tipo da notificação

    # Pega os dias estipulados pelo usuário.
    # Com as preferencias do usuario, pegar o dia em que a preferencia foi criada e ir adicionando aos dias. Ex: começou dia 07 com 5 dias e ja se passou 2 vai do dia 07 ao 09
    data = await get_climate_data(location.longitude, location.latitude, 20240912, 20240922)
    climate = ApiResponse(**data)

    # Calculando a média de temperatura e precipitação 
    total_temperature = sum(item.temperature for item in api_response.data) 
    total_precipitation = sum(item.precipitation for item in api_response.data) 
    num_days = len(api_response.data)

    # Média de temperatura e precipitação
    average_temperature = total_temperature / num_days 
    average_precipitation = total_precipitation / num_days

    temperature_threshold_max = 20  # Define o limite máximo. Pegar das preferencias de local do usuario posteriormente.
    temperature_threshold_min = 0   # Define o limite minimo. Exemplo


    precipitation_threshold_max = 200
    precipitation_threshold_min = 0
    # Verifica se a temperatura excede o limite (ajuste conforme necessário)
    # É possivel colocar mais verificações como temperatura mínima
    if average_temperature > temperature_threshold_max:
        message = f"A temperatura média máxima em {location.nome} ultrapassou o limite estipulado de {num_days} dias!" # Menagem da notificação
        await add_notification_to_firestore(message, type, location.id)

    if average_temperature <= temperature_threshold_min:
        message = f"A temperatura média mínima em {location.nome} ultrapassou o limite estipulado de {num_days} dias!" # Menagem da notificação
        await add_notification_to_firestore(message, type, location.id)
    
    if average_precipitation > precipitation_threshold_min:
        message = f"A precipitação média máxima em {location.nome} ultrapassou o limite estipulado de {num_days} dias!" # Menagem da notificação
        await add_notification_to_firestore(message, type, location.id)

    if average_precipitation <= precipitation_threshold_min:
        message = f"A precipitação média mínima em {location.nome} ultrapassou o limite estipulado de {num_days} dias!" # Menagem da notificação
        await add_notification_to_firestore(message, type, location.id)
    