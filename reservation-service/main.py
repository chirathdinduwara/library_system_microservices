from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← add this
from fastapi.responses import Response
from db import connect_db, close_db
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(title="Reservation Service", version="1.0.0", lifespan=lifespan)

# ── CORS — needed so api-gateway can talk to this service ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080"],  # your gateway URL
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

# ── Root & favicon ─────────────────────────────────────────
@app.get("/")
async def root():
    return {"service": "Reservation Service", "status": "running"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)