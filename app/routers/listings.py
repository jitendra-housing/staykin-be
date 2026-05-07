from collections.abc import Iterable

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.core.db import get_db
from app.db.seeds.genders import GENDER_FEMALE, GENDER_MALE, GENDER_OTHER
from app.db.seeds.listing_gender_prefs import (
    LISTING_GENDER_PREF_BOYS_ONLY,
    LISTING_GENDER_PREF_GIRLS_ONLY,
    LISTING_GENDER_PREF_MIXED,
)
from app.db.seeds.room_types import ROOM_TYPE_EITHER
from app.models.listing import Listing
from app.models.team import TeamMember
from app.models.user import User
from app.schemas.listing import ListingCreate, ListingFeedOut, ListingOut, ListingUpdate

router = APIRouter(prefix="/listings", tags=["listings"])


async def _residents_count_map(
    db: AsyncSession, owner_ids: Iterable[int]
) -> dict[int, int]:
    ids = list(set(owner_ids))
    if not ids:
        return {}
    tm_self = aliased(TeamMember)
    tm_other = aliased(TeamMember)
    rows = await db.execute(
        select(tm_self.user_id, func.count(distinct(tm_other.user_id)))
        .select_from(tm_self)
        .join(tm_other, tm_other.team_id == tm_self.team_id)
        .where(tm_self.user_id.in_(ids))
        .group_by(tm_self.user_id)
    )
    return {uid: cnt for uid, cnt in rows.all()}


def _with_residents(listing: Listing, count_map: dict[int, int]) -> ListingFeedOut:
    n = max(1, count_map.get(listing.owner_user_id, 0))
    base = ListingOut.model_validate(listing).model_dump()
    return ListingFeedOut(**base, total_residents=n)


@router.post("", response_model=ListingOut, status_code=status.HTTP_201_CREATED)
async def create_listing(
    payload: ListingCreate, db: AsyncSession = Depends(get_db)
) -> Listing:
    owner = await db.get(User, payload.owner_user_id)
    if owner is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="owner_user_id not found")

    listing = Listing(**payload.model_dump())
    db.add(listing)
    await db.commit()
    await db.refresh(listing)
    return listing


@router.get("", response_model=list[ListingFeedOut])
async def list_listings(
    db: AsyncSession = Depends(get_db),
    user_id: int = Query(..., description="viewing user's id; filters from their profile prefs"),
) -> list[ListingFeedOut]:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")

    stmt = select(Listing).where(Listing.owner_user_id != user_id)

    if user.preferred_locality_ids:
        stmt = stmt.where(Listing.locality_id.in_(user.preferred_locality_ids))
    if user.bhk_prefs:
        stmt = stmt.where(Listing.bhk.in_(user.bhk_prefs))
    if user.budget_max is not None:
        stmt = stmt.where(Listing.monthly_rent <= user.budget_max)
    if user.furnishing_prefs:
        stmt = stmt.where(Listing.furnishing.in_(user.furnishing_prefs))
    if user.move_in_pref is not None:
        stmt = stmt.where(Listing.move_in <= user.move_in_pref)
    if user.room_type_pref is not None and user.room_type_pref != ROOM_TYPE_EITHER:
        stmt = stmt.where(Listing.room_type.in_([user.room_type_pref, ROOM_TYPE_EITHER]))
    if user.gender == GENDER_MALE:
        stmt = stmt.where(
            Listing.gender_pref.in_([LISTING_GENDER_PREF_BOYS_ONLY, LISTING_GENDER_PREF_MIXED])
        )
    elif user.gender == GENDER_FEMALE:
        stmt = stmt.where(
            Listing.gender_pref.in_([LISTING_GENDER_PREF_GIRLS_ONLY, LISTING_GENDER_PREF_MIXED])
        )
    elif user.gender == GENDER_OTHER:
        stmt = stmt.where(Listing.gender_pref == LISTING_GENDER_PREF_MIXED)

    stmt = stmt.order_by(Listing.created_at.desc())
    result = await db.execute(stmt)
    listings = list(result.scalars().all())
    counts = await _residents_count_map(db, (l.owner_user_id for l in listings))
    return [_with_residents(l, counts) for l in listings]


@router.get("/{listing_id}", response_model=ListingFeedOut)
async def get_listing(
    listing_id: int, db: AsyncSession = Depends(get_db)
) -> ListingFeedOut:
    listing = await db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="listing not found")
    counts = await _residents_count_map(db, [listing.owner_user_id])
    return _with_residents(listing, counts)


@router.patch("/{listing_id}", response_model=ListingOut)
async def update_listing(
    listing_id: int, payload: ListingUpdate, db: AsyncSession = Depends(get_db)
) -> Listing:
    listing = await db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="listing not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(listing, key, value)

    await db.commit()
    await db.refresh(listing)
    return listing


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(listing_id: int, db: AsyncSession = Depends(get_db)) -> None:
    listing = await db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="listing not found")
    await db.delete(listing)
    await db.commit()
