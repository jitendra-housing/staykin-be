from pydantic import BaseModel


class LifestyleTagOut(BaseModel):
    id: int
    value: str   # the enum-style key, e.g. "LATE_NIGHTS"
    label: str   # display label, e.g. "Late nights"
