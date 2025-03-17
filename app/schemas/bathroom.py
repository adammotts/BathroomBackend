# app/schemas/bathroom.py
from pydantic import BaseModel
from datetime import datetime

class Bathroom(BaseModel):
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

class CreateBathroomRequest(Bathroom):
    pass