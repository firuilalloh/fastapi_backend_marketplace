from fastapi import APIRouter, HTTPException
from supabase.lib.client_options import ClientOptions
from ..database import get_supabase_client
from ..models.product_model import Product, productResponse, productResponseId, productUpdate, productUpdateResponse
from ..services.product_service import s_get_all_products as sgap, s_get_product_by_id as sgpb, s_update_product as sup

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=productResponse)
def r_get_all_products():
    return sgap()

@router.get("/{id}", response_model=productResponseId)
def r_get_product_by_id(id: int):
    return sgpb(id)
    
@router.patch("/update/{id}", response_model=productUpdateResponse)
def r_update_product(id: int, product_update: productUpdate):

    update_data = product_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    return sup(id, update_data)