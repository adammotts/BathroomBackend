from datetime import datetime
from typing import List
from fastapi import UploadFile, HTTPException
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from app.schemas.bathroom import Bathroom, CreateBathroomRequest, GetWithinAreaRequest
from app.database.mongodb import db
import json

class BathroomModel:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = db["bathrooms"]

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
                    id=str(ObjectId()),
                    approved=True,
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

        await self.collection.insert_one({ **bathroom_data, "approved": True })

        return Bathroom(**bathroom_data)
    
    async def approve_bathroom(self, bathroom_id: str) -> Bathroom:
        result = await self.collection.find_one_and_update(
            {"id": bathroom_id},
            {"$set": {"approved": True}},
            return_document=True
        )

        if result is None:
            raise ValueError("Bathroom not found")

        return Bathroom(**result)
    
    async def get_within_area(self, bounding_box: GetWithinAreaRequest) -> List[Bathroom]:
        query = {
            "latitude": {
                "$gte": bounding_box.bottom_right_latitude,
                "$lte": bounding_box.top_left_latitude
            },
            "longitude": {
                "$gte": bounding_box.top_left_longitude,
                "$lte": bounding_box.bottom_right_longitude
            }
        }

        bathrooms_list = await self.collection.find(query).to_list(length=None)
        return [Bathroom(**bathroom) for bathroom in bathrooms_list]

    async def get_all_bathrooms(self) -> List[Bathroom]:
        bathrooms_list = await self.collection.find({"approved": True}).to_list(length=None)

        return [Bathroom(**bathroom) for bathroom in bathrooms_list]
    
    async def delete_all_bathrooms(self) -> None:
        await self.collection.delete_many({})

bathroom_model = BathroomModel()