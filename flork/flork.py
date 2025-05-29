import random
import sys
from pathlib import Path

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from pynput import keyboard

from character_abstract import Character


#TODO:НАСТРОЙКИ:
# Выключить звуки
# Зафиксировать по X
# Зафиксировать по Y
class Flork(Character):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent.parent  # Найти родительский каталог проекта
    # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable' / 'flork'

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(100, screen.height() - self.get_taskbar_height() - 200, 200, 200)
        self.setMouseTracking(True)

        self.current_gif = None

        self.shy = QMovie(str(self.resource_path / "flork_shy.gif"))
        self.shy.setScaledSize(QSize(200, 200))
        self.shy.setSpeed(110)
        self.shy.frameChanged.connect(self.check_frame_change)

        self.dance = QMovie(str(self.resource_path / "flork_dance.gif"))
        self.dance.setScaledSize(QSize(200, 200))
        self.dance.setSpeed(120)
        self.dance.frameChanged.connect(self.check_frame_change)

        self.flork_main_pixmap = QPixmap(str(self.resource_path / "flork_main.png")).scaled(200, 200,
                                                                                            Qt.AspectRatioMode.KeepAspectRatio,
                                                                                            Qt.TransformationMode.SmoothTransformation)
        self.flork_left_pixmap = QPixmap(str(self.resource_path / "flork_left.png")).scaled(200, 200,
                                                                                            Qt.AspectRatioMode.KeepAspectRatio,
                                                                                            Qt.TransformationMode.SmoothTransformation)
        self.flork_right_pixmap = QPixmap(str(self.resource_path / "flork_right.png")).scaled(200, 200,
                                                                                              Qt.AspectRatioMode.KeepAspectRatio,
                                                                                              Qt.TransformationMode.SmoothTransformation)

        self.flork_main = QLabel(self)
        self.flork_main.setMouseTracking(True)
        self.flork_main.setPixmap(self.flork_main_pixmap)
        self.flork_main.setGeometry(0, 0, 200, 200)

        self.flag = True
        self.is_first_frame = False
        self.isAnimationPlaying = False

        # СЛУШАТЕЛЬ КЛАВИАТУРЫ
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    def check_frame_change(self, frame_number):
        if frame_number == 0:
            if self.is_first_frame:
                self.stopAnimation()
                self.is_first_frame = False
            else:
                self.is_first_frame = True

    # ОБРАБОТКА НАЖАТИЯ НА КЛАВИАТУРУ
    def on_press(self, key):
        if self.flag:
            self.flork_main.setPixmap(self.flork_left_pixmap)
            self.flag = False
        else:
            self.flork_main.setPixmap(self.flork_right_pixmap)
            self.flag = True

        # ОБРАБОТКА ОТПУСКАНИЯ КЛАВИШИ КЛАВИАТУРЫ

    def on_release(self, key):
        self.flork_main.setPixmap(self.flork_main_pixmap)

    def stopAnimation(self):
        self.current_gif.stop()
        self.flork_main.setPixmap(self.flork_main_pixmap)
        self.isAnimationPlaying = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.isAnimationPlaying:
                random_int = random.randint(1, 2)
                self.playAnimation(random_int)
        else:
            super().mousePressEvent(event)

    def playAnimation(self, number):
        match number:
            case (1):
                self.current_gif = self.shy
                self.current_gif.start()
                self.flork_main.setMovie(self.current_gif)
            case (2):
                self.current_gif = self.dance
                self.current_gif.start()
                self.flork_main.setMovie(self.current_gif)
        # QTimer.singleShot(3800, self.stopAnimation)
        self.isAnimationPlaying = True

    def get_taskbar_height(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        available_rect = screen.availableGeometry()
        dpi_scale = screen.devicePixelRatio()

        if screen_rect.bottom() != available_rect.bottom():
            return int((screen_rect.bottom() - available_rect.bottom()) / dpi_scale)
        elif screen_rect.top() != available_rect.top():
            return int((available_rect.top() - screen_rect.top()) / dpi_scale)
        else:
            return int(40 / dpi_scale)

    def getSettingWindow(self, root_container):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    flork = Flork()
    flork.show()
    sys.exit(app.exec())