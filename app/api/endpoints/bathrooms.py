from fastapi import APIRouter, HTTPException, Depends, Body, UploadFile, File
from typing import List
from app.schemas.bathroom import Bathroom, CreateBathroomRequest, GetWithinAreaRequest
from app.schemas.user import User
from app.models.bathroom import bathroom_model
from app.api.endpoints.users import get_current_user

router = APIRouter()

@router.post("/from-json", response_model=List[Bathroom])
async def populate_bathrooms(file: UploadFile = File(...)):
    return await bathroom_model.create_from_json(file)

@router.post("/new", response_model=Bathroom)
async def create_bathroom(bathroom: CreateBathroomRequest = Body(...), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException("Must be signed in")

    return await bathroom_model.create_bathroom(bathroom)

@router.get("/area", response_model=List[Bathroom])
async def get_within_area(bounding_box: GetWithinAreaRequest = Body(...)):
    return await bathroom_model.get_within_area(bounding_box)

@router.get("/all", response_model=List[Bathroom])
async def get_bathrooms():
    return await bathroom_model.get_all_bathrooms()

@router.delete("/clear", response_model=None)
async def clear_bathrooms():
    return await bathroom_model.delete_all_bathrooms()