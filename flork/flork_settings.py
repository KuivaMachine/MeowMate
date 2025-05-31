import json
import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QCheckBox, QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from ui.question_window import Question
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
        self.sounds_check.setStyleSheet(self.get_stylesheet())

        self.question = Question("Разрешает коту\nгоняться за мухой\n(шанс появления - 1.25%)")

        self.vbox.addWidget(self.sounds_check, alignment=Qt.AlignLeft)



        self.ok = OkButton(self,'flork_done_btn')
        self.ok.setGeometry((320-90)//2,390,90,40)
        self.ok.clicked.connect(self.save_settings)

    def get_stylesheet(self):
        return f"""
        /* FLORK_CHECKBOX */
        QCheckBox {{
            spacing: 8px;
            color: black;
            font-size: 20px;
            font-weight: regular;
            font-family: 'PT Mono';
        }}
        /* Квадратик в невыбранном состоянии */
        QCheckBox::indicator {{
            width: 25px;
            height: 25px;
            border: 2px solid #0F0F94;  /* Рамка */
            border-radius: 6px;
            background: #E8DEFF;  /* Фон */
        }}
        /* При наведении */
        QCheckBox::indicator:hover {{
            background:#C7ADFF;
            border: 2px solid #0F0F94;
        }}
        /* В выбранном состоянии */
        QCheckBox::indicator:checked {{
            background: #AD87FF;  /* Фон выбранного */
            image: url({(self.resource_path/'checkmark.png').as_posix()});
        }}"""

    def save_settings(self):
        settings = {
                "sounds": self.sounds_check.isChecked(),
        }
        self.on_close.emit()
        self.close()

        with open(str(self.app_directory/"settings/flork_settings.json"), "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)



