from pydantic import BaseModel

class Location(BaseModel):
    nome: str
    latitude: float
    longitude: float
