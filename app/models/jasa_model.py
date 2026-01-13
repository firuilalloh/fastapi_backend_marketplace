from pydantic import BaseModel
from typing import Optional, List

class Jasa(BaseModel):
    id: int
    nama_jasa: str
    description: str
    price: int

class jasaCreate(BaseModel):
    nama_jasa: str
    description: str
    price: int

class jasaResponseId(BaseModel):
    status: str = "success"
    data: list[Jasa]

class jasaUpdate(BaseModel):
    tier: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None