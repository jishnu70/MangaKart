from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from auth import schemas, crud, utils
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=schemas.UserOut)
async def register_user(user:schemas.UserCreate, db:AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    return await crud.create_user(db, user)

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db:AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_username(db, form_data.username)
    if not db_user or not utils.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = utils.create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}