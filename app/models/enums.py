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


class SleepSchedule(str, enum.Enum):
    EARLY_BIRD = "EARLY_BIRD"
    NIGHT_OWL = "NIGHT_OWL"
    FLEXIBLE = "FLEXIBLE"


class Cleanliness(str, enum.Enum):
    VERY_TIDY = "VERY_TIDY"
    AVERAGE = "AVERAGE"
    RELAXED = "RELAXED"


class YesNoSometimes(str, enum.Enum):
    YES = "YES"
    NO = "NO"
    SOMETIMES = "SOMETIMES"


class FoodPref(str, enum.Enum):
    VEG = "VEG"
    NON_VEG = "NON_VEG"
    EGGITARIAN = "EGGITARIAN"


class Frequency(str, enum.Enum):
    OFTEN = "OFTEN"
    SOMETIMES = "SOMETIMES"
    RARELY = "RARELY"


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
