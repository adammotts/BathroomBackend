from pydantic import BaseModel, EmailStr
from typing import List, Optional, Tuple

class UserBase(BaseModel):
    email: EmailStr
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    avatarImage: Optional[str] = None
    bio: Optional[str] = None
    interests: Optional[List[Tuple[str, int]]] = []
    users_met_online: Optional[List[str]] = []
    users_met_in_person: Optional[List[str]] = []

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    username: str
    password: str

    class Config:
        from_attributes = True

class User(UserBase):
    id: str
    username: str

    class Config:
        from_attributes = True

class UserInDB(UserBase):
    id: str
    username: str
    hashed_password: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

    class Config:
        from_attributes = True
