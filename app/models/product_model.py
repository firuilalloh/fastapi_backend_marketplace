from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    image_url: Optional[str] = None
    name: str
    price: float
    tech: str
    description: Optional[str] = None

class productResponse(BaseModel):
    status: str = "success"
    data: list[Product]

class productResponseId(BaseModel):
    status: str = "success"
    data: list[Product]

class productUpdate(BaseModel):
    name: Optional[str] = None
    price:  Optional[float] = None
    tech: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class productUpdateResponse(BaseModel):
    status: str = "success"
    message: str
    product_id: int