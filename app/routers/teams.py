from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.team import Team, TeamMember
from app.models.user import User
from app.schemas.team import (
    TeamCreate,
    TeamDetailOut,
    TeamMemberAdd,
    TeamMemberOut,
    TeamOut,
)

router = APIRouter(prefix="/teams", tags=["teams"])


async def _team_or_404(db: AsyncSession, team_id: int) -> Team:
    team = await db.get(Team, team_id)
    if team is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="team not found")
    return team


async def _members(db: AsyncSession, team_id: int) -> list[TeamMember]:
    result = await db.execute(
        select(TeamMember).where(TeamMember.team_id == team_id).order_by(TeamMember.joined_at)
    )
    return list(result.scalars().all())


@router.post("", response_model=TeamDetailOut, status_code=status.HTTP_201_CREATED)
async def create_team(payload: TeamCreate, db: AsyncSession = Depends(get_db)) -> TeamDetailOut:
    owner = await db.get(User, payload.owner_user_id)
    if owner is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="owner_user_id not found")

    team = Team(owner_user_id=payload.owner_user_id, name=payload.name)
    db.add(team)
    await db.flush()
    db.add(TeamMember(team_id=team.id, user_id=payload.owner_user_id))
    await db.commit()
    await db.refresh(team)

    members = await _members(db, team.id)
    return TeamDetailOut(
        **TeamOut.model_validate(team).model_dump(),
        members=[TeamMemberOut.model_validate(m) for m in members],
    )


@router.get("/{team_id}", response_model=TeamDetailOut)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)) -> TeamDetailOut:
    team = await _team_or_404(db, team_id)
    members = await _members(db, team_id)
    return TeamDetailOut(
        **TeamOut.model_validate(team).model_dump(),
        members=[TeamMemberOut.model_validate(m) for m in members],
    )


@router.get("/by-owner/{user_id}", response_model=list[TeamOut])
async def list_teams_by_owner(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> list[Team]:
    result = await db.execute(
        select(Team).where(Team.owner_user_id == user_id).order_by(Team.created_at.desc())
    )
    return list(result.scalars().all())


@router.post(
    "/{team_id}/members", response_model=TeamMemberOut, status_code=status.HTTP_201_CREATED
)
async def add_team_member(
    team_id: int, payload: TeamMemberAdd, db: AsyncSession = Depends(get_db)
) -> TeamMember:
    await _team_or_404(db, team_id)
    user = await db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="user_id not found")

    member = TeamMember(team_id=team_id, user_id=payload.user_id)
    db.add(member)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, detail="user already in team") from None
    return member


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team_member(
    team_id: int, user_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    team = await _team_or_404(db, team_id)
    if user_id == team.owner_user_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="cannot remove team owner"
        )

    member = await db.get(TeamMember, {"team_id": team_id, "user_id": user_id})
    if member is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="member not found")
    await db.delete(member)
    await db.commit()
