from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from typing import List
from db import borrow_collection
from models import BorrowCreate, BorrowUpdate, BorrowResponse, BorrowStatus

router = APIRouter(prefix="/borrows", tags=["Borrows"])


def borrow_helper(borrow) -> dict:
    return {
        "id": str(borrow["_id"]),
        "book_id": borrow["book_id"],
        "member_id": borrow["member_id"],
        "borrow_date": borrow["borrow_date"],
        "due_date": borrow["due_date"],
        "return_date": borrow.get("return_date"),
        "status": borrow["status"]
    }


@router.get("/", response_model=List[BorrowResponse])
def get_all_borrows():
    borrows = []
    for borrow in borrow_collection.find():
        borrows.append(borrow_helper(borrow))
    return borrows


@router.get("/member/{member_id}", response_model=List[BorrowResponse])
def get_borrows_by_member(member_id: str):
    borrows = []
    for borrow in borrow_collection.find({"member_id": member_id}):
        borrows.append(borrow_helper(borrow))
    return borrows


@router.get("/book/{book_id}", response_model=List[BorrowResponse])
def get_borrows_by_book(book_id: str):
    borrows = []
    for borrow in borrow_collection.find({"book_id": book_id}):
        borrows.append(borrow_helper(borrow))
    return borrows


@router.get("/{borrow_id}", response_model=BorrowResponse)
def get_borrow(borrow_id: str):
    if not ObjectId.is_valid(borrow_id):
        raise HTTPException(status_code=400, detail="Invalid borrow ID")
    
    borrow = borrow_collection.find_one({"_id": ObjectId(borrow_id)})
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return borrow_helper(borrow)


@router.post("/", response_model=BorrowResponse)
def create_borrow(borrow: BorrowCreate):
    borrow_dict = borrow.model_dump()
    result = borrow_collection.insert_one(borrow_dict)
    
    new_borrow = borrow_collection.find_one({"_id": result.inserted_id})
    return borrow_helper(new_borrow)


@router.put("/{borrow_id}", response_model=BorrowResponse)
def update_borrow(borrow_id: str, borrow: BorrowUpdate):
    if not ObjectId.is_valid(borrow_id):
        raise HTTPException(status_code=400, detail="Invalid borrow ID")
    
    existing = borrow_collection.find_one({"_id": ObjectId(borrow_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    update_data = {k: v for k, v in borrow.model_dump().items() if v is not None}
    
    if update_data:
        borrow_collection.update_one(
            {"_id": ObjectId(borrow_id)},
            {"$set": update_data}
        )
    
    updated_borrow = borrow_collection.find_one({"_id": ObjectId(borrow_id)})
    return borrow_helper(updated_borrow)


@router.delete("/{borrow_id}")
def delete_borrow(borrow_id: str):
    if not ObjectId.is_valid(borrow_id):
        raise HTTPException(status_code=400, detail="Invalid borrow ID")
    
    result = borrow_collection.delete_one({"_id": ObjectId(borrow_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    return {"message": "Borrow record deleted successfully"}


@router.put("/{borrow_id}/return", response_model=BorrowResponse)
def return_book(borrow_id: str):
    if not ObjectId.is_valid(borrow_id):
        raise HTTPException(status_code=400, detail="Invalid borrow ID")
    
    existing = borrow_collection.find_one({"_id": ObjectId(borrow_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    if existing["status"] == BorrowStatus.RETURNED:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    borrow_collection.update_one(
        {"_id": ObjectId(borrow_id)},
        {"$set": {"status": BorrowStatus.RETURNED, "return_date": datetime.utcnow()}}
    )
    
    updated_borrow = borrow_collection.find_one({"_id": ObjectId(borrow_id)})
    return borrow_helper(updated_borrow)