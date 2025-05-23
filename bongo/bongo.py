import random
import sys
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout
from pynput import keyboard

from utils.enums import BongoType


class BongoApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.bongo = Bongo()
        self.bongo.show()

    def close_bongo(self):
        self.bongo.close()
        self.quit()

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

        self.bongo_type = BongoType.BONGO


        self.cat_main_pixmap = None
        self.right_pixmap = None
        self.left_pixmap = None
        self.drag_pos = None
        self.setMouseTracking(True)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(1200, 500, 392,392)


        self.cat = QLabel(self)
        self.cat.setGeometry(0, 0, 392, 392)
        self.cat.setMouseTracking(True)
        self.cat.setStyleSheet("""
        QLabel{
          background-color: transparent;
         border: none;
        }
        """)

        self.cat_piano_pixmap = QPixmap(str(self.resource_path / 'piano' / "cat_piano.png"))
        self.cat_piano_left_pixmap = QPixmap(str(self.resource_path / 'piano' / "cat_piano_left.png"))
        self.cat_piano_right_pixmap = QPixmap(str(self.resource_path / 'piano' / "cat_piano_right.png"))

        self.cat_rock_pixmap = QPixmap(str(self.resource_path / 'rock' / "cat_rock.png"))
        self.cat_rock_left_pixmap = QPixmap(str(self.resource_path / 'rock' / "cat_rock_left.png"))
        self.cat_rock_right_pixmap = QPixmap(str(self.resource_path / 'rock' / "cat_rock_right.png"))

        self.cat_classic_pixmap = QPixmap(str(self.resource_path / 'classic' / "cat_classic.png"))
        self.cat_classic_left_pixmap = QPixmap(str(self.resource_path / 'classic' / "cat_classic_left.png"))
        self.cat_classic_right_pixmap = QPixmap(str(self.resource_path / 'classic' / "cat_classic_right.png"))

        self.cat_guitar_pixmap = QPixmap(str(self.resource_path / 'guitar' / "cat_guitar.png"))
        self.cat_guitar_left_pixmap = QPixmap(str(self.resource_path / 'guitar' / "cat_guitar_left.png"))
        self.cat_guitar_right_pixmap = QPixmap(str(self.resource_path / 'guitar' / "cat_guitar_right.png"))

        self.cat_bongo_pixmap = QPixmap(str(self.resource_path / 'bongo' / "cat_bongo.png"))
        self.cat_bongo_left_pixmap = QPixmap(str(self.resource_path / 'bongo' / "cat_bongo_left.png"))
        self.cat_bongo_right_pixmap = QPixmap(str(self.resource_path / 'bongo' / "cat_bongo_right.png"))

        self.flag = True

        match self.bongo_type:
            case(BongoType.ROCK):
                self.cat_main_pixmap = self.cat_rock_pixmap
                self.left_pixmap = self.cat_rock_left_pixmap
                self.right_pixmap = self.cat_rock_right_pixmap
            case (BongoType.PIANO):
                self.cat_main_pixmap = self.cat_piano_pixmap
                self.left_pixmap = self.cat_piano_left_pixmap
                self.right_pixmap = self.cat_piano_right_pixmap
            case (BongoType.CLASSIC):
                self.cat_main_pixmap = self.cat_classic_pixmap
                self.left_pixmap = self.cat_classic_left_pixmap
                self.right_pixmap = self.cat_classic_right_pixmap
            case (BongoType.GUITAR):
                self.cat_main_pixmap = self.cat_guitar_pixmap
                self.left_pixmap = self.cat_guitar_left_pixmap
                self.right_pixmap = self.cat_guitar_right_pixmap
            case (BongoType.BONGO):
                self.cat_main_pixmap = self.cat_bongo_pixmap
                self.left_pixmap = self.cat_bongo_left_pixmap
                self.right_pixmap = self.cat_bongo_right_pixmap


        self.cat.setPixmap(self.cat_main_pixmap)
        # СЛУШАТЕЛЬ КЛАВИАТУРЫ
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()




    # ОБРАБОТКА НАЖАТИЯ НА КЛАВИАТУРУ
    def on_press(self, key):
        if self.flag:
            self.cat.setPixmap(self.left_pixmap)
            self.flag = False
        else:
            self.cat.setPixmap(self.right_pixmap)
            self.flag = True


    # ОБРАБОТКА ОТПУСКАНИЯ КЛАВИШИ КЛАВИАТУРЫ
    def on_release(self, key):
        self.cat.setPixmap(self.cat_main_pixmap)



    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_pos:
                # Вычисляем новую позицию
                new_pos = self.pos() + event.globalPosition().toPoint() - self.drag_pos

                # Получаем геометрию родительского окна
                parent_rect = QApplication.primaryScreen().geometry()

                left_maximum = parent_rect.left()-100
                right_maximum = parent_rect.right() -300
                top_maximum = parent_rect.top() -140
                bottom_maximum = parent_rect.bottom() - 240


                # Ограничиваем перемещение
                x = max(left_maximum,
                        min(new_pos.x(),
                            right_maximum))

                y = max(top_maximum,
                        min(new_pos.y(),
                            bottom_maximum))

                # Перемещаем виджет
                self.move(x, y)
                self.drag_pos = event.globalPosition().toPoint()
                event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None


if __name__ == "__main__":

    app = BongoApp(sys.argv)
    sys.exit(app.exec())