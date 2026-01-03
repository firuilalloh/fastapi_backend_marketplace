from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from ..models.product_model import Product, productResponse, productResponseId, productUpdate, productUpdateResponse
from ..services.product_service import s_get_all_products as sgap, s_get_product_by_id as sgpb, s_update_product as sup, s_delete_product as sdp
from ..services.authentication_service import get_current_user, check_is_admin
from ..models.auth_model import User

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=productResponse)
def r_get_all_products():
    return sgap()

@router.get("/{id}", response_model=productResponseId)
def r_get_product_by_id(id: int, current_user: Annotated[User, Depends(get_current_user)]):
    return sgpb(id)
    
@router.delete("/delete/{id}")
def r_delete_product(id: int, admin_user: Annotated[User, Depends(check_is_admin)]):
    return sdp(id)

@router.patch("/update/{id}", response_model=productUpdateResponse)
def r_update_product(id: int, product_update: productUpdate, admin_user: Annotated[User, Depends(check_is_admin)]):

    update_data = product_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    return sup(id, update_data)