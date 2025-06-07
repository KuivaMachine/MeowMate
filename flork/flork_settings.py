import json
import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QSlider, QLabel
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

        self.size = settings["size"]



        self.flork_label = QSvgWidget(self)
        self.flork_label.setGeometry(30, 30, 150, 28)
        self.flork_label.load(str(self.resource_path / 'flork_label.svg'))

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(30,100,30,300)

        self.text = QLabel(f"Размер, пиксели: {self.size}")
        self.text.setObjectName('text')


        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet("""
        QSlider::groove:horizontal {
            height: 10px;
            background-color:#E8DEFF;
            border-radius: 3px;
            border:2px solid #0F0F94;
        }

        QSlider::handle:horizontal {
            width: 10px;
            height: 25px;
            margin: -5px 0;
            background-color:#0F0F94;
            border: 2px solid #0F0F94;
            border-radius: 3px;
        }

        QSlider::sub-page:horizontal {
            background-color:#9F73FF;
            border-radius: 3px;
            border:2px solid #0F0F94;
        }
          
        """)
        self.slider.setRange(100, 500)
        self.slider.setValue(int(self.size))  # значение по умолчанию
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(100)

        # Подписываемся на изменение положения ползунка
        self.slider.valueChanged.connect(self.update_label_and_fix_position)




        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.slider)




        self.ok = OkButton(self,'flork_done_btn')
        self.ok.setGeometry((320-90)//2,390,90,40)
        self.ok.clicked.connect(self.save_settings)

    def update_label_and_fix_position(self, value):
        """
        Этот метод обновляет отображаемое значение и гарантирует, что ползунок находится точно на одной из позиций риска.
        """
        fixed_value = round(value / 50) * 50
        self.slider.setValue(fixed_value)
        self.size = fixed_value
        self.text.setText(f"Размер, пиксели: {self.size}")


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
                "size": self.slider.value(),
        }
        self.on_close.emit()
        self.close()

        with open(str(self.app_directory/"settings/flork_settings.json"), "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)



