from pydantic import BaseModel
from typing import List
from datetime import datetime

class LocationParameters(BaseModel):
    location_id: str
    max_pluvi: float
    min_pluvi: float
    max_temp: float
    min_temp: float
    duracao_max: int
        
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