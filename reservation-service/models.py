from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
from datetime import datetime

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class ReservationCreate(BaseModel):
    user_id: str
    book_id: str

class ReservationUpdate(BaseModel):
    status: Optional[ReservationStatus] = None

class ReservationOut(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    book_id: str
    status: ReservationStatus
    created_at: datetime

    # ── Convert ObjectId → str automatically ──────────────
    @field_validator("id", mode="before")
    @classmethod
    def convert_objectid(cls, v):
        return str(v)   # handles ObjectId, str, anything

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }