from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from app.schemas.bathroom import Bathroom, CreateBathroomRequest
from app.schemas.user import User
from app.database.mongodb import db
import json

class BathroomModel:
    def __init__(self):
        self.collection = db["bathrooms"]

    async def create_from_json(self, file: UploadFile) -> List[Bathroom]:
        try:
            contents = await file.read()
            data = json.loads(contents.decode("utf-8"))

            if not isinstance(data, list):
                raise ValueError("JSON file must contain a list of bathroom records.")

            new_bathrooms = []

            for bathroom in data:
                now = datetime.now()

                new_bathroom = Bathroom(
                    **bathroom,
                    created_at=now,
                    updated_at=now
                )

                new_bathrooms.append(new_bathroom.model_dump())

            if new_bathrooms:
                await self.collection.insert_many(new_bathrooms)

            return [Bathroom(**bathroom) for bathroom in new_bathrooms]

        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON file format.")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    async def create_bathroom(self, bathroom: CreateBathroomRequest) -> Bathroom:
        bathroom_data = bathroom.model_dump()

        await self.collection.insert_one(bathroom_data)

        return Bathroom(**bathroom_data)

    async def get_all_bathrooms(self) -> List[Bathroom]:
        bathrooms_list = await self.collection.find().to_list(length=None)

        return [Bathroom(**bathroom) for bathroom in bathrooms_list]
    
    async def delete_all_bathrooms(self) -> None:
        await self.collection.delete_many({})

bathroom_model = BathroomModel()