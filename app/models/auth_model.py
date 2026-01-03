from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    username: str
    role: str | None = "user"
    password: str

class Token(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    id: int | None = None
    email: str
    role: str = "user"
    username: str

class UserInDb(User):
    hashed_password: str

class UserCreate(BaseModel):
    email: str
    username: str
    password: str