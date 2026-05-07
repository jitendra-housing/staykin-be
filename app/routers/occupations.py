from fastapi import APIRouter

from app.db.seeds.occupations import OCCUPATIONS
from app.schemas.occupation import OccupationOut

router = APIRouter(prefix="/occupations", tags=["occupations"])


@router.get("", response_model=list[OccupationOut])
def list_occupations() -> list[OccupationOut]:
    return [OccupationOut(id=oid, name=name) for oid, name in OCCUPATIONS]
