from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.room import Room, RoomParticipant
from app.schemas.room import RoomDetailOut, RoomOut, RoomParticipantOut

router = APIRouter(prefix="/rooms", tags=["rooms"])


async def _participants(db: AsyncSession, room_id: int) -> list[RoomParticipant]:
    result = await db.execute(
        select(RoomParticipant)
        .where(RoomParticipant.room_id == room_id)
        .order_by(RoomParticipant.joined_at)
    )
    return list(result.scalars().all())


@router.get("", response_model=list[RoomOut])
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    user_id: int = Query(..., description="user whose rooms to list"),
) -> list[Room]:
    stmt = (
        select(Room)
        .join(RoomParticipant, RoomParticipant.room_id == Room.id)
        .where(RoomParticipant.user_id == user_id)
        .order_by(Room.created_at.desc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().unique().all())


@router.get("/{room_id}", response_model=RoomDetailOut)
async def get_room(room_id: int, db: AsyncSession = Depends(get_db)) -> RoomDetailOut:
    room = await db.get(Room, room_id)
    if room is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="room not found")
    participants = await _participants(db, room_id)
    return RoomDetailOut(
        **RoomOut.model_validate(room).model_dump(),
        participants=[RoomParticipantOut.model_validate(p) for p in participants],
    )
