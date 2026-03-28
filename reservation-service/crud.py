from motor.motor_asyncio import AsyncIOMotorDatabase
from models import ReservationCreate, ReservationStatus, ReservationUpdate
from datetime import datetime, timezone
from bson import ObjectId

COLLECTION = "reservations"

async def create_reservation(db: AsyncIOMotorDatabase, payload: ReservationCreate):
    doc = {
        **payload.model_dump(),
        "status": ReservationStatus.PENDING,
        "created_at": datetime.now(timezone.utc)
    }
    result = await db[COLLECTION].insert_one(doc)
    return await db[COLLECTION].find_one({"_id": result.inserted_id})

async def get_reservation(db: AsyncIOMotorDatabase, reservation_id: str):
    return await db[COLLECTION].find_one({"_id": ObjectId(reservation_id)})

async def cancel_reservation(db: AsyncIOMotorDatabase, reservation_id: str):
    await db[COLLECTION].update_one(
        {"_id": ObjectId(reservation_id)},
        {"$set": {"status": ReservationStatus.CANCELLED}}
    )
    return await get_reservation(db, reservation_id)

async def get_all_reservations(db: AsyncIOMotorDatabase):
    cursor = db[COLLECTION].find()
    return [doc async for doc in cursor]

async def update_reservation(db: AsyncIOMotorDatabase, reservation_id: str, payload: ReservationUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        return await get_reservation(db, reservation_id)  # nothing to update
    await db[COLLECTION].update_one(
        {"_id": ObjectId(reservation_id)},
        {"$set": update_data}
    )
    return await get_reservation(db, reservation_id)