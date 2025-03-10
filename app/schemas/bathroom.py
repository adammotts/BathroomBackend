# app/schemas/bathroom.py
from pydantic import BaseModel
from datetime import datetime

class BathroomRaw(BaseModel):
    name: str
    address: str
    zip: str
    latitude: str
    longitude: str
    hours: str
    remarks: str
    dist: float

    class Config:
        from_attributes = True

class Bathroom(BaseModel):
    id: str
    name: str
    address: str
    zip: str
    latitude: float
    longitude: float
    hours: str
    remarks: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        from_attributes = True