import json
import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QCheckBox, QLabel, QSlider
from PyQt5.QtWidgets import QVBoxLayout

from ui.settings_window import SettingsWindow, OkButton


class HamSettingsWindow(SettingsWindow):
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'ham'

    on_close = pyqtSignal()

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.setObjectName('HamSettingsWindow')

        self.enable_hiding = settings["hiding"]
        self.size = settings["size"]



        self.ham_label = QSvgWidget(self)
        self.ham_label.setGeometry(30, 30, 197, 28)
        self.ham_label.load(str(self.resource_path / 'ham_label.svg'))

        self.vbox = QVBoxLayout(self)
        self.vbox.setSpacing(20)
        self.vbox.setContentsMargins(30,130,30,180)

        self.text = QLabel(f"Размер, пиксели: {self.size}")
        self.text.setObjectName('text')

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    height: 10px;
                    background-color:#9064BF;
                    border-radius: 3px;
                    border:2px solid #220A5F;
                }

                QSlider::handle:horizontal {
                    width: 10px;
                    height: 25px;
                    margin: -5px 0;
                    background-color:#5300AB;
                    border: 2px solid #220A5F;
                    border-radius: 3px;
                }

                QSlider::sub-page:horizontal {
                    background-color:#5300AB;
                    border-radius: 3px;
                    border:2px solid #220A5F;
                }
                """)
        self.slider.setRange(100, 400)
        self.slider.setValue(int(self.size))
        self.slider.valueChanged.connect(lambda: self.text.setText(f"Размер, пиксели: {self.slider.value()}"))

        self.enable_hiding_check = QCheckBox("Прятаться")
        self.enable_hiding_check.setChecked(self.enable_hiding)
        self.enable_hiding_check.setStyleSheet(self.get_stylesheet())

        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.slider)
        self.vbox.addWidget(self.enable_hiding_check, alignment=Qt.AlignLeft)


        self.ok = OkButton(self,'ham_done_btn')
        self.ok.setGeometry((320-90)//2,390,90,40)
        self.ok.clicked.connect(self.save_settings)



    def get_stylesheet(self):
        return f"""
        /* HAM_CHECKBOX */
        QCheckBox {{
            margin:20px 0px;
            color: black;
            font-size: 20px;
            font-weight: regular;
            font-family: 'PT Mono';
        }}
        /* Квадратик в невыбранном состоянии */
        QCheckBox::indicator {{
            width: 25px;
            height: 25px;
            border: 2px solid #220A5F;  /* Рамка */
            border-radius: 6px;
            background: #9064BF;  /* Фон */
        }}
        /* При наведении */
        QCheckBox::indicator:hover {{
            background:#72489E;
        }}
        /* В выбранном состоянии */
        QCheckBox::indicator:checked {{
            background: #EC54B3;  /* Фон выбранного */
            image: url({(self.resource_path/'checkmark.png').as_posix()});
        }}"""

    def save_settings(self):
        settings = {
            "size": self.slider.value(),
            "hiding": self.enable_hiding_check.isChecked()
        }
        self.on_close.emit()
        self.close()

        with open(str(self.app_directory/"settings/ham_settings.json"), "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)



