import json
import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QToolBar, QComboBox

from ui.settings_window import SettingsWindow, OkButton
from utils.utils import get_bongo_enum


class BongoSettingsWindow(SettingsWindow):
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'bongo'
    on_close = pyqtSignal()

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.setObjectName('BongoSettingsWindow')

        self.bongo_type = settings["bongo_type"]
        self.enable_sounds = settings["sounds"]
        self.enable_tap_counter = settings["tap_counter"]



        self.bongo_label = QSvgWidget(self)
        self.bongo_label.setGeometry(30,30,150,28)
        self.bongo_label.load(str(self.resource_path / 'bongo_label.svg'))

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(30,120,30,120)

        self.taps_count_check = QCheckBox("Включить счетчик")
        self.taps_count_check.setChecked(self.enable_tap_counter)
        self.taps_count_check.setObjectName('checkbox_bongo')

        self.sounds_check = QCheckBox("Включить звуки")
        self.sounds_check.setChecked(self.enable_sounds)
        self.sounds_check.setObjectName('checkbox_bongo')


        self.toolbar = QToolBar()
        self.toolbar.setObjectName('toolbar_bongo')
        self.combo = QComboBox()
        self.combo.setObjectName('toolbar_bongo_combo')
        self.combo.addItems(["Классика", "Пианино", "Электрогитара","Бонго","Гитара"])
        self.combo.setCurrentText(self.bongo_type)
        self.toolbar.addWidget(self.combo)

        self.vbox.addWidget(self.sounds_check)
        self.vbox.addWidget(self.taps_count_check)
        self.vbox.addWidget(self.toolbar)


        self.ok = OkButton(self,'ok_button')
        self.ok.setGeometry((320-90)//2,390,90,40)
        self.ok.clicked.connect(self.save_settings)


    def save_settings(self):
        settings = {
                "sounds": self.sounds_check.isChecked(),
                "tap_counter": self.taps_count_check.isChecked(),
                "bongo_type": self.combo.currentText()
        }
        self.on_close.emit()
        self.close()

        with open("./settings/bongo_settings.json", "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)


