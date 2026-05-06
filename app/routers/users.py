from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, UserUpsert

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut)
async def upsert_user(payload: UserUpsert, db: AsyncSession = Depends(get_db)) -> User:
    """Create-or-update by phone. Phone is the identity."""
    result = await db.execute(select(User).where(User.phone == payload.phone))
    user = result.scalar_one_or_none()

    data = payload.model_dump(exclude_unset=True)
    if user is None:
        user = User(**data)
        db.add(user)
    else:
        for key, value in data.items():
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.get("/{phone}", response_model=UserOut)
async def get_user_by_phone(phone: str, db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)
) -> User:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user
