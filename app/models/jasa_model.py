from pydantic import BaseModel
from typing import Optional, List

class Jasa(BaseModel):
    id: int
    nama_jasa: str
    description: str
    price: int

class JasaCreate(BaseModel):
    nama_jasa: str
    description: str
    price: int

class JasaResponseId(BaseModel):
    status: str = "success"
    data: list[Jasa]

class JasaUpdate(BaseModel):
    tier: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class JasaResponse(BaseModel):
    status: str = "success"
    data: List[Jasa]