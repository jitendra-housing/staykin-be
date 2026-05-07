from typing import Literal

from pydantic import BaseModel

from app.schemas.team import TeamOut
from app.schemas.user import UserOut


class FlatmateTeamItem(BaseModel):
    type: Literal["team"] = "team"
    team: TeamOut
    members: list[UserOut]


class FlatmateUserItem(BaseModel):
    type: Literal["user"] = "user"
    user: UserOut


FlatmateItem = FlatmateTeamItem | FlatmateUserItem
