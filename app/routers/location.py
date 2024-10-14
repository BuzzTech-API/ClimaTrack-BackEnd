from fastapi import APIRouter, HTTPException
from app.models.location_model import Location
from app.database.firebase import get_db
from app.services.exist_location import exist_location

router = APIRouter()

@router.post("/add_location/")
async def add_location(location: Location):
    try:
        db = get_db()
        collection_ref = db.collection("localizacoes")

        # Passando latitude e longitude corretamente
        if exist_location(location.latitude, location.longitude):
            raise HTTPException(status_code=409, detail="A localização já existe.")

        data = {
            "nome": location.nome,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "isOffline": False
        }

        collection_ref.add(data)

        return {"message": "Localização adicionada com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar localização: {e}")
