from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.database import init_db, close_db
from auth.routes import router as auth_router
from manga.routes import router as manga_router
from cart.routes import router as cart_router
from order.routes import router as order_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Close database
    await close_db()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(manga_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.get("/root")
async def home_page():
    return {"message": "Backend is online"}