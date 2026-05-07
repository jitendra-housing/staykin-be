from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.db.seeds.decision_statuses import (
    DECISION_ACCEPTED,
    DECISION_PENDING,
    DECISION_REJECTED,
)
from app.db.seeds.request_statuses import (
    REQUEST_STATUS_ACCEPTED,
    REQUEST_STATUS_IN_PROGRESS,
    REQUEST_STATUS_REJECTED,
    VALID_REQUEST_STATUS_IDS,
)
from app.db.seeds.request_target_kinds import TARGET_KIND_TEAM, TARGET_KIND_USER
from app.models.connection_request import ConnectionRequest, ConnectionRequestDecision
from app.models.room import Room, RoomParticipant
from app.models.team import Team, TeamMember
from app.models.user import User
from app.schemas.connection_request import (
    RequestCreate,
    RequestDecisionAction,
    RequestDecisionOut,
    RequestDetailOut,
    RequestOut,
)

router = APIRouter(prefix="/requests", tags=["requests"])


async def _request_or_404(db: AsyncSession, request_id: int) -> ConnectionRequest:
    req = await db.get(ConnectionRequest, request_id)
    if req is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="request not found")
    return req


async def _decisions(
    db: AsyncSession, request_id: int
) -> list[ConnectionRequestDecision]:
    result = await db.execute(
        select(ConnectionRequestDecision)
        .where(ConnectionRequestDecision.request_id == request_id)
        .order_by(ConnectionRequestDecision.user_id)
    )
    return list(result.scalars().all())


def _to_detail(
    req: ConnectionRequest, decisions: list[ConnectionRequestDecision]
) -> RequestDetailOut:
    return RequestDetailOut(
        **RequestOut.model_validate(req).model_dump(),
        decisions=[RequestDecisionOut.model_validate(d) for d in decisions],
    )


@router.post("", response_model=RequestDetailOut, status_code=status.HTTP_201_CREATED)
async def create_request(
    payload: RequestCreate, db: AsyncSession = Depends(get_db)
) -> RequestDetailOut:
    sender = await db.get(User, payload.from_user_id)
    if sender is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="from_user_id not found")

    target_user_id: int | None = None
    target_team_id: int | None = None
    decider_ids: list[int] = []

    if payload.target_kind == TARGET_KIND_USER:
        if payload.target_id == payload.from_user_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="cannot send request to yourself"
            )
        target = await db.get(User, payload.target_id)
        if target is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="target user not found")
        target_user_id = payload.target_id
        decider_ids = [payload.target_id]
    else:
        team = await db.get(Team, payload.target_id)
        if team is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="target team not found")
        target_team_id = payload.target_id

        members_res = await db.execute(
            select(TeamMember.user_id).where(TeamMember.team_id == payload.target_id)
        )
        member_ids = [uid for (uid,) in members_res.all()]
        if payload.from_user_id in member_ids:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="cannot send request to a team you are in",
            )
        if not member_ids:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="team has no members"
            )
        decider_ids = member_ids

    req = ConnectionRequest(
        from_user_id=payload.from_user_id,
        target_kind=payload.target_kind,
        target_user_id=target_user_id,
        target_team_id=target_team_id,
        status=REQUEST_STATUS_IN_PROGRESS,
    )
    db.add(req)
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="open request to this target already exists"
        ) from None

    for uid in decider_ids:
        db.add(
            ConnectionRequestDecision(
                request_id=req.id, user_id=uid, decision=DECISION_PENDING
            )
        )
    await db.commit()
    await db.refresh(req)

    decisions = await _decisions(db, req.id)
    return _to_detail(req, decisions)


def _validate_status_filter(v: int | None) -> int | None:
    if v is None:
        return v
    if v not in VALID_REQUEST_STATUS_IDS:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"unknown status id: {v}")
    return v


