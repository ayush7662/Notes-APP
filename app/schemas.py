from datetime import datetime
from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str 

class NoteCreateSchema(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True

class ShareSchema(BaseModel):
    share_with_email: EmailStr
