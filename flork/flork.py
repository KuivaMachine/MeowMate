import random
import sys
from pathlib import Path

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QLabel
from pynput import keyboard

from flork.flork_settings import FlorkSettingsWindow
from utils.character_abstract import Character




def get_taskbar_height():
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


class Flork(Character):

    app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'flork'

    def __init__(self, settings):
        super().__init__()

        self.size = settings["size"]
        self.drag_pos = None
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.screen = QApplication.primaryScreen().geometry()
        self.setGeometry(100, self.screen.height() - get_taskbar_height() - self.size, self.size, self.size)
        self.setMouseTracking(True)

        self.current_gif = None

        self.flork_main_pixmap = QPixmap(str(self.resource_path / "flork_main.png")).scaled(self.size, self.size,
                                                                                            Qt.AspectRatioMode.KeepAspectRatio,
                                                                                            Qt.TransformationMode.SmoothTransformation)
        self.flork_left_pixmap = QPixmap(str(self.resource_path / "flork_left.png")).scaled(self.size, self.size,
                                                                                            Qt.AspectRatioMode.KeepAspectRatio,
                                                                                            Qt.TransformationMode.SmoothTransformation)
        self.flork_right_pixmap = QPixmap(str(self.resource_path / "flork_right.png")).scaled(self.size, self.size,
                                                                                              Qt.AspectRatioMode.KeepAspectRatio,
                                                                                              Qt.TransformationMode.SmoothTransformation)

        self.flork_main = QLabel(self)
        self.flork_main.setMouseTracking(True)
        self.flork_main.setPixmap(self.flork_main_pixmap)
        self.flork_main.setGeometry(0, 0, self.size, self.size)

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
    def on_press(self, _):
        if self.flag:
            self.flork_main.setPixmap(self.flork_left_pixmap)
            self.flag = False
        else:
            self.flork_main.setPixmap(self.flork_right_pixmap)
            self.flag = True

    # ОБРАБОТКА ОТПУСКАНИЯ КЛАВИШИ КЛАВИАТУРЫ
    def on_release(self, _):
        self.flork_main.setPixmap(self.flork_main_pixmap)

    def stopAnimation(self):
        self.current_gif.stop()
        self.flork_main.setPixmap(self.flork_main_pixmap)
        self.isAnimationPlaying = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.isAnimationPlaying:
                random_int = random.randint(1, 7)
                self.playAnimation(random_int )

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_pos:
                new_pos = self.pos() + event.globalPos() - self.drag_pos
                parent_rect = QApplication.primaryScreen().geometry()

                left_maximum = parent_rect.left() - 20
                right_maximum = parent_rect.right() - self.size

                x = max(left_maximum,
                        min(new_pos.x(),
                            right_maximum))

                self.move(x, self.screen.height() - get_taskbar_height() - self.size)
                self.drag_pos = event.globalPos()

    def playAnimation(self, number):
        match number:
            case (1):
                self.current_gif = QMovie(str(self.resource_path / "flork_shy.gif"))
            case (2):
                self.current_gif = QMovie(str(self.resource_path / "flork_dance.gif"))
            case (3):
                self.current_gif = QMovie(str(self.resource_path / "flork_cool.gif"))
            case (4):
                self.current_gif = QMovie(str(self.resource_path / "flork_rock.gif"))
            case (5):
                self.current_gif = QMovie(str(self.resource_path / "flork_heart.gif"))
            case (6):
                self.current_gif = QMovie(str(self.resource_path / "flork_birthday.gif"))
            case (7):
                self.current_gif = QMovie(str(self.resource_path / "flork_fingers.gif"))

        self.current_gif.setScaledSize(QSize(self.size, self.size))
        self.current_gif.setSpeed(120)
        self.current_gif.frameChanged.connect(self.check_frame_change)
        self.current_gif.start()
        self.flork_main.setMovie(self.current_gif)
        self.isAnimationPlaying = True

    @staticmethod
    def getSettingWindow(root_container, settings):
        return FlorkSettingsWindow(root_container, settings)
