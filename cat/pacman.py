import sys
from pathlib import Path

from PyQt5.QtCore import QPropertyAnimation, Qt, QPoint, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QLabel

from utils.utils import get_taskbar_height


class Pacman(QLabel):

    app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable'/'cat'

    def __init__(self):
        super().__init__()

        # РАЗМЕРЫ ОКНА МОНИТОРА
        self.monitor_width = QApplication.primaryScreen().geometry().width()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, screen.height() - get_taskbar_height(QApplication.primaryScreen())-300, screen.width(), 300)

        self.pacman_label = QLabel(self)
        self.pacman_label.setGeometry(700, 0, 800, 300)

        self.pacman_gif = QMovie(str(self.resource_path /"pacman.gif"))
        self.pacman_gif.setScaledSize(QSize(800, 300))
        self.pacman_label.setMovie(self.pacman_gif)
        self.pacman_gif.start()

        self.pacman_animation = QPropertyAnimation(self.pacman_label, b"pos")
        self.pacman_animation.setDuration(17000)
        self.pacman_animation.setStartValue(QPoint(self.monitor_width, 0))
        self.pacman_animation.setEndValue(QPoint(0 - self.pacman_label.width(), 0))
        self.pacman_animation.finished.connect(self.remove_pacman)

    def remove_pacman(self):
        self.pacman_animation.stop()
        self.pacman_gif.stop()
        self.hide()

    def show_and_start(self):
        self.show()
        self.pacman_animation.start()