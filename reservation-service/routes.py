from fastapi import APIRouter, HTTPException, status
from db import get_database
from models import ReservationCreate, ReservationOut, ReservationUpdate
from bson import ObjectId
import crud

router = APIRouter(prefix="/reservations", tags=["Reservations"])

# ── Convert ObjectId → string ──────────────────────────────
def serialize(doc: dict) -> dict:
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
async def get_all_reservations():
    db = get_database()
    results = await crud.get_all_reservations(db)
    return [serialize(doc) for doc in results]  # ← serialize each doc

@router.put("/{reservation_id}")
async def update_reservation(reservation_id: str, payload: ReservationUpdate):
    db = get_database()
    result = await crud.update_reservation(db, reservation_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return serialize(result)

@router.get("/{reservation_id}")
async def get_reservation(reservation_id: str):
    db = get_database()
    reservation = await crud.get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return serialize(reservation)   # ← serialize before returning

@router.patch("/{reservation_id}/cancel")
async def cancel_reservation(reservation_id: str):
    db = get_database()
    result = await crud.cancel_reservation(db, reservation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return serialize(result)        # ← serialize before returning