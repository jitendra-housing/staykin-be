from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.listing import Listing
from app.models.user import User
from app.schemas.listing import ListingCreate, ListingOut, ListingUpdate

router = APIRouter(prefix="/listings", tags=["listings"])


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


@router.get("", response_model=list[ListingOut])
async def list_listings(
    db: AsyncSession = Depends(get_db),
    locality_id: int | None = Query(default=None),
    bhk: int | None = Query(default=None),
    max_rent: int | None = Query(default=None, ge=0),
    gender_pref: int | None = Query(default=None),
    move_in: int | None = Query(default=None),
) -> list[Listing]:
    stmt = select(Listing).order_by(Listing.created_at.desc())
    if locality_id is not None:
        stmt = stmt.where(Listing.locality_id == locality_id)
    if bhk is not None:
        stmt = stmt.where(Listing.bhk == bhk)
    if max_rent is not None:
        stmt = stmt.where(Listing.monthly_rent <= max_rent)
    if gender_pref is not None:
        stmt = stmt.where(Listing.gender_pref == gender_pref)
    if move_in is not None:
        stmt = stmt.where(Listing.move_in == move_in)

    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{listing_id}", response_model=ListingOut)
async def get_listing(listing_id: int, db: AsyncSession = Depends(get_db)) -> Listing:
    listing = await db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="listing not found")
    return listing


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
