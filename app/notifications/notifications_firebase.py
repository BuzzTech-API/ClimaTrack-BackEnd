from app.database.firebase import get_db

async def add_notification_to_firestore(
    message: str, 
    type: str, 
    id_local: str
) -> None:
    """Adiciona a notificação ao firebase"""
    db = get_db() # Pega a sessão do firebase

    doc_ref = db.collection("notifications").add({
        "timestamp": datetime.now(), # Pega a hora e data atual para mostrar quando a notificação foi criada
        "message": message,
        "type": type,
        "id_local": id_local,
        "is_active": True
    })
    # print("Notificação adicionada ao Firestore:", doc_ref) # para debug