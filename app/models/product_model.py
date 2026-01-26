from pydantic import BaseModel, Field
from typing import List, Optional

class Product(BaseModel):
    id: int
    image_url: Optional[List[str]] = Field(default_factory=list)
    name: str
    price: float
    tech: list[str] = Field(default_factory=list)
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
    tech: Optional[list[str]] = None
    description: Optional[str] = None
    image_url: Optional[List[str]] = None
class productUpdateResponse(BaseModel):
    status: str = "success"
    message: str
    product_id: Optional[int] = None

class ProductCreateResponse(BaseModel):
    status: str = "success"
    message: str
    data: Optional[list[Product]] = None