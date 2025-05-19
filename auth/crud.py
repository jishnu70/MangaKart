from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth import models, utils
from auth.schemas import UserCreate

async def get_user_by_username(db: AsyncSession, username:str):
    result = await db.execute(select(models.User).filter_by(username=username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data: UserCreate):
    hashed_pw = utils.hash_password(user_data.password)
    user = models.User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_pw
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user