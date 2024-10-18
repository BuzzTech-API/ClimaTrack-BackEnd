from typing import Union
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def weather_forecast(longitude: Union[int, float], latitude: Union[int, float]):
    """
    Função que obtém as previsões do clima para as coordenadas fornecidas.

    Args:
        longitude (Union[int, float]): A longitude do local.
        latitude (Union[int, float]): A latitude do local.

    Returns:
        list: Lista de dicionários com dados diários do clima ou mensagem de erro.
    """
    try:
        #Monta a url com os dados fornecidos pelo usuario para poder fazer a requisição na api da Weather Forecast
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
            "timezone": "America/Sao_Paulo",
            "past_days": 1,
            "forecast_days": 1
        }

        # Chamada à API
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Extrai os dados diários
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy().astype(float)
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy().astype(float)
        daily_precipitation = daily.Variables(2).ValuesAsNumpy().astype(float)

        # Cria uma lista de datas com base no tempo inicial e final
        start_time = pd.to_datetime(daily.Time(), unit="s", utc=True) # Converte o tempo de início para datetime
        end_time = pd.to_datetime(daily.TimeEnd(), unit="s", utc=True) # Converte o tempo de fim para datetime
        interval = pd.Timedelta(seconds=daily.Interval()) # Define o intervalo de tempo entre os registros

        dates = [] # Lista para armazenar as datas
        current_time = start_time # Inicia o tempo atual com o tempo de início
        while current_time < end_time:
            dates.append(current_time) # Adiciona a data atual à lista
            current_time += interval # Avança o tempo atual pelo intervalo definido

        daily_data = [] # Lista para armazenar os dados diários formatados
        for i, date in enumerate(dates):
            # Adiciona um dicionário com as informações diárias do clima
            daily_data.append({
                "date": date.strftime("%d-%m-%Y"), # Formata a data para o formato "dia-mês-ano"
                "temperature_max (C°)": daily_temperature_2m_max[i],
                "temperature_min (C°)": daily_temperature_2m_min[i],
                "precipitation (mm)": daily_precipitation[i],
            })

        return daily_data
    
    except Exception as e:
        return str(e)