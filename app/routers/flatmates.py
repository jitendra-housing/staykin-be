from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.team import Team, TeamMember
from app.models.user import User
from app.schemas.flatmate import FlatmateItem, FlatmateTeamItem, FlatmateUserItem
from app.schemas.team import TeamOut
from app.schemas.user import UserOut

router = APIRouter(prefix="/flatmates", tags=["flatmates"])


def _set_match(a: list[int] | None, b: list[int] | None) -> bool:
    """A wildcard if either side has no preference, else require intersection."""
    sa, sb = frozenset(a or ()), frozenset(b or ())
    if not sa or not sb:
        return True
    return bool(sa & sb)


def _scalar_match(a: object, b: object) -> bool:
    """A wildcard if either side is None, else require equality."""
    if a is None or b is None:
        return True
    return a == b


def _budget_match(a: User, b: User) -> bool:
    """A wildcard if either side has no full range, else require overlap."""
    if (
        a.budget_min is None
        or a.budget_max is None
        or b.budget_min is None
        or b.budget_max is None
    ):
        return True
    return a.budget_min <= b.budget_max and a.budget_max >= b.budget_min


def _prefs_match(a: User, b: User) -> bool:
    return (
        _set_match(a.preferred_locality_ids, b.preferred_locality_ids)
        and _set_match(a.bhk_prefs, b.bhk_prefs)
        and _set_match(a.furnishing_prefs, b.furnishing_prefs)
        and _budget_match(a, b)
        and _scalar_match(a.room_type_pref, b.room_type_pref)
        and _scalar_match(a.move_in_pref, b.move_in_pref)
        and _scalar_match(a.move_in_date, b.move_in_date)
        and _scalar_match(a.gender_pref, b.gender_pref)
    )


@router.get("/{user_id}", response_model=list[FlatmateItem])
async def list_flatmates(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> list[FlatmateItem]:
    """Return matching flatmates grouped by team.

    Users whose search preferences exactly match the requester's are
    collected, then any matched user that belongs to a team is folded
    into a single team item (with all team members). Remaining matches
    are returned as solo user items. The requester is excluded.
    """
    requester = await db.get(User, user_id)
    if requester is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")

    candidates = (
        await db.execute(select(User).where(User.id != user_id))
    ).scalars().all()
    matches = [u for u in candidates if _prefs_match(requester, u)]
    if not matches:
        return []

    match_ids = [u.id for u in matches]

    # First team (by joined_at) per matched user.
    team_rows = (
        await db.execute(
            select(TeamMember.user_id, Team)
            .join(Team, Team.id == TeamMember.team_id)
            .where(TeamMember.user_id.in_(match_ids))
            .order_by(TeamMember.user_id, TeamMember.joined_at)
        )
    ).all()
    team_by_user: dict[int, Team] = {}
    for uid, team in team_rows:
        team_by_user.setdefault(uid, team)

    # Load full member lists for each team that any match belongs to.
    team_ids = {t.id for t in team_by_user.values()}
    members_by_team: dict[int, list[User]] = {tid: [] for tid in team_ids}
    if team_ids:
        member_rows = (
            await db.execute(
                select(TeamMember.team_id, User)
                .join(User, User.id == TeamMember.user_id)
                .where(TeamMember.team_id.in_(team_ids))
                .order_by(TeamMember.team_id, TeamMember.joined_at)
            )
        ).all()
        for tid, user in member_rows:
            members_by_team[tid].append(user)

    items: list[FlatmateItem] = []
    seen_teams: set[int] = set()
    for u in matches:
        team = team_by_user.get(u.id)
        # Treat legacy single-member teams as solo to keep the response invariant
        # (team items always carry >=2 members).
        if team is None or len(members_by_team.get(team.id, [])) < 2:
            items.append(FlatmateUserItem(user=UserOut.model_validate(u)))
            continue
        if team.id in seen_teams:
            continue
        seen_teams.add(team.id)
        items.append(
            FlatmateTeamItem(
                team=TeamOut.model_validate(team),
                members=[UserOut.model_validate(m) for m in members_by_team[team.id]],
            )
        )
    return items
