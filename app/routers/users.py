from fastapi import APIRouter, HTTPException
from supabase.lib.client_options import ClientOptions
from ..database import get_supabase_client
from ..models import User, userResponse

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/", response_model=userResponse)
def get_all_users():
    try:
        supabase = get_supabase_client()
        res = supabase.table("tb_user").select("*").execute()
        data_user = res.data
        return {
            "status": "success",
            "data": data_user,
            }
    except Exception as e:
        print("Error fetching users:", e)
        raise HTTPException(status_code=500, detail=str(e))