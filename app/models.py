from pydantic import BaseModel
from typing import Optional

# product models
class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str

class productResponse(BaseModel):
    status: str = "success"
    data: list[Product]

class productResponseId(BaseModel):
    status: str = "success"
    data: list[Product]

class productUpdate(BaseModel):
    name: Optional[str] = None
    price:  Optional[float] = None
    category: Optional[str] = None

class productUpdateResponse(BaseModel):
    status: str = "success"
    message: str
    product_id: int

# jasa models
class Jasa(BaseModel):
    id: int
    tier: str
    description: str
    price: float

class jasaResponse(BaseModel):
    status: str = "success"
    data: list[Jasa]

class jasaResponseId(BaseModel):
    status: str = "success"
    data: list[Jasa]

class jasaUpdate(BaseModel):
    tier: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class User(BaseModel):
    id: int
    user: str
    email: str

class userResponse(BaseModel):
    status: str = "success"
    data: list[User]