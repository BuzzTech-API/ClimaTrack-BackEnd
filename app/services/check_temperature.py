from app.routers.climate import get_current_climate_data
from app.notifications.notifications import add_notification_to_firestore
from app.models.location_model import LocationDTO

async def check_extreme_temperature(
    location: LocationDTO
) -> None:
    """"Exemplo de função que checa determinado parâmetro"""
    current_data = await get_current_climate_data(location.latitude, location.longitude)

    # Temperatura do dia atual
    current_temp = current_data[1]['temperature_max (C°)']

    temperature_threshold = 20  # Define o limite. Pegar das preferencias de local do usuario posteriormente.

    # Verifica se a temperatura excede o limite (ajuste conforme necessário)
    # É possivel colocar mais verificações como temperatura mínima
    if current_temp > temperature_threshold:
        message = f"A temperatura em {location.nome} ultrapassou o limite estipulado!" # Menagem da notificação
        type = "Temperatura Extrema" # Tipo da notificação
        add_notification_to_firestore(message, type, location.id)