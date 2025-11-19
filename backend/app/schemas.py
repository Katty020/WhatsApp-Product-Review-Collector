from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReviewOut(BaseModel):
    id: UUID
    contact_number: str
    user_name: str
    product_name: str
    product_review: str
    created_at: datetime

    class Config:
        from_attributes = True

