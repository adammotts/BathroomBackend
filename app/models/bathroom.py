from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from app.schemas.bathroom import Bathroom, BathroomRaw
from app.schemas.user import User
from app.database.mongodb import db
import json

class BathroomModel:
    def __init__(self):
        self.collection = db["bathrooms"]

    async def create_from_json(self, file_path: str) -> None:
        new_bathrooms = []

        with open(file_path, "r", encoding="utf-8") as file:
            bathrooms = json.load(file)

        for bathroom in bathrooms:
            bathroom_id = str(ObjectId())
            now = datetime.now()

            new_bathroom = Bathroom(**bathroom, id=bathroom_id, created_at=now, updated_at=now)

            new_bathrooms.append(
                new_bathroom.model_dump()
            )

        await self.collection.insert_many(new_bathrooms)

        return [Bathroom(**bathroom) for bathroom in new_bathrooms]

    async def get_all_bathrooms(self) -> List[Bathroom]:
        bathrooms_list = await self.collection.find().to_list(length=None)

        return [Bathroom(**bathroom) for bathroom in bathrooms_list]
    
    async def delete_all_bathrooms(self) -> None:
        await self.collection.delete_many({})

bathroom_model = BathroomModel()