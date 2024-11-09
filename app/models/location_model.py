from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    nome: str
    latitude: float
    longitude: float

class LocationDTO(BaseModel):
    nome: str
    latitude: float
    longitude: float
    isOffline: bool 
    id: str

class LocationsDTO(BaseModel): 
    locations: List[LocationDTO]