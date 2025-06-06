import json
import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSignal, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QCheckBox, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from ui.question_window import Question
from ui.settings_window import SettingsWindow, OkButton


class ApricotSettingsWindow(SettingsWindow):
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'cat'
    on_close = pyqtSignal()

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.setObjectName('ApricotSettingsWindow')

        self.enable_sounds = settings["sounds"]
        self.enable_fly = settings["fly"]
        self.enable_pacman = settings["pacman"]
        self.cat_hiding_delay = settings["cat_hiding_delay"]

        self.bongo_label = QSvgWidget(self)
        self.bongo_label.setGeometry(30, 30, 196, 28)
        self.bongo_label.load(str(self.resource_path / 'apricot_label.svg'))

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(30, 120, 30, 120)

        self.sounds_check = QCheckBox("Включить звуки")
        self.sounds_check.setChecked(self.enable_sounds)
        self.sounds_check.setStyleSheet(self.get_stylesheet())

        self.pacman_check = QCheckBox("Пакмен")
        self.pacman_check.setChecked(self.enable_pacman)
        self.pacman_check.setStyleSheet(self.get_stylesheet())
        self.question = Question("Запустите кота\nи наберите\nна клавиатуре:\n\"пакмен\" или \"pacman\"")
        self.pacman_hbox = QHBoxLayout()
        self.pacman_hbox.setSpacing(5)
        self.pacman_hbox.addWidget(self.pacman_check, alignment=Qt.AlignLeft)
        self.pacman_hbox.addWidget(self.question, alignment=Qt.AlignLeft)


        self.fly_check = QCheckBox("Муха")
        self.fly_check.setChecked(self.enable_fly)
        self.fly_check.setStyleSheet(self.get_stylesheet())
        self.question = Question("Разрешает коту\nгоняться за мухой\n(шанс появления - 1.25%)")
        self.fly_hbox = QHBoxLayout()
        self.fly_hbox.setSpacing(5)
        self.fly_hbox.addWidget(self.fly_check, alignment=Qt.AlignLeft)
        self.fly_hbox.addWidget(self.question, alignment=Qt.AlignLeft)


        self.text = QLabel("Задержка перед появлением,\nсекунды:")
        self.text.setObjectName('text')

        self.input = QLineEdit()
        regex = QRegExp("^([0-9]|[1-5][0-9]|60)$")
        validator = QRegExpValidator(regex, self.input)
        self.input.setValidator(validator)
        self.input.setText(self.cat_hiding_delay)
        self.input.setObjectName('apricot_cat_hiding_delay')
        self.input.setPlaceholderText("от 0 до 60")

        self.vbox.addWidget(self.sounds_check)
        self.vbox.addLayout(self.pacman_hbox)
        self.vbox.addLayout(self.fly_hbox)
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.input)

        self.ok = OkButton(self, 'apricot_done_btn')
        self.ok.setGeometry((320 - 90) // 2, 390, 90, 40)
        self.ok.clicked.connect(self.save_settings)

    def get_stylesheet(self):
        return f"""
          /* APRICOT_CHECKBOX */
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
                border: 2px solid #692D00;
                border-radius: 6px;
                background: #FFC89E;  /* Фон */
            }}
            /* При наведении */
            QCheckBox::indicator:hover {{
                background:#CF844B;
                border: 2px solid #692D00;
            }}
            /* В выбранном состоянии */
            QCheckBox::indicator:checked {{
                background: #CF844B; 
                border: 2px solid #692D00;
                font-size: 20px;
                font-weight: light;
                font-family: 'PT Mono';
                image: url({(self.resource_path / 'checkmark.png').as_posix()});
            }}"""

    def save_settings(self):
        settings = {
            "sounds": self.sounds_check.isChecked(),
            "pacman": self.pacman_check.isChecked(),
            "fly": self.fly_check.isChecked(),
            "cat_hiding_delay": self.input.text() if self.input.text() != "" else "0",
        }
        self.on_close.emit()
        self.close()

        with open(str(self.app_directory/"settings/apricot_settings.json"), "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
