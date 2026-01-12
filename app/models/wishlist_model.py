from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class WishlistBase(BaseModel):
    product_id: int

class WishlistResponse(WishlistBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    product_details: Optional[dict] = None
    user_details: Optional[Any] = None

    class Config:
        from_attributes = True