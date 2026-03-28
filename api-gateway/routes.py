import os
import httpx
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# ── Service URLs from .env ────────────────────────────────
BOOK_SERVICE        = os.getenv("BOOK_SERVICE")
MEMBER_SERVICE      = os.getenv("MEMBER_SERVICE")
BORROW_SERVICE      = os.getenv("BORROW_SERVICE")
REVIEW_SERVICE      = os.getenv("REVIEW_SERVICE")
STAFF_SERVICE       = os.getenv("STAFF_SERVICE")
RESERVATION_SERVICE = os.getenv("RESERVATION_SERVICE")

# ── Reusable async forward helper ────────────────────────
async def forward(request: Request, url: str, **kwargs):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                headers={k: v for k, v in request.headers.items() if k != "host"},
                **kwargs
            )
            return JSONResponse(status_code=resp.status_code, content=resp.json())
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {url}")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail=f"Service timed out: {url}")


# ── BOOK SERVICE ──────────────────────────────────────────
@router.get("/books")
async def get_books(request: Request):
    return await forward(request, f"{BOOK_SERVICE}/books")

@router.post("/books")
async def create_book(request: Request):
    return await forward(request, f"{BOOK_SERVICE}/books", json=await request.json())

@router.put("/books/{book_id}")
async def update_book(request: Request, book_id: str):
    return await forward(request, f"{BOOK_SERVICE}/books/{book_id}", json=await request.json())

@router.delete("/books/{book_id}")
async def delete_book(request: Request, book_id: str):
    return await forward(request, f"{BOOK_SERVICE}/books/{book_id}")


# ── MEMBER SERVICE ────────────────────────────────────────
@router.get("/members")
async def get_members(request: Request):
    return await forward(request, f"{MEMBER_SERVICE}/members")

@router.post("/members")
async def create_member(request: Request):
    return await forward(request, f"{MEMBER_SERVICE}/members", json=await request.json())

@router.put("/members/{member_id}")
async def update_member(request: Request, member_id: str):
    return await forward(request, f"{MEMBER_SERVICE}/members/{member_id}", json=await request.json())

@router.delete("/members/{member_id}")
async def delete_member(request: Request, member_id: str):
    return await forward(request, f"{MEMBER_SERVICE}/members/{member_id}")


# ── BORROW SERVICE ────────────────────────────────────────
@router.get("/borrows")
async def get_borrows(request: Request):
    return await forward(request, f"{BORROW_SERVICE}/borrows")

@router.post("/borrows")
async def create_borrow(request: Request):
    return await forward(request, f"{BORROW_SERVICE}/borrows", json=await request.json())

@router.put("/borrows/{borrow_id}")
async def update_borrow(request: Request, borrow_id: str):
    return await forward(request, f"{BORROW_SERVICE}/borrows/{borrow_id}", json=await request.json())

@router.delete("/borrows/{borrow_id}")
async def delete_borrow(request: Request, borrow_id: str):
    return await forward(request, f"{BORROW_SERVICE}/borrows/{borrow_id}")


# ── REVIEW SERVICE ────────────────────────────────────────
@router.get("/reviews")
async def get_reviews(request: Request):
    return await forward(request, f"{REVIEW_SERVICE}/reviews")

@router.post("/reviews")
async def create_review(request: Request):
    return await forward(request, f"{REVIEW_SERVICE}/reviews", json=await request.json())

@router.put("/reviews/{review_id}")
async def update_review(request: Request, review_id: str):
    return await forward(request, f"{REVIEW_SERVICE}/reviews/{review_id}", json=await request.json())

@router.delete("/reviews/{review_id}")
async def delete_review(request: Request, review_id: str):
    return await forward(request, f"{REVIEW_SERVICE}/reviews/{review_id}")


# ── STAFF SERVICE ─────────────────────────────────────────
@router.get("/staff")
async def get_staff(request: Request):
    return await forward(request, f"{STAFF_SERVICE}/staff")

@router.post("/staff")
async def create_staff(request: Request):
    return await forward(request, f"{STAFF_SERVICE}/staff", json=await request.json())

@router.put("/staff/{staff_id}")
async def update_staff(request: Request, staff_id: str):
    return await forward(request, f"{STAFF_SERVICE}/staff/{staff_id}", json=await request.json())

@router.delete("/staff/{staff_id}")
async def delete_staff(request: Request, staff_id: str):
    return await forward(request, f"{STAFF_SERVICE}/staff/{staff_id}")


# ── RESERVATION SERVICE ───────────────────────────────────
@router.get("/reservations")
async def get_reservations(request: Request):
    return await forward(request, f"{RESERVATION_SERVICE}/reservations/")

@router.post("/reservations")
async def create_reservation(request: Request):
    return await forward(request, f"{RESERVATION_SERVICE}/reservations/", json=await request.json())

@router.get("/reservations/{reservation_id}")          # ← was missing
async def get_reservation(request: Request, reservation_id: str):
    return await forward(request, f"{RESERVATION_SERVICE}/reservations/{reservation_id}")

@router.patch("/reservations/{reservation_id}/cancel") # ← was missing
async def cancel_reservation(request: Request, reservation_id: str):
    return await forward(request, f"{RESERVATION_SERVICE}/reservations/{reservation_id}/cancel")

@router.delete("/reservations/{reservation_id}")
async def delete_reservation(request: Request, reservation_id: str):
    return await forward(request, f"{RESERVATION_SERVICE}/reservations/{reservation_id}")