@router.get("/sent", response_model=list[RequestOut])
async def list_sent_requests(
    db: AsyncSession = Depends(get_db),
    user_id: int = Query(..., description="sender's user id"),
    status_filter: int | None = Query(default=None, alias="status"),
) -> list[ConnectionRequest]:
    status_filter = _validate_status_filter(status_filter)
    stmt = (
        select(ConnectionRequest)
        .where(ConnectionRequest.from_user_id == user_id)
        .order_by(ConnectionRequest.created_at.desc())
    )
    if status_filter is not None:
        stmt = stmt.where(ConnectionRequest.status == status_filter)

    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/received", response_model=list[RequestOut])
async def list_received_requests(
    db: AsyncSession = Depends(get_db),
    user_id: int = Query(..., description="recipient's user id"),
    status_filter: int | None = Query(default=None, alias="status"),
) -> list[ConnectionRequest]:
    status_filter = _validate_status_filter(status_filter)
    stmt = (
        select(ConnectionRequest)
        .join(
            ConnectionRequestDecision,
            ConnectionRequestDecision.request_id == ConnectionRequest.id,
        )
        .where(ConnectionRequestDecision.user_id == user_id)
        .order_by(ConnectionRequest.created_at.desc())
    )
    if status_filter is not None:
        stmt = stmt.where(ConnectionRequest.status == status_filter)

    result = await db.execute(stmt)
    return list(result.scalars().unique().all())


@router.get("/{request_id}", response_model=RequestDetailOut)
async def get_request(
    request_id: int, db: AsyncSession = Depends(get_db)
) -> RequestDetailOut:
    req = await _request_or_404(db, request_id)
    decisions = await _decisions(db, request_id)
    return _to_detail(req, decisions)


async def _record_decision(
    db: AsyncSession, request_id: int, user_id: int, decision: int
) -> RequestDetailOut:
    req = await _request_or_404(db, request_id)
    if req.status != REQUEST_STATUS_IN_PROGRESS:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="request is no longer open"
        )

    row = await db.get(
        ConnectionRequestDecision, {"request_id": request_id, "user_id": user_id}
    )
    if row is None:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="user is not a decider on this request"
        )
    if row.decision != DECISION_PENDING:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="decision already made")

    now = datetime.now(timezone.utc)
    row.decision = decision
    row.decided_at = now

    if decision == DECISION_REJECTED:
        req.status = REQUEST_STATUS_REJECTED
        req.decided_at = now
    else:
        pending_res = await db.execute(
            select(ConnectionRequestDecision).where(
                ConnectionRequestDecision.request_id == request_id,
                ConnectionRequestDecision.decision == DECISION_PENDING,
            )
        )
        if pending_res.scalars().first() is None:
            req.status = REQUEST_STATUS_ACCEPTED
            req.decided_at = now

            room = Room(request_id=request_id)
            db.add(room)
            await db.flush()

            participant_ids: set[int] = {req.from_user_id}
            if req.target_kind == TARGET_KIND_USER and req.target_user_id is not None:
                participant_ids.add(req.target_user_id)
            elif req.target_team_id is not None:
                members_res = await db.execute(
                    select(TeamMember.user_id).where(
                        TeamMember.team_id == req.target_team_id
                    )
                )
                participant_ids.update(uid for (uid,) in members_res.all())

            for uid in participant_ids:
                db.add(RoomParticipant(room_id=room.id, user_id=uid))

    await db.commit()
    await db.refresh(req)
    decisions = await _decisions(db, request_id)
    return _to_detail(req, decisions)


@router.post("/{request_id}/accept", response_model=RequestDetailOut)
async def accept_request(
    request_id: int,
    payload: RequestDecisionAction,
    db: AsyncSession = Depends(get_db),
) -> RequestDetailOut:
    return await _record_decision(db, request_id, payload.user_id, DECISION_ACCEPTED)


@router.post("/{request_id}/reject", response_model=RequestDetailOut)
async def reject_request(
    request_id: int,
    payload: RequestDecisionAction,
    db: AsyncSession = Depends(get_db),
) -> RequestDetailOut:
    return await _record_decision(db, request_id, payload.user_id, DECISION_REJECTED)
