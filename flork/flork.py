
import random
import sys
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from pynput import keyboard

from utils.utils import get_taskbar_height


class Flork(QMainWindow):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent.parent  # Найти родительский каталог проекта
    # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable'/'flork'

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(1200, screen.height()-get_taskbar_height()-200, 200, 200)
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

        self.flork_main_pixmap = QPixmap(str(self.resource_path/"flork_main.png")).scaled( 200, 200,  Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.flork_left_pixmap = QPixmap(str(self.resource_path/"flork_left.png")).scaled( 200, 200,  Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.flork_right_pixmap = QPixmap(str(self.resource_path/"flork_right.png")).scaled( 200, 200,  Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
      
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

    def check_frame_change(self,frame_number):
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
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            
           if not self.isAnimationPlaying:
                random_int = random.randint(1,2)
                self.playAnimation(random_int)


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




if __name__ == "__main__":
    app = QApplication(sys.argv)
    flork = Flork()
    flork.show()
    sys.exit(app.exec())