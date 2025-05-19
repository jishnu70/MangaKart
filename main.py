from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db

app = FastAPI()

@app.get("/root")
def home_page():
    return {"message": "Backend is online"}

@app.get("/manga")
async def get_volumne_info(db: AsyncSession = Depends(get_db)):
    return