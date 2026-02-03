from ..database import get_supabase_client
def s_get_all_jasa():
    supabase = get_supabase_client()
    result = supabase.table("tb_jasa").select("*").execute()

    return {
        "status": "success",
        "data": result.data
    }

def s_get_jasa_by_id(jasa_id: int):
    supabase = get_supabase_client()

    result = (
        supabase
        .table("tb_jasa")
        .select("*")
        .eq("id", jasa_id)
        .single()
        .execute()
    )

    return {
        "status": "success",
        "data": result.data
    }

def s_create_jasa(payload: dict):
    supabase = get_supabase_client()
    result = supabase.table("tb_jasa").insert(payload).execute()

    return {
        "status": "success",
        "message": "Jasa berhasil ditambahkan",
        "data": result.data
    }

def s_update_jasa(jasa_id: int, payload: dict):
    supabase = get_supabase_client()

    result = (
        supabase
        .table("tb_jasa")
        .update(payload)
        .eq("id", jasa_id)
        .execute()
    )

    return {
        "status": "success",
        "message": "Jasa berhasil diperbarui",
        "data": result.data
    }

