from pydantic import BaseModel
from typing import Optional

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