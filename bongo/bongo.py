import random
import sys
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from pynput import keyboard


class Bongo(QMainWindow):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent.parent # Найти родительский каталог проекта
    # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable' / 'bongo'

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(1200, 500, 230,230)


        self.bongo = QLabel(self)
        self.bongo.setStyleSheet("""
        QLabel{
          background-color: transparent;
         border: none;
        }
        """)
        self.bongo_main_pixmap = QPixmap(str(self.resource_path / 'piano'/"cat_piano.png"))
        self.bongo.setGeometry(0,0,230,171)
        self.bongo.setPixmap(self.bongo_main_pixmap)
        self.bongo_left_pixmap = QPixmap(str(self.resource_path / 'piano'/"cat_piano_left.png"))
        self.bongo_right_pixmap = QPixmap(str(self.resource_path / 'piano'/"cat_piano_right.png"))
        self.flag = True

        # СЛУШАТЕЛЬ КЛАВИАТУРЫ
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    # ОБРАБОТКА НАЖАТИЯ НА КЛАВИАТУРУ
    def on_press(self, key):
        if self.flag:
            print('here')
            self.bongo.setPixmap(self.bongo_left_pixmap)
            self.flag = False
        else:
            self.bongo.setPixmap(self.bongo_right_pixmap)
            self.flag = True


    # ОБРАБОТКА ОТПУСКАНИЯ КЛАВИШИ КЛАВИАТУРЫ
    def on_release(self, key):
        self.bongo.setPixmap(self.bongo_main_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bongo = Bongo()
    bongo.show()
    sys.exit(app.exec())
