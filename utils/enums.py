from enum import Enum

class CatState(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"

class Characters(Enum):
    CAT = "cat"
    FLORK = "flork"
    BONGO_CAT= "bongo_cat"
class Direction(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"

class ThemeColor (Enum):
    LIGHT = 'light'
    DARK = 'dark'