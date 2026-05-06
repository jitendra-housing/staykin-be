from fastapi import APIRouter

from app.db.seeds.lifestyle_tags import LIFESTYLE_TAGS
from app.schemas.lifestyle_tag import LifestyleTagOut

router = APIRouter(prefix="/lifestyle-tags", tags=["lifestyle-tags"])


@router.get("", response_model=list[LifestyleTagOut])
def list_lifestyle_tags() -> list[LifestyleTagOut]:
    return [LifestyleTagOut(id=tid, value=key, label=label) for tid, key, label in LIFESTYLE_TAGS]
