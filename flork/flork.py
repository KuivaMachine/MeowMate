
import random
import sys
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from pynput import keyboard


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
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(1200, screen.height()-240, 200, 200)
        self.setMouseTracking(True)
        
        self.flork_gif = QMovie(str(self.resource_path/"flork_shy.gif"))
        self.flork_gif.setScaledSize(QSize(200,200))
  
        self.flork_main_pixmap = QPixmap(str(self.resource_path/"flork_main.png")).scaled( 200, 200,  Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.flork_left_pixmap = QPixmap(str(self.resource_path/"flork_left.png")).scaled( 200, 200,  Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.flork_right_pixmap = QPixmap(str(self.resource_path/"flork_right.png")).scaled( 200, 200,  Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
      
        self.flork_main = QLabel(self)
        self.flork_main.setMouseTracking(True)
        self.flork_main.setPixmap(self.flork_main_pixmap)
        self.flork_main.setGeometry(0, 0, 200, 200)

        self.flag = True
        self.isAnimationPlaying = False

        # СЛУШАТЕЛЬ КЛАВИАТУРЫ
        self.listener = keyboard.Listener(
            on_press=self.on_press, 
            on_release=self.on_release
        )
        self.listener.start()

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
  
    def on_gif_finished(self):
        self.flork_gif.stop()
        self.flork_main.setPixmap(self.flork_main_pixmap)
        self.isAnimationPlaying = False
   
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            
           if not self.isAnimationPlaying:
                random_int = random.randint(0,1)
                self.playAnimation(1)


    def playAnimation(self, number):     
        match number:
            case (1):
                self.flork_gif.start()
                self.flork_main.setMovie(self.flork_gif)
        QTimer.singleShot(3800, self.on_gif_finished)  
        self.isAnimationPlaying = True




if __name__ == "__main__":
    app = QApplication(sys.argv)
    flork = Flork()
    flork.show()
    sys.exit(app.exec())