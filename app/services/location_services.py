from app.database.firebase import get_db
from fastapi import HTTPException
from google.cloud.firestore import FieldFilter

db = get_db()
collection_ref = db.collection("localizacoes")


def exist_location_by_lat_long(latitude, longitude):
    try:
        # Retorna todos documentos com latitude e longitude iguais às do corpo da requisição
        docs = (
            collection_ref
            .where(filter=FieldFilter("latitude", "==", latitude))
            .where(filter=FieldFilter("longitude", "==", longitude))
            .stream()
        )

        # Verifica se algum documento encontrado tem as mesmas coordenadas
        for doc in docs:
            if doc.exists:
                return True

        return False
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao procurar localizações semelhantes: {e}")
    
def exist_location_by_id(id_location: str):
    try:
        # Busca o documento diretamente pelo ID fornecido
        doc = collection_ref.document(id_location).get()

        # Verifica se o documento existe
        if doc.exists:
            return True
        return False

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao procurar localização pelo ID: {e}")

def validate_location(latitude, longitude):
    
    if latitude < -90 or latitude > 90:
        return False
    if longitude < -180 or longitude > 180:
        return False
    
    return True