
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtGui import QMovie, QPixmap
from PyQt6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QLabel

from ui.custom_button import CustomAnimatedButton


class DescriptionWindow(QWidget):
    def __init__(self, name, text_description):
        super().__init__()
        self.name = name
        self.description = text_description

        self.setMaximumWidth(260)
        self.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border: none;
                }
            """)
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



    def setup_buttons(self):
        buttons_container = QWidget()
        buttons_container.setFixedSize(260,130)
        buttons_container.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)

        stack = QStackedLayout(buttons_container)
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        # 2. Добавляем кнопку (будет спереди)
        start_button = CustomAnimatedButton("ЗАПУСТИТЬ", "./drawable/menu/fire_mini.gif", self)
        setting_button = CustomAnimatedButton("НАСТРОИТЬ", "./drawable/menu/gears_mini.gif", self)
        button_layout = QWidget()
        button_layout.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
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
        description_container.setStyleSheet("""
            QWidget {
                background-color: #FFE5BD;
                border: 2px solid #000000;
                border-radius: 15px;
            }
        """)


        name_label  = QLabel(self.name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("""
        QLabel{
        color: #000000;
        font-size: 30px;
        font-weight: light;
        font-family: 'JetBrains Mono';
        border: none;
        }
        """)


        description_label = QLabel(self.description)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("""
                QLabel{
                color: #000000;
                text-align: left;
                font-size: 15px;
                font-weight: light;
                font-family: 'JetBrains Mono';
                border: none;
                }
                """)

        description_layout = QVBoxLayout(description_container)
        description_layout.addWidget(name_label, stretch=2)
        description_layout.addWidget(description_label, stretch=8)

        return description_container

