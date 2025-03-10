# schemas/interaction.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Interaction(BaseModel):
    content: str
    sender: EmailStr
    timestamp: datetime = datetime.now()
