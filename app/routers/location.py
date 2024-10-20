from fastapi import APIRouter, HTTPException
from app.models.location_model import Location
from app.database.firebase import get_db
from app.services.location_services import exist_location_by_lat_long, exist_location_by_id, validate_location

router = APIRouter()
db = get_db()
collection_ref = db.collection("localizacoes")

@router.post("/add_location/")
async def add_location(location: Location):
    try:
        # Verifica se as coordenadas são válidas
        if not validate_location(location.latitude, location.longitude):
            raise HTTPException(status_code=400, detail= "Coordenadas inválidas. A latitude deve estar entre -90 e 90, e a longitude entre -180 e 180.")
        
        # Verifica se a localização com a latitude e longitude fornecidas já existe
        if exist_location_by_lat_long(location.latitude, location.longitude):
            raise HTTPException(status_code=409, detail="A localização já existe.")

        data = {
            "nome": location.nome,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "isOffline": False
        }

        # Adiciona os dados ao Firestore
        doc_ref = collection_ref.add(data)

        return {
            "id": doc_ref[1].id,  # Retorna o ID do documento recém-criado
            "message": "Localização adicionada com sucesso!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar localização: {e}")

@router.delete("/del_location/")
def delete_location(id_location: str):
    try:
        # Verifica se a localização com o ID fornecido existe
        if not exist_location_by_id(id_location):
            raise HTTPException(status_code=404, detail="Localização não encontrada no banco de dados.")

        collection_ref.document(id_location).delete()

        return {"message": "Localização deletada com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar localização: {e}")
    
# Ivan Germano: Rota para buscar todas as localizações utilizando stream() que é uma função fornecida pela 
# biblioteca do Firebase para o Firestore. Ele é utilizado para obter todos os documentos dentro de uma coleção.
@router.get("/find_all_locations/")
async def find_all_locations():
    try:
        locations = []
        docs = collection_ref.stream()
        for doc in docs:
            location_data = doc.to_dict()
            # Ivan Germano: Adiciona o ID do documento para permitir a manipulação dele no frontend
            location_data["id"] = doc.id 
            locations.append(location_data)

        # Ivan Germano: O print abaixo é para debug caso queira ver como os dados vem do firestore.
        # print(locations) 
        return {"locations": locations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar localizações: {e}")