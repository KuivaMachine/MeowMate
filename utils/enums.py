import sys
from enum import Enum
from pathlib import Path

from PyQt6.QtCore import QSize, QPoint

from character import Character
# Определяем путь к каталогу с данными в зависимости от режима исполнения
base_path = getattr(sys, '_MEIPASS', None)
if base_path is not None:
    # Мы находимся в упакованном виде (PyInstaller)
    app_directory = Path(base_path)
else:
    # Обычный режим разработки
    app_directory = Path(__file__).parent.parent  # Найти родительский каталог проекта

# Теперь можем обратиться к нужным ресурсам
resource_path = app_directory / 'drawable'

class CatState(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"

class Direction(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"

class ThemeColor (Enum):
    LIGHT = 'light'
    DARK = 'dark'

class CharactersStartCoordinates(Enum):
    CAT = QPoint()

class CharactersList (Enum):
    CAT = Character('АБРИКОС', 'Описание кота', str(resource_path / 'cat' / 'cat_preview.gif'), QSize(160, 160), 130)
    FLORK =  Character('ФЛОРК', 'ОПИСАНИЕ ФЛОРКА', str(resource_path / 'flork' / 'flork_dance.gif'), QSize(160, 160),130)
    CSAT = Character('АБРИКОС', 'Описание кота', str(resource_path / 'cat' / 'cat_preview.gif'), QSize(160, 160), 130)
    FLFORK = Character('ФЛОРК', 'ОПИСАНИЕ ФЛОРКА', str(resource_path / 'flork' / 'flork_dance.gif'), QSize(160, 160),
                      130)
    CDAT = Character('АБРИКОС', 'Описание кота', str(resource_path / 'cat' / 'cat_preview.gif'), QSize(160, 160), 130)
    FLGORK = Character('ФЛОРК', 'ОПИСАНИЕ ФЛОРКА', str(resource_path / 'flork' / 'flork_dance.gif'), QSize(160, 160),
                      130)
    @classmethod
    def getFirst(cls):
        return next(iter(cls))