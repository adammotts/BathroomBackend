from fastapi import APIRouter, HTTPException, status, Depends, Body, UploadFile, File
from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr
from bson import ObjectId
from app.schemas.bathroom import Bathroom, CreateBathroomRequest
from app.schemas.user import User
from app.models.bathroom import bathroom_model
from app.models.user import user_model
from app.api.endpoints.users import get_current_user
from app.database.mongodb import db

router = APIRouter()

@router.post("/from-json", response_model=List[Bathroom])
async def populate_bathrooms(file: UploadFile = File(...)):
    return await bathroom_model.create_from_json(file)

@router.post("/new", response_model=Bathroom)
async def create_bathroom(bathroom: CreateBathroomRequest = Body(...), current_user: User = Depends(get_current_user)):
    return await bathroom_model.create_bathroom(bathroom)

@router.get("/all", response_model=List[Bathroom])
async def get_bathrooms():
    return await bathroom_model.get_all_bathrooms()

@router.delete("/clear", response_model=None)
async def clear_bathrooms():
    return await bathroom_model.delete_all_bathrooms()