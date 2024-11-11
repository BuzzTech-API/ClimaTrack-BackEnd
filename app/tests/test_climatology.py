import pytest
from app.services.climatology import get_temporal_data
import json

@pytest.fixture
def expected_response():
    # Isso é um exemplo aleatório de resposta que esperamos da API da NASA
    return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                -45.762218,
                -23.166403,
                853.91
                ]
            },
            "properties": {
                "parameter": {
                "T2M": {
                    "20201201": 23.52,
                    "20201202": 23.28,
                    "20201203": 25.36,
                    "20201204": 24.32,
                    "20201205": 22.05,
                    "20201206": 20.55,
                    "20201207": 21.28,
                    "20201208": 21.69,
                    "20201209": 20.99,
                    "20201210": 20.98,
                    "20201211": 21.04,
                    "20201212": 22.11,
                    "20201213": 22.51,
                    "20201214": 24.69,
                    "20201215": 23.7,
                    "20201216": 23.82,
                    "20201217": 23.04,
                    "20201218": 23.14,
                    "20201219": 24.68,
                    "20201220": 23.95,
                    "20201221": 24.68,
                    "20201222": 21.88,
                    "20201223": 19.51,
                    "20201224": 19.06,
                    "20201225": 19.48,
                    "20201226": 20.69,
                    "20201227": 20.59,
                    "20201228": 21.88,
                    "20201229": 21.84,
                    "20201230": 22.84,
                    "20201231": 23.69
                }
                }
  },
  "header": {
    "title": "NASA/POWER CERES/MERRA2 Native Resolution Daily Data",
    "api": {
      "version": "v2.5.9",
      "name": "POWER Daily API"
    },
    "sources": [
      "merra2"
    ],
    "fill_value": -999,
    "start": "20201201",
    "end": "20201231"
  },
  "messages": [],
  "parameters": {
    "T2M": {
      "units": "C",
      "longname": "Temperature at 2 Meters"
    }
  },
  "times": {
    "data": 1.28,
    "process": 0.11
  }
}

def test_get_temporal_data(expected_response):
    # Parâmetros para a função de teste
    parameters = "T2M"
    longitude = -45.762218
    latitude = -23.166403
    start = 20201201
    end = 20201231

    # Chamando a função para pegar os dados
    response = get_temporal_data(parameters, longitude, latitude, start, end)

    # É preciso rotar o comando "pytest -s app/tests/test_climatology.py" para que seja possível verificar o JSON da resposta.
    print(json.dumps(response, indent=4))

    # Verificando se a resposta contém a chave 'properties'
    assert "properties" in response, "A resposta não contém a chave 'properties'"
    
    # TESTE para REDLIGHT - Este teste falhará porque a chave 'invalid_key' não existe, manter comentado caso queira testa o GREENLIGHT
    #assert "invalid_key" in response, "A chave 'invalid_key' não existe, o teste deve falhar."

    # Verificando se os dados de temperatura estão presentes e corretos
    for date, temp in expected_response["properties"]["parameter"]["T2M"].items():
        assert response["properties"]["parameter"]["T2M"].get(date) == temp, f"Erro na temperatura do dia {date}"


# JSON esperado para os parametros testados:
# {
#   "type": "Feature",
#   "geometry": {
#     "type": "Point",
#     "coordinates": [
#       -45.762218,
#       -23.166403,
#       853.91
#     ]
#   },
#   "properties": {
#     "parameter": {
#       "T2M": {
#         "20201201": 23.52,
#         "20201202": 23.28,
#         "20201203": 25.36,
#         "20201204": 24.32,
#         "20201205": 22.05,
#         "20201206": 20.55,
#         "20201207": 21.28,
#         "20201208": 21.69,
#         "20201209": 20.99,
#         "20201210": 20.98,
#         "20201211": 21.04,
#         "20201212": 22.11,
#         "20201213": 22.51,
#         "20201214": 24.69,
#         "20201215": 23.7,
#         "20201216": 23.82,
#         "20201217": 23.04,
#         "20201218": 23.14,
#         "20201219": 24.68,
#         "20201220": 23.95,
#         "20201221": 24.68,
#         "20201222": 21.88,
#         "20201223": 19.51,
#         "20201224": 19.06,
#         "20201225": 19.48,
#         "20201226": 20.69,
#         "20201227": 20.59,
#         "20201228": 21.88,
#         "20201229": 21.84,
#         "20201230": 22.84,
#         "20201231": 23.69
#       }
#     }
#   },
#   "header": {
#     "title": "NASA/POWER CERES/MERRA2 Native Resolution Daily Data",
#     "api": {
#       "version": "v2.5.9",
#       "name": "POWER Daily API"
#     },
#     "sources": [
#       "merra2"
#     ],
#     "fill_value": -999,
#     "start": "20201201",
#     "end": "20201231"
#   },
#   "messages": [],
#   "parameters": {
#     "T2M": {
#       "units": "C",
#       "longname": "Temperature at 2 Meters"
#     }
#   },
#   "times": {
#     "data": 1.28,
#     "process": 0.11
#   }
# }
#