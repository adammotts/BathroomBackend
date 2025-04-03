from fastapi import APIRouter, HTTPException, Depends, Body, UploadFile, File, Query
from typing import List
from app.schemas.bathroom import Bathroom, CreateBathroomRequest, GetWithinAreaRequest
from app.schemas.user import User
from app.models.bathroom import bathroom_model

router = APIRouter()

@router.post("/from-json", response_model=List[Bathroom])
async def populate_bathrooms(file: UploadFile = File(...)):
    return await bathroom_model.create_from_json(file)

@router.post("/new", response_model=Bathroom)
async def create_bathroom(bathroom: CreateBathroomRequest = Body(...)):
    return await bathroom_model.create_bathroom(bathroom)

@router.patch("/approve", response_model=Bathroom)
async def approve_bathroom(bathroom_id: str):
    return await bathroom_model.approve_bathroom(bathroom_id)

@router.get("/area", response_model=List[Bathroom])
async def get_within_area(
    top_left_latitude: float = Query(...),
    top_left_longitude: float = Query(...),
    bottom_right_latitude: float = Query(...),
    bottom_right_longitude: float = Query(...)
):
    return await bathroom_model.get_within_area(
        GetWithinAreaRequest(
            top_left_latitude=top_left_latitude,
            top_left_longitude=top_left_longitude,
            bottom_right_latitude=bottom_right_latitude,
            bottom_right_longitude=bottom_right_longitude
        )
    )

@router.get("/all", response_model=List[Bathroom])
async def get_bathrooms():
    return await bathroom_model.get_all_bathrooms()

@router.delete("/clear", response_model=None)
async def clear_bathrooms():
    return await bathroom_model.delete_all_bathrooms()