import sys
from enum import Enum
from pathlib import Path

from PyQt5.QtCore import QSize

from utils.character_model import CharacterModel

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
    ROCK = "Электрогитара"
    GUITAR = 'Гитара'
    BONGO = 'Бонго'
    PIANO = 'Пианино'
    CLASSIC='Классика'

class ThemeColor (Enum):
    LIGHT = 'light'
    DARK = 'dark'


class CharactersList (Enum):
    CAT = CharacterModel('АБРИКОС', '🍑 Солнечный проказник с пушистой душой! Этот рыжий комочек радости не просто сидит на экране — он живёт в нём! Cледит за твоим курсором с любопытством котёнка, а если ты подойдёшь слишком близко… Ха-ап! Нажмёшь на него — исчезнет в облачке смеха и тут же материализуется в новом месте, подмигивая)', str(resource_path / 'cat' / 'cat_preview.gif'), QSize(160, 160), 130)
    FLORK =  CharacterModel('ФЛОРК', '🍰 Флорк — мем, который обнял весь мир! А если кликнешь на него… Сюрприз! Может, он пустится в зажигательный танец, а может неожиданно достать праздничный тортик (откуда?!). Он скромен, но искренне верит, что мир становится лучше, когда люди улыбаются) Тортик в комплект не входит… или входит?', str(resource_path / 'flork' / 'flork_dance.gif'), QSize(160, 160), 130)
    BONGO = CharacterModel('БОНГО-КОТ', '🎹 Пушистый ритм-мастер! Этот усатый виртуоз отбивает зажигательный бит с каждым нажатием клавиатуры — на бонго, на гитаре, а может даже пианино! Настоящая мем-легенда, воплощение чистой радости и позитива. Поставь его где угодно — и он тут же устроит мини-концерт под звуки твоей печати.', str(resource_path / 'bongo' / 'cat_preview.gif'), QSize(160, 160), 100)
    HAM = CharacterModel('ЛЕНУСИК', '🦎💜 Фиолетовый философ на твоем рабочем столе! Этот хамелеон — настоящий мастер ничегонеделания! Его глаза смотрят даже в параллельную вселенную, а его кредо — "радуйся, пока другие ищут тебя взглядом". Осторожно - возможно он уже спрятался среди твоих документов! "Где же Ленусик? А вот же он! …Или нет?"', str(resource_path / 'ham' / 'ham_preview.gif'), QSize(160, 160), 120)

    @classmethod
    def getFirst(cls):
        return next(iter(cls))