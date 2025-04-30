from re import match

from PyQt6.QtCore import QSize, Qt, QRect, pyqtSignal
from PyQt6.QtGui import QMovie, QPixmap
from PyQt6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QLabel

from ui.custom_button import CustomAnimatedButton
from utils.enums import Characters


class DescriptionWindow(QWidget):
    start_button_clicked = pyqtSignal()
    settings_button_clicked = pyqtSignal()
    def __init__(self, parent, name, text_description):
        super().__init__()
        self.parent = parent
        self.name_label = None
        self.description_label = None
        self.name = name
        self.description = text_description

        self.setMaximumWidth(260)

        self.gears = QLabel()
        self.gears_movie = QMovie("./drawable/menu/gears_big.gif")
        self.gears_movie.setScaledSize(QSize(260, 130))
        self.gears.setMovie(self.gears_movie)
        self.gears.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gears.hide()

        self.rockets = QLabel()
        self.rocket_movie = QMovie("./drawable/menu/rockets.gif")
        self.rocket_movie.setScaledSize(QSize(260, 130))
        self.rockets.setMovie(self.rocket_movie)
        self.rockets.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rockets.hide()


        description_layout = QVBoxLayout(self)
        description_layout.setContentsMargins(0, 0, 0, 0)
        description_layout.addWidget(self.setup_description())
        description_layout.addWidget(self.setup_buttons())

    def update_info(self, character):
        match character:
            case(Characters.FLORK):
                self.name = "ФЛОРК"
                self.description = "Описание флорка"
            case (Characters.CAT):
                self.name = "АБРИКОС"
                self.description = "Описание кота"
            case (Characters.BONGO_CAT):
                self.name = "БОНГО-КОТ"
                self.description = "Описание бонго кота"


        self.name_label.setText(self.name)
        self.description_label.setText(self.description)



    def setup_buttons(self):
        buttons_container = QWidget()
        buttons_container.setFixedSize(260,130)
        stack = QStackedLayout(buttons_container)
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        # 2. Добавляем кнопку (будет спереди)
        start_button = CustomAnimatedButton("ЗАПУСТИТЬ", "./drawable/menu/fire_mini.gif", self)
        start_button.clicked.connect(lambda : self.start_button_clicked.emit())
        setting_button = CustomAnimatedButton("НАСТРОИТЬ", "./drawable/menu/gears_mini.gif", self)
        setting_button.clicked.connect(lambda : self.settings_button_clicked.emit())
        button_layout = QWidget()
        button_layout.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        main_layout = QVBoxLayout(button_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(start_button)
        main_layout.addWidget(setting_button)

        stack.addWidget(button_layout)
        stack.addWidget(self.gears)
        stack.addWidget(self.rockets)

        return buttons_container


    def startRocketsAnimation(self):
        self.rocket_movie.start()
        self.rockets.show()


    def hideRocketsAnimation(self):
        self.rockets.hide()
        self.rocket_movie.stop()


    def startGearsAnimation(self):
        self.gears_movie.start()
        self.gears.show()


    def hideGearsAnimation(self):
        self.gears.hide()
        self.gears_movie.stop()


    def setup_description(self):
        description_container = QWidget()
        description_container.setObjectName('description_container')


        self.name_label  = QLabel(self.name)
        self.name_label.setObjectName('name_text')
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)



        self.description_label = QLabel(self.description)
        self.description_label.setObjectName('description_text')
        self.description_label.setWordWrap(True)


        description_layout = QVBoxLayout(description_container)
        description_layout.addWidget(self.name_label, stretch=2)
        description_layout.addWidget(self.description_label, stretch=8)

        return description_container

