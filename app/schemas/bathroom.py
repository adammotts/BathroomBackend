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

class GetWithinAreaRequest(BaseModel):
    top_left_latitude: float
    top_left_longitude: float
    bottom_right_latitude: float
    bottom_right_longitude: float

    class Config:
        from_attributes = True