from pydantic import BaseModel


class OccupationOut(BaseModel):
    id: int
    name: str
