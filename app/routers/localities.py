from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.locality import Locality
from app.schemas.locality import LocalityOut

router = APIRouter(prefix="/localities", tags=["localities"])


@router.get("", response_model=list[LocalityOut])
async def list_localities(db: AsyncSession = Depends(get_db)) -> list[Locality]:
    result = await db.execute(select(Locality).order_by(Locality.id))
    return list(result.scalars().all())
