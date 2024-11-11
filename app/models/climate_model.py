from pydantic import BaseModel
from typing import List

class ClimateData(BaseModel):
    day: str
    temperature: float
    precipitation: float

class ApiResponse(BaseModel):
    message: str
    status: str
    data: List[ClimateData]