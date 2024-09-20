import requests
from typing import Union

"""
Faz uma requisição para a API da NASA para pegar dados climáticos diários

start (int): data de inicio no formato YYYYMMDD
end (int): data final no formato YYYYMMDD
"""
def get_temporal_data(parameters: str, longitude: Union[int, float], latitude: Union[int, float], start: int, end: int):
    try:
        #Monta a url com os dados fornecidos pelo usuario para poder fazer a requisição na api da NASA
        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        params = {
            "parameters": parameters,
            "community": "SB",
            "longitude": longitude,
            "latitude": latitude,
            "start": start,
            "end": end
        }

        #Faz o request
        response = requests.get(base_url, params=params)

        #Verifica se a requisição foi bem sucedida e retorna o json
        if response.status_code == 200:
            return response.json()

        #Tratamento de erros da api
        elif response.status_code == 422:
            return "Erro 422: Entidade não processável. Verifique os parâmetros da solicitação"
        elif response.status_code == 429:
            return "Erro 429: Muitas requisições. Aguarde antes de tentar novamente"
        elif response.status_code == 500:
            return "Erro 500: Erro interno do servidor"
        elif response.status_code == 503:
            return "Erro 503: Serviço indisponível"
        else:
            return f"Erro {response.status_code}: Não especificado."
        
    except requests.exceptions.RequestException as req_err:
            return f"Erro na requisição: {req_err}"