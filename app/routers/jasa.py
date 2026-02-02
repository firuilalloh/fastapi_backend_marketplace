from fastapi import APIRouter
from ..models.jasa_model import (
    JasaResponse,
    JasaCreate,
    JasaUpdate
)
from ..services.jasa_service import (
    s_get_all_jasa,
    s_get_jasa_by_id,
    s_create_jasa,
    s_update_jasa
)

router = APIRouter(
    prefix="/api/jasa",
    tags=["Jasa"]
)

@router.get("/", response_model=JasaResponse)
def get_all_jasa():
    return s_get_all_jasa()

@router.get("/{jasa_id}")
def get_jasa_by_id(jasa_id: int):
    return s_get_jasa_by_id(jasa_id)

@router.post("/")
def create_jasa(payload: JasaCreate):
    return s_create_jasa(payload.dict())

@router.put("/{jasa_id}")
def update_jasa(jasa_id: int, payload: JasaUpdate):
    return s_update_jasa(
        jasa_id,
        payload.dict(exclude_unset=True)
    )
