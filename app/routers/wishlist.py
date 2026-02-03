from fastapi import APIRouter, Depends
from app.services import wishlist_service
from app.models.wishlist_model import WishlistBase
from app.database import get_supabase_client
from app.services.authentication_service import get_current_user 

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.post("/toggle")
async def toggle(
    request: WishlistBase, 
    current_user = Depends(get_current_user), 
    db = Depends(get_supabase_client)
):
    result = wishlist_service.toggle_wishlist(db, current_user.id, request.product_id)
    return result

@router.get("/")
async def get_my_wishlist(
    current_user = Depends(get_current_user), 
    db = Depends(get_supabase_client)
):
    result = wishlist_service.get_user_wishlist(db, current_user.id)
    return result