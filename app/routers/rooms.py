from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.db.seeds.request_target_kinds import TARGET_KIND_USER
from app.models.connection_request import ConnectionRequest
from app.models.room import Room, RoomParticipant
from app.models.team import Team, TeamMember
from app.schemas.room import (
    AddFlatmateAction,
    RoomDetailOut,
    RoomOut,
    RoomParticipantOut,
)
from app.schemas.team import TeamDetailOut, TeamMemberOut, TeamOut

router = APIRouter(prefix="/rooms", tags=["rooms"])


async def _participants(db: AsyncSession, room_id: int) -> list[RoomParticipant]:
    result = await db.execute(
        select(RoomParticipant)
        .where(RoomParticipant.room_id == room_id)
        .order_by(RoomParticipant.joined_at)
    )
    return list(result.scalars().all())


def _flag(viewer_id: int, sender_id: int, flatmate_team_id: int | None) -> bool:
    return viewer_id != sender_id and flatmate_team_id is None


def _room_out(room: Room, sender_id: int, viewer_id: int) -> RoomOut:
    return RoomOut(
        id=room.id,
        request_id=room.request_id,
        flatmate_team_id=room.flatmate_team_id,
        add_flatmate_enabled=_flag(viewer_id, sender_id, room.flatmate_team_id),
        created_at=room.created_at,
    )


@router.get("", response_model=list[RoomOut])
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    user_id: int = Query(..., description="user whose rooms to list"),
) -> list[RoomOut]:
    stmt = (
        select(Room, ConnectionRequest.from_user_id)
        .join(RoomParticipant, RoomParticipant.room_id == Room.id)
        .join(ConnectionRequest, ConnectionRequest.id == Room.request_id)
        .where(RoomParticipant.user_id == user_id)
        .order_by(Room.created_at.desc())
    )
    result = await db.execute(stmt)
    return [_room_out(room, sender_id, user_id) for room, sender_id in result.unique().all()]


@router.get("/{room_id}", response_model=RoomDetailOut)
async def get_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Query(..., description="viewing user's id"),
) -> RoomDetailOut:
    room = await db.get(Room, room_id)
    if room is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="room not found")

    is_participant = await db.get(RoomParticipant, {"room_id": room_id, "user_id": user_id})
    if is_participant is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="not a participant")

    req = await db.get(ConnectionRequest, room.request_id)
    assert req is not None

    participants = await _participants(db, room_id)
    return RoomDetailOut(
        **_room_out(room, req.from_user_id, user_id).model_dump(),
        participants=[RoomParticipantOut.model_validate(p) for p in participants],
    )


@router.post("/{room_id}/add-flatmate", response_model=TeamDetailOut)
async def add_flatmate(
    room_id: int,
    payload: AddFlatmateAction,
    db: AsyncSession = Depends(get_db),
) -> TeamDetailOut:
    room = await db.get(Room, room_id)
    if room is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="room not found")

    is_participant = await db.get(
        RoomParticipant, {"room_id": room_id, "user_id": payload.user_id}
    )
    if is_participant is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="not a participant")

    req = await db.get(ConnectionRequest, room.request_id)
    assert req is not None
    if payload.user_id == req.from_user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="sender cannot add themselves as flatmate"
        )

    if room.flatmate_team_id is not None:
        team = await db.get(Team, room.flatmate_team_id)
        assert team is not None
        members = await _team_members(db, team.id)
        return TeamDetailOut(
            **TeamOut.model_validate(team).model_dump(),
            members=[TeamMemberOut.model_validate(m) for m in members],
        )

    candidate_id = req.from_user_id

    if req.target_kind == TARGET_KIND_USER:
        team = Team(owner_user_id=payload.user_id, name=None)
        db.add(team)
        await db.flush()
        db.add(TeamMember(team_id=team.id, user_id=payload.user_id))
        db.add(TeamMember(team_id=team.id, user_id=candidate_id))
    else:
        assert req.target_team_id is not None
        team = await db.get(Team, req.target_team_id)
        if team is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="target team no longer exists"
            )

        adder_in_team = await db.get(
            TeamMember, {"team_id": team.id, "user_id": payload.user_id}
        )
        if adder_in_team is None:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, detail="adder is no longer in the team"
            )

        existing = await db.get(
            TeamMember, {"team_id": team.id, "user_id": candidate_id}
        )
        if existing is None:
            db.add(TeamMember(team_id=team.id, user_id=candidate_id))

    room.flatmate_team_id = team.id

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="conflict adding flatmate"
        ) from None

    await db.refresh(team)
    members = await _team_members(db, team.id)
    return TeamDetailOut(
        **TeamOut.model_validate(team).model_dump(),
        members=[TeamMemberOut.model_validate(m) for m in members],
    )


async def _team_members(db: AsyncSession, team_id: int) -> list[TeamMember]:
    result = await db.execute(
        select(TeamMember).where(TeamMember.team_id == team_id).order_by(TeamMember.joined_at)
    )
    return list(result.scalars().all())
