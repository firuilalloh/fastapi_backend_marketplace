from fastapi import APIRouter, HTTPException
from supabase.lib.client_options import ClientOptions
from ..database import get_supabase_client
from ..models import Product, productResponse, productResponseId, productUpdate, productUpdateResponse

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=productResponse)
def get_all_products():
    try:
        supabase = get_supabase_client()
        res = supabase.table("tb_product").select("*").execute()
        data_product = res.data
        return {
            "status": "success",
            "data": data_product,
            }
    except Exception as e:
        print("Error fetching products:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=productResponseId)
def get_product_by_id(id: int):
    try:
        supabase = get_supabase_client()
        res = supabase.table("tb_product").select("*").eq("id", id).execute()
        data_product = res.data
        if not data_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {
            "status": "success",
            "data": data_product,
            }
    except Exception as e:
        print("Error fetching product by ID:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/update/{id}", response_model=productUpdateResponse)
def update_product(id: int, product_update: productUpdate):

    update_data = product_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    try:
        supabase = get_supabase_client()
        res = supabase.table("tb_product").update(update_data).eq("id", id).execute()

        if not res.data:
            raise HTTPException(status_code=404, detail=f"Product with ID {id} not found or update failed")

        return {
            "status": "success",
            "message": "Product updated successfully",
            "product_id": id
            }
    
    except HTTPException:
        raise

    except Exception as e:
        print("Error updating product:", e)
        raise HTTPException(status_code=500, detail=str(e))