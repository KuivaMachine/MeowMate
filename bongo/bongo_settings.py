import json
import os
import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QCheckBox, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QToolBar, QComboBox

from ui.settings_window import SettingsWindow, OkButton

def get_appdata_path(relative_path):
    appdata = os.getenv('APPDATA')
    app_dir = Path(appdata) / "MeowMate" / relative_path
    return app_dir

class BongoSettingsWindow(SettingsWindow):
    app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'bongo'
    on_close = pyqtSignal()

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.setObjectName('BongoSettingsWindow')

        self.bongo_type = settings["bongo_type"]
        self.enable_tap_counter = settings["tap_counter"]
        self.count = settings["count"]

        self.bongo_label = QSvgWidget(self)
        self.bongo_label.setGeometry(30, 30, 150, 28)
        self.bongo_label.load(str(self.resource_path / 'bongo_label.svg'))

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(30, 120, 30, 120)

        self.taps_count_check = QCheckBox("Показать счетчик")
        self.taps_count_check.setChecked(self.enable_tap_counter)
        self.taps_count_check.setStyleSheet(self.get_stylesheet())

        self.reset_btn = QPushButton("Сбросить счетчик")
        self.reset_btn.setStyleSheet("""QPushButton {
            color: black;
            font-size: 15px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
            background-color: #FFE0E0;
            border: 2px solid #8F3C43;
            border-radius:5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #E3BABC;
        }
        QPushButton:pressed {
            color: black;
            font-size: 15px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
            background-color: #E38D91;
            border: 2px solid black;
            border-radius:5px;
        }""")
        self.reset_btn.clicked.connect(self.reset_counter)


        self.toolbar = QToolBar()
        self.toolbar.setObjectName('toolbar_bongo')
        self.combo = QComboBox()
        self.combo.setObjectName('toolbar_bongo_combo')
        self.combo.addItems(["Классика", "Пианино", "Электрогитара", "Бонго", "Гитара"])
        self.combo.setCurrentText(self.bongo_type)
        self.toolbar.addWidget(self.combo)


        self.vbox.addWidget(self.taps_count_check)
        self.vbox.addWidget(self.reset_btn)
        self.vbox.addWidget(self.toolbar)

        self.ok = OkButton(self, 'ok_button')
        self.ok.setGeometry((320 - 90) // 2, 390, 90, 40)
        self.ok.clicked.connect(self.save_settings)
    def reset_counter(self):
        self.count = 0

    def get_stylesheet(self):
        return f"""
          /* BONGO_CHECKBOX */
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
            border: 2px solid #8F3C43;  /* Рамка */
            border-radius: 6px;
            background: #FFE0E0;  /* Фон */
        }}
        /* При наведении */
        QCheckBox::indicator:hover {{
            background:#E3B3B5;
            border: 2px solid #8F3C43;
        }}
        /* В выбранном состоянии */
        QCheckBox::indicator:checked {{
            background: #E3B3B5;  /* Фон выбранного */
            border: 2px solid #8F3C43;
            font-size: 20px;
            font-weight: light;
            font-family: 'PT Mono';
            image: url({(self.resource_path / 'checkmark.png').as_posix()});
        }}"""


    def save_settings(self):
        settings = {
            "tap_counter": self.taps_count_check.isChecked(),
            "bongo_type": self.combo.currentText(),
            "count": self.count
        }
        self.on_close.emit()
        self.close()

        with open(str(get_appdata_path("settings/bongo_settings.json")), "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
