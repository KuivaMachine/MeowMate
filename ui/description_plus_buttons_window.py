import sys
from pathlib import Path

from PyQt5.QtCore import QSize, Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint, QAbstractAnimation
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QLabel

from ui.custom_button import CustomAnimatedButton


class DescriptionWindow(QWidget):
    start_button_clicked = pyqtSignal()
    settings_button_clicked = pyqtSignal()
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable'/'menu'

    def __init__(self, parent, name, text_description):
        super().__init__()
        self.parent = parent
        self.name_label = None
        self.description_label = None
        self.name = name
        self.description = text_description

        self.setMaximumWidth(260)

        self.gears = QLabel()
        self.gears_movie = QMovie(str(self.resource_path /'gears_big.gif'))
        self.gears_movie.setScaledSize(QSize(260, 130))
        self.gears.setMovie(self.gears_movie)
        self.gears.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gears.hide()

        self.rockets = QLabel()
        self.rocket_movie = QMovie(str(self.resource_path /'rockets.gif'))
        self.rocket_movie.setScaledSize(QSize(260, 130))
        self.rockets.setMovie(self.rocket_movie)
        self.rockets.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rockets.hide()

        description_layout = QVBoxLayout(self)
        description_layout.setContentsMargins(0, 0, 0, 0)
        description_layout.addWidget(self.setup_description())
        description_layout.addWidget(self.setup_buttons())


    def update_info(self, character):

        self.name = character.value.name
        self.description = character.value.description

        self.name_label.hide()
        self.description_label.hide()

        self.name_label.setText(self.name)
        self.description_label.setText(self.description)

        self.name_label.show()
        self.description_label.show()

        self.name_animation.start()
        self.description_animation.start()




    def setup_buttons(self):
        buttons_container = QWidget()
        buttons_container.setFixedSize(260,130)
        stack = QStackedLayout(buttons_container)
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        start_button = CustomAnimatedButton("ЗАПУСТИТЬ", str(self.resource_path /'fire_mini.gif'), self)
        start_button.clicked.connect(lambda : self.start_button_clicked.emit())
        setting_button = CustomAnimatedButton("НАСТРОИТЬ", str(self.resource_path /'gears_mini.gif'), self)
        setting_button.clicked.connect(lambda : self.settings_button_clicked.emit())
        button_layout = QWidget()
        button_layout.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        main_layout = QVBoxLayout(button_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(start_button)
        main_layout.addWidget(setting_button)

        stack.addWidget(button_layout)
        stack.addWidget(self.gears)
        stack.addWidget(self.rockets)

        return buttons_container


    def start_rockets_animation(self):
        self.rocket_movie.start()
        self.rockets.show()


    def hide_rockets_animation(self):
        self.rockets.hide()
        self.rocket_movie.stop()


    def start_gears_animation(self):
        self.gears_movie.start()
        self.gears.show()


    def hide_gears_animation(self):
        self.gears.hide()
        self.gears_movie.stop()


    def setup_description(self):
        description_container = QWidget()
        description_container.setFixedSize(260, 345)
        description_container.setObjectName('description_container')


        self.name_label  = QLabel(self.name)
        self.name_label.setObjectName('name_text')
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_animation = QPropertyAnimation(self.name_label, b"pos")
        self.name_animation.setDuration(500)
        self.name_animation.setDirection(QAbstractAnimation.Direction.Backward)
        self.name_animation.setEasingCurve(QEasingCurve.Type.InExpo)
        self.name_animation.setStartValue(QPoint(self.name_label.pos().x(),self.name_label.pos().y()))
        self.name_animation.setEndValue(QPoint(self.name_label.pos().x()-200,self.name_label.pos().y()))

        self.description_label = QLabel(self.description)
        self.description_label.setObjectName('description_text')
        self.description_label.setWordWrap(True)

        self.description_animation = QPropertyAnimation(self.description_label, b"pos")
        self.description_animation.setDuration(500)
        self.description_animation.setDirection(QAbstractAnimation.Direction.Backward)
        self.description_animation.setEasingCurve(QEasingCurve.Type.InOutCirc)
        self.description_animation.setStartValue(QPoint(self.name_label.pos().x() + 10, self.name_label.pos().y()))
        self.description_animation.setEndValue(QPoint(self.name_label.pos().x() + 400, self.name_label.pos().y()))

        description_layout = QVBoxLayout(description_container)
        description_layout.addWidget(self.name_label, stretch=2)
        description_layout.addWidget(self.description_label, stretch=8)

        return description_container

