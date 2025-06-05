import sys
from pathlib import Path
import random

from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QTimer
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel

from ham.ham_settings import HamSettingsWindow
from utils.character_abstract import Character


class Ham(Character):
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'ham'

    def __init__(self, settings):
        super().__init__()
        self.enable_sounds = settings["sounds"]

        self.is_first_frame = None
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.screen = QApplication.primaryScreen().geometry()
        self.setGeometry(500, 500, 267, 150)
        self.setMouseTracking(True)

        self.main_movie = QMovie(str(self.resource_path / "main.gif"))
        self.main_movie.setSpeed(120)
        self.main_movie.setScaledSize(QSize(267, 150))
        self.main_movie.start()

        self.run_movie = QMovie(str(self.resource_path / "move.gif"))
        self.run_movie.setSpeed(140)
        self.run_movie.setScaledSize(QSize(267, 150))
        self.run_movie.frameChanged.connect(self.check_frame_change)

        self.stick_pix = QPixmap(str(self.resource_path / "stick.png")).scaled(267, 150,
                                                                               Qt.AspectRatioMode.KeepAspectRatio,
                                                                               Qt.TransformationMode.SmoothTransformation)
        self.transparent_pix = QPixmap(str(self.resource_path / "transparent.png")).scaled(267, 150,
                                                                                           Qt.AspectRatioMode.KeepAspectRatio,
                                                                                           Qt.TransformationMode.SmoothTransformation)

        self.stick = QLabel(self)
        self.stick.setMouseTracking(True)
        self.stick.setPixmap(self.stick_pix)
        self.stick.setGeometry(0, 0, 267, 150)

        self.ham_main = QLabel(self)
        self.ham_main.setMouseTracking(True)
        self.ham_main.setMovie(self.main_movie)
        self.ham_main.setGeometry(0, 0, 267, 150)

        self.run_animation = QPropertyAnimation(self.ham_main, b"pos")
        self.run_animation.setDuration(300)

        self.timer = QTimer(self)
        self.timer.setInterval(300000) #5 минут
        self.timer.timeout.connect(self.make_transparent)
        self.timer.start()

    def make_transparent(self):
        self.ham_main.setPixmap(self.transparent_pix)

    def stop_run_animation(self):
        self.run_movie.stop()
        self.ham_main.setMovie(self.main_movie)
        self.main_movie.start()

    def check_frame_change(self, frame_number):
        if frame_number == 0:
            if self.is_first_frame:
                self.stop_run_animation()
                self.is_first_frame = False
            else:
                self.is_first_frame = True

    def mousePressEvent(self, event):
        self.main_movie.stop()
        self.timer.stop()
        self.timer.start()
        self.ham_main.setMovie(self.run_movie)
        self.run_movie.start()

        self.run_animation.setStartValue(QPoint(self.ham_main.x(), self.ham_main.y()))
        self.run_animation.setEndValue(QPoint(self.get_x_value(self.ham_main.x()), self.ham_main.y()))
        self.run_animation.start()
        super().mousePressEvent(event)

    def get_x_value(self, current_x):
        max_right = 60  # Максимум вправо от 0
        max_left = -65  # Максимум влево от 0
        # Определяем доступное расстояние для движения в каждом направлении
        available_right = max_right - current_x
        available_left = current_x - max_left
        if available_right > available_left:
            # Движение вправо
            shift = random.randint(10, available_right)
            new_x = current_x + shift
        else:  # Движение влево
            shift = random.randint(10, available_left)
            new_x = current_x - shift
        return new_x

    @staticmethod
    def getSettingWindow(root_container, settings):
        return HamSettingsWindow(root_container, settings)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ham = Ham()
    ham.show()
    sys.exit(app.exec())
