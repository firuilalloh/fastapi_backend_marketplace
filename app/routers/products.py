from typing import Annotated, Optional, List
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from ..models.product_model import Product, productResponse, productResponseId, productUpdate, productUpdateResponse, ProductCreateResponse
from ..services.product_service import s_get_all_products as sgap, s_get_product_by_id as sgpb, s_update_product as sup, s_delete_product as sdp, s_create_product as scp
from ..services.authentication_service import get_current_user, check_is_admin
from ..models.auth_model import User

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/", response_model=productResponse)
def r_get_all_products():
    return sgap()


@router.get("/{id}", response_model=productResponseId)
def r_get_product_by_id(id: int, current_user: Annotated[User, Depends(get_current_user), Depends(check_is_admin)]):
    return sgpb(id)


@router.post("/create", response_model=ProductCreateResponse)
async def r_create_product(
    name: str = Form(...),
    price: float = Form(...),
    tech: str = Form(...),
    description: Optional[str] = Form(None),
    files: list[UploadFile] = File(...),
    admin_user: Annotated[User, Depends(check_is_admin)] = None
):
    tech_list = [item.strip() for item in tech.split(",")]
    return scp(name, price, tech_list, description, files)


@router.delete("/delete/{id}")
def r_delete_product(id: int, admin_user: Annotated[User, Depends(check_is_admin)]):
    return sdp(id)


@router.patch("/update/{id}", response_model=productUpdateResponse)
async def r_update_product(
    id: int,
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    tech: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    admin_user: Annotated[User, Depends(check_is_admin)] = None
):
    tech_list = [t.strip() for t in tech.split(",")] if tech else None

    return sup(id=id, name=name, price=price, tech=tech_list, description=description, files=files)
