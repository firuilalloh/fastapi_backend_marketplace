from supabase import Client

def toggle_wishlist(supabase: Client, user_id:str, product_id:int):
    check = supabase.table("tb_wishlist").select("*").eq("user_id", user_id).eq("product_id", product_id).execute()

    if check.data:
        supabase.table("tb_wishlist").delete().eq("user_id", user_id).eq("product_id", product_id).execute()
        return {"status": "removed", "message": "Product removed from wishlist"}
    else:
        supabase.table("tb_wishlist").insert({"user_id": user_id, "product_id": product_id}).execute()
        return {"status": "added", "message": "Product added to wishlist"}
    
def get_user_wishlist(supabase: Client, user_id: str):
    response = supabase.table("tb_wishlist").select("""id, user_id, product_id, created_at, product_details:tb_product(*), user_details:tb_user(id, username, email)""").eq("user_id", user_id).execute()
    
    return response.data