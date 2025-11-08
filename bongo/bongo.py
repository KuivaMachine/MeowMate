import json
import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from pynput import keyboard

from bongo.bongo_settings import BongoSettingsWindow
from ui.tap_counter_window import Counter
from utils.character_abstract import Character
from utils.enums import BongoType
from utils.utils import get_bongo_enum

# ЧИТАЕТ НАСТРОЙКИ ИЗ ПАПКИ APPDATA
def get_appdata_path(relative_path):
    appdata = os.getenv('APPDATA')
    app_dir = Path(appdata) / "MeowMate" / relative_path
    return app_dir

class Bongo(Character):
    app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'bongo'

    def __init__(self, settings):
        super().__init__()
        self.bongo_type = get_bongo_enum(settings["bongo_type"])    # ТИП ИНСТРУМЕНТА
        self.enable_tap_counter = settings["tap_counter"]           # РАЗРЕШЕН ЛИ СЧЕТЧИК
        self.count = settings["count"]                              # ЧИСЛО НА СЧЕТЧИКЕ

        self.is_close_btn_showing = False
        self.cat_main_pixmap = None                                 # ГЛАВНАЯ КАРТИНКА
        self.left_pixmap = None                                     # ЛЕВАЯ ЛАПА УДАРИЛА
        self.right_pixmap = None                                    # ПРАВАЯ ЛАПА УДАРИЛА
        self.drag_pos = None                                        # НАЧАЛЬНАЯ ПОЗИЦИЯ ОКНА В МОМЕНТ НАЖАТИЯ ПЕРЕД ПЕРЕТАСКИВАНИЕМ
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint|
            Qt.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(900, 600, 392, 392)

        self.cat = QLabel(self)
        self.cat.setFixedSize(392, 392)

        self.flag = True
        match self.bongo_type:
            case (BongoType.ROCK):
                self.cat_main_pixmap = QPixmap(str(self.resource_path / 'rock' / "cat_rock.png"))
                self.left_pixmap = QPixmap(str(self.resource_path / 'rock' / "cat_rock_left.png"))
                self.right_pixmap = QPixmap(str(self.resource_path / 'rock' / "cat_rock_right.png"))
            case (BongoType.PIANO):
                self.cat_main_pixmap = QPixmap(str(self.resource_path / 'piano' / "cat_piano.png"))
                self.left_pixmap = QPixmap(str(self.resource_path / 'piano' / "cat_piano_left.png"))
                self.right_pixmap = QPixmap(str(self.resource_path / 'piano' / "cat_piano_right.png"))
            case (BongoType.CLASSIC):
                self.cat_main_pixmap = QPixmap(str(self.resource_path / 'classic' / "cat_classic.png"))
                self.left_pixmap = QPixmap(str(self.resource_path / 'classic' / "cat_classic_left.png"))
                self.right_pixmap = QPixmap(str(self.resource_path / 'classic' / "cat_classic_right.png"))
            case (BongoType.GUITAR):
                self.cat_main_pixmap = QPixmap(str(self.resource_path / 'guitar' / "cat_guitar.png"))
                self.left_pixmap = QPixmap(str(self.resource_path / 'guitar' / "cat_guitar_left.png"))
                self.right_pixmap = QPixmap(str(self.resource_path / 'guitar' / "cat_guitar_right.png"))
            case (BongoType.BONGO):
                self.cat_main_pixmap = QPixmap(str(self.resource_path / 'bongo' / "cat_bongo.png"))
                self.left_pixmap = QPixmap(str(self.resource_path / 'bongo' / "cat_bongo_left.png"))
                self.right_pixmap = QPixmap(str(self.resource_path / 'bongo' / "cat_bongo_right.png"))


        self.cat.setPixmap(self.cat_main_pixmap)


        # СЛУШАТЕЛЬ КЛАВИАТУРЫ
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        )
        self.listener.start()

        if self.enable_tap_counter:
            self.counter = Counter(self.count, self)

    # ОБРАБОТКА НАЖАТИЯ НА КЛАВИАТУРУ
    def on_press(self, _):
        if self.flag:
            self.cat.setPixmap(self.left_pixmap)
            self.flag = False
        else:
            self.cat.setPixmap(self.right_pixmap)
            self.flag = True
        self.count = int(self.count)+1
        if self.enable_tap_counter:
            self.counter.setText(str(self.count))


    # ОБРАБОТКА ОТПУСКАНИЯ КЛАВИШИ КЛАВИАТУРЫ
    def on_release(self, _):
        self.cat.setPixmap(self.cat_main_pixmap)

    # СЛУШАТЕЛЬ ЗАКРЫТИЯ ОКНА
    def closeEvent(self, event):
        settings = {
            "tap_counter": self.enable_tap_counter,
            "bongo_type": self.bongo_type.value,
            "count": self.count
        }
        with open(str(get_appdata_path("settings/bongo_settings.json")), "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)


        self.listener.stop()
        super().closeEvent(event)

    # ВОЗВРАЩАЕТ ОКНО НАСТРОЕК
    @staticmethod
    def getSettingWindow(root_container, settings):
        return BongoSettingsWindow(root_container, settings)
