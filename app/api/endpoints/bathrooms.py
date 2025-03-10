from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr
from bson import ObjectId
from app.schemas.bathroom import Bathroom
from app.models.bathroom import bathroom_model
from app.models.user import user_model
from app.api.endpoints.users import get_current_user
from app.database.mongodb import db

router = APIRouter()

@router.post("/from-json", response_model=List[Bathroom])
async def populate_bathrooms():
    return await bathroom_model.create_from_json("/Users/ma/Documents/GitHub/BathroomBackend/data.json")

@router.get("/all", response_model=List[Bathroom])
async def get_bathrooms():
    return await bathroom_model.get_all_bathrooms()

@router.delete("/clear", response_model=None)
async def clear_bathrooms():
    return await bathroom_model.delete_all_bathrooms()