from fastapi import APIRouter, HTTPException
from app.services.climatology import get_temporal_data
from app.services.formatted_response import format_climate_response 

router = APIRouter()

@router.get("/climate/")
async def get_climate_data(
    longitude: float,
    latitude: float,
    start: int,
    end: int
):
    try:
        # Definindo diretamente os parametros fixos
        parameters = "T2M,PRECTOTCORR"
        # Chama a função que acessa a API da NASA
        response = get_temporal_data(parameters, longitude, latitude, start, end)
        
        # Se houver algum erro na requisição à API da NASA
        if isinstance(response, str):
            raise HTTPException(status_code=400, detail=response)
        
        #print("Resposta da API da NASA JSON cru:", response)
        
        formatted_response = format_climate_response(response)
        
        #print("Resposta da API da NASA formatada:", formatted_response)

        return formatted_response  # Retorna o JSON da API da NASA
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
