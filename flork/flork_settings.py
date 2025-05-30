import json
import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QVBoxLayout
from ui.settings_window import SettingsWindow, OkButton


class FlorkSettingsWindow(SettingsWindow):
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'flork'

    on_close = pyqtSignal()

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.setObjectName('FlorkSettingsWindow')

        self.enable_sounds = settings["sounds"]



        self.bongo_label = QSvgWidget(self)
        self.bongo_label.setGeometry(30,30,150,28)
        self.bongo_label.load(str(self.resource_path / 'flork_label.svg'))

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(30,70,30,220)

        self.sounds_check = QCheckBox("Включить звуки")
        self.sounds_check.setChecked(self.enable_sounds)
        self.sounds_check.setObjectName('checkbox_flork')



        self.vbox.addWidget(self.sounds_check)




        self.ok = OkButton(self,'flork_done_btn')
        self.ok.setGeometry((320-90)//2,390,90,40)
        self.ok.clicked.connect(self.save_settings)


    def save_settings(self):
        settings = {
                "sounds": self.sounds_check.isChecked(),
        }
        self.on_close.emit()
        self.close()

        with open("./settings/flork_settings.json", "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)



