from fastapi import APIRouter, HTTPException
from supabase.lib.client_options import ClientOptions
from ..database import get_supabase_client
from ..models import Jasa, jasaResponse, jasaResponseId, jasaUpdate

router = APIRouter(prefix="/api/jasa", tags=["Jasa"])

@router.get("/", response_model=jasaResponse)
def get_all_jasa():
    try:
        supabase = get_supabase_client()
        res = supabase.table("tb_jasa").select("*").execute()
        data_jasa = res.data
        return {
            "status": "success",
            "data": data_jasa,
            }
    except Exception as e:
        print("Error fetching jasa:", e)
        raise HTTPException(status_code=500, detail=str(e))

