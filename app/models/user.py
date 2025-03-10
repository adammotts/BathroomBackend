# app/models/user.py
from pydantic import EmailStr
from app.schemas.user import UserInDB
from app.database.mongodb import db
from typing import List, Tuple

class User:
    def __init__(self):
        self.collection = db["users"]

    async def get_by_email(self, email: EmailStr) -> UserInDB:
        return await self.collection.find_one({"email": email})

    async def get_by_username(self, username: str) -> UserInDB:
        return await self.collection.find_one({"username": username})

    async def get_by_id(self, id: str) -> UserInDB:
        return await self.collection.find_one({"id": id})
    
    async def get_all(self):
        return await self.collection.find().to_list(1000)
    
    async def record_online_interaction(self, user1: UserInDB, user2: UserInDB) -> None:
        user1_id = str(user1["id"])
        user2_id = str(user2["id"])

        if user2_id not in user1["users_met_online"]:
            user1["users_met_online"].append(user2_id)
            await self.collection.update_one(
                {"id": user1_id},
                {"$set": {"users_met_online": user1["users_met_online"]}}
            )

        if user1_id not in user2["users_met_online"]:
            user2["users_met_online"].append(user1_id)
            await self.collection.update_one(
                {"id": user2_id},
                {"$set": {"users_met_online": user2["users_met_online"]}}
            )

    async def check_existing_username_and_email(self, username: str, email: EmailStr) -> bool:
        existing_user = await self.collection.find_one({
            "$or": [
                {"email": email.lower()},
                {"username": username.lower()}
            ]
        })

        return existing_user is not None
    
    async def create_user(self, form_data):
        return await self.collection.insert_one(form_data)
    
    async def update_interests(self, user_id: str, interests: List[Tuple[str, int]]):
        return await self.collection.update_one({"id": user_id}, {"$set": {"interests": interests}})


user_model = User()