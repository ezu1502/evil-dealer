from enum import StrEnum, Enum, auto

class Ranks(Enum):
    ACE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()

class Suits(Enum):
    DIAMONDS = auto()
    CLUBS = auto()
    HEARTS = auto()
    SPADES = auto()

class TurnState(Enum):
    PLAYER_TURN = auto()
    DEALER_TURN = auto()
    FINISHED = auto()

class Actions(StrEnum):
    HIT = "H"
    STAND = "S"
    DOUBLE = "D"
    SPLIT = "P"
    SURRENDER = "R"