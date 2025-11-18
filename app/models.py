# app/models.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional, Tuple


class RegistrationRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=200)
    password: Optional[str] = Field(default=None, min_length=6, max_length=200)  # optional for demo


class RegistrationResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime

class UserItem(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime

class UserListResponse(BaseModel):
    items: List[UserItem]
    next_page_token: Optional[str] = None  # pass this back as ?page_token= to get next page
