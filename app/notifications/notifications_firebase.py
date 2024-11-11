from datetime import datetime
from typing import Any, Dict, List

from app.database.firebase import get_db


async def add_notification_to_firestore(message: str, type: str, id_local: str) -> None:
    """Adiciona a notificação ao firebase"""
    db = get_db()  # Pega a sessão do firebase

    doc_ref = db.collection(
        "notifications"
    ).add(
        {
            "timestamp": datetime.now(),  # Pega a hora e data atual para mostrar quando a notificação foi criada
            "message": message,
            "type": type,
            "id_local": id_local,
            "is_active": True,
        }
    )
    # print("Notificação adicionada ao Firestore:", doc_ref) # para debug


async def get_notifications_by_local(id_local: str) -> List[Dict[str, Any]]:
    """Busca todas as notificações para um local específico no Firebase."""
    db = get_db()  # Função que retorna a conexão com o Firebase Firestore
    notifications_ref = db.collection("notifications")

    # Filtra as notificações pelo id_local
    query = notifications_ref.where("id_local", "==", id_local).where(
        "is_active", "==", True
    )
    results = query.stream()

    notifications = []
    for doc in results:
        notification_data = doc.to_dict()
        notification_data["id"] = doc.id  # Adiciona o ID do documento ao dicionário
        notifications.append(notification_data)

    return notifications
