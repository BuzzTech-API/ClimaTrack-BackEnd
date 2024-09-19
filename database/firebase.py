import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

db = None 

def get_db():
    global db

    if not db:
        try:
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            db = firestore.client()
        except Exception as e:
            print("Erro ao inicializar o Firestore:", str(e))
            raise
    return db