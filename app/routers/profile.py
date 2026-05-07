from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.core.db import get_db
from app.core.vibe import vibe_score
from app.models.listing import Listing
from app.models.team import TeamMember
from app.models.user import User
from app.schemas.user import PhoneLookupOut, UserOut, UserUpdate, UserUpsert

router = APIRouter(prefix="/profile", tags=["profile"])


async def _user_out(
    db: AsyncSession, user: User, viewer: User | None = None
) -> UserOut:
    listings_res = await db.execute(
        select(Listing.id)
        .where(Listing.owner_user_id == user.id)
        .order_by(Listing.created_at.desc())
    )
    listing_ids = [lid for (lid,) in listings_res.all()]

    tm_self = aliased(TeamMember)
    tm_other = aliased(TeamMember)
    teammates_res = await db.execute(
        select(tm_other.user_id)
        .join(tm_self, tm_self.team_id == tm_other.team_id)
        .where(tm_self.user_id == user.id, tm_other.user_id != user.id)
        .distinct()
    )
    team_member_ids = [uid for (uid,) in teammates_res.all()]

    score = (
        vibe_score(viewer.lifestyle_tag_ids, user.lifestyle_tag_ids)
        if viewer is not None and viewer.id != user.id
        else None
    )

    return UserOut.model_validate(user).model_copy(
        update={
            "listing_ids": listing_ids,
            "team_member_ids": team_member_ids,
            "vibe_score": score,
        }
    )


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


@router.get("/by-phone/{phone}", response_model=PhoneLookupOut)
async def get_profile_by_phone(
    phone: str, db: AsyncSession = Depends(get_db)
) -> PhoneLookupOut:
    """Lookup a user_id by phone. Returns user_id=-1 if no user with that phone."""
    result = await db.execute(select(User.id).where(User.phone == phone))
    row = result.scalar_one_or_none()
    return PhoneLookupOut(user_id=row if row is not None else -1)


@router.get("/{user_id}", response_model=UserOut)
async def get_profile(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    viewer_id: int | None = Query(
        None,
        description=(
            "Logged-in user id of whoever is viewing this profile. "
            "REQUIRED to populate `vibe_score`; without it, `vibe_score` is null. "
            "When viewing your own profile (viewer_id == user_id), `vibe_score` "
            "is also null by design."
        ),
    ),
) -> UserOut:
    """Fetch a user's profile.

    The response includes a `vibe_score` (0-100 lifestyle compatibility
    between the viewer and this profile owner) only when:
      - `viewer_id` is provided in the query string, AND
      - `viewer_id` is different from `user_id` (i.e. not your own profile), AND
      - both users have at least one lifestyle tag selected.

    Otherwise `vibe_score` is null.
    """
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="profile not found")
    viewer = await db.get(User, viewer_id) if viewer_id is not None else None
    return await _user_out(db, user, viewer)


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
