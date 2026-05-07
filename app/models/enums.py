import enum


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class BHK(str, enum.Enum):
    STUDIO = "STUDIO"
    ONE_BHK = "ONE_BHK"
    TWO_BHK = "TWO_BHK"
    THREE_BHK = "THREE_BHK"
    FOUR_BHK = "FOUR_BHK"
    FIVE_BHK = "FIVE_BHK"


class RoomType(str, enum.Enum):
    SINGLE = "SINGLE"
    SHARING = "SHARING"
    BOTH = "BOTH"


class Furnishing(str, enum.Enum):
    FULL = "FULL"
    SEMI = "SEMI"
    UNFURNISHED = "UNFURNISHED"


class MoveIn(str, enum.Enum):
    ASAP = "ASAP"
    WITHIN_1_MONTH = "WITHIN_1_MONTH"
    ONE_TO_THREE_MONTHS = "ONE_TO_THREE_MONTHS"


class ListingGenderPref(str, enum.Enum):
    GIRLS_ONLY = "GIRLS_ONLY"
    BOYS_ONLY = "BOYS_ONLY"
    MIXED = "MIXED"


class Amenity(str, enum.Enum):
    PARKING = "PARKING"
    AC = "AC"
    KITCHEN = "KITCHEN"
    WASHING_MACHINE = "WASHING_MACHINE"
    LIFT = "LIFT"
    BALCONY = "BALCONY"
    POOL = "POOL"


class RequestTargetKind(str, enum.Enum):
    USER = "USER"
    TEAM = "TEAM"


class RequestStatus(str, enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class DecisionStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
