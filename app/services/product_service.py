from fastapi import HTTPException
from supabase.lib.client_options import ClientOptions
from ..database import get_supabase_client

def s_get_all_products():
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
    
def s_get_product_by_id(id: int):
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
    
def s_update_product(id: int, update_data: dict):
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
    except Exception as e:
        print("Error updating product:", e)
        raise HTTPException(status_code=500, detail=str(e))