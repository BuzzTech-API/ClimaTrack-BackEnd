from app.database.firebase import get_db
from fastapi import HTTPException

def exist_location(latitude, longitude):
    try:
        db = get_db()
        collection_ref = db.collection("localizacoes")

        # Retorna todos documentos com latitude e longitude iguais às do corpo da requisição
        docs = (
            collection_ref
            .where("latitude", "==", latitude)
            .where("longitude", "==", longitude)
            .stream()
        )

        # Verifica se algum documento encontrado tem as mesmas coordenadas
        for doc in docs:
            data = doc.to_dict() 
            if data['latitude'] == latitude and data['longitude'] == longitude:
                return True

        return False

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao procurar localizações semelhantes: {e}")
