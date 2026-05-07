from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.listing import Listing
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, UserUpsert

router = APIRouter(prefix="/profile", tags=["profile"])


async def _user_out(db: AsyncSession, user: User) -> UserOut:
    result = await db.execute(
        select(Listing.id)
        .where(Listing.owner_user_id == user.id)
        .order_by(Listing.created_at.desc())
    )
    listing_ids = [lid for (lid,) in result.all()]
    return UserOut.model_validate(user).model_copy(update={"listing_ids": listing_ids})


@router.post("", response_model=UserOut)
async def upsert_profile(payload: UserUpsert, db: AsyncSession = Depends(get_db)) -> UserOut:
    """Create-or-update profile by phone. Phone is the identity."""
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
    return await _user_out(db, user)


@router.get("/{user_id}", response_model=UserOut)
async def get_profile(user_id: int, db: AsyncSession = Depends(get_db)) -> UserOut:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="profile not found")
    return await _user_out(db, user)


@router.patch("/{user_id}", response_model=UserOut)
async def update_profile(
    user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)
) -> UserOut:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="profile not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return await _user_out(db, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(user_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """Delete a user and every row related to them.

    All FKs to users.id are ON DELETE CASCADE, so deleting the user row
    cascades to: listings, teams (owned), team_members, requests
    (sent and targeting them), request_decisions, room_participants. Teams
    cascade further to their team_members and any requests targeting them;
    requests cascade to request_decisions and rooms; rooms cascade to
    room_participants. ImageKit photos are NOT removed (orphaned).
    """
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="profile not found")
    await db.delete(user)
    await db.commit()
