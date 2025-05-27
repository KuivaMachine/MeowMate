import sys
from enum import Enum
from pathlib import Path

from PyQt5.QtCore import QSize, QPoint

from character import Character
base_path = getattr(sys, '_MEIPASS', None)
if base_path is not None:
    app_directory = Path(base_path)
else:
    app_directory = Path(__file__).parent.parent
resource_path = app_directory / 'drawable'

class CatState(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"

class Direction(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"

class BongoType(Enum):
    ROCK = 'rock'
    GUITAR = 'guitar'
    BONGO = 'bongo'
    PIANO = 'piano'
    CLASSIC='classic'

class ThemeColor (Enum):
    LIGHT = 'light'
    DARK = 'dark'


class CharactersList (Enum):
    CAT = Character('АБРИКОС', 'Описание кота', str(resource_path / 'cat' / 'cat_preview.gif'), QSize(160, 160), 130)
    FLORK =  Character('ФЛОРК', 'ОПИСАНИЕ ФЛОРКА', str(resource_path / 'flork' / 'flork_dance.gif'), QSize(160, 160),130)
    BONGO = Character('БОНГО-КОТ', 'Описание бонго-кота', str(resource_path / 'bongo' / 'cat_preview.gif'), QSize(160, 160), 100)
    @classmethod
    def getFirst(cls):
        return next(iter(cls))