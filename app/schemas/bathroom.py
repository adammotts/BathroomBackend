# app/schemas/bathroom.py
from pydantic import BaseModel
from datetime import datetime

class Bathroom(BaseModel):
    id: str
    name: str
    address: str
    zip: str
    latitude: float
    longitude: float
    hours: str
    remarks: str
    approved: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        from_attributes = True

class CreateBathroomRequest(Bathroom):
    name: str
    address: str
    zip: str
    latitude: float
    longitude: float
    hours: str
    remarks: str

class GetWithinAreaRequest(BaseModel):
    top_left_latitude: float
    top_left_longitude: float
    bottom_right_latitude: float
    bottom_right_longitude: float

    class Config:
        from_attributes = True