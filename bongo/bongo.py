import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from pynput import keyboard

from ui.alert_window import AlertWindow
from utils.enums import BongoType


# TODO:НАСТРОЙКИ:
# Выключить звуки
# Выбрать инструмент
# Включить счетчик нажатий

class BongoApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.bongo = Bongo()
        self.bongo.show()

    def close_bongo(self):
        self.bongo.close()
        self.quit()


class CloseButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setStyleSheet("""QPushButton {
    color: black;
    font-size: 17px;
    font-weight: bold;
    font-family: 'JetBrains Mono';
    background-color: #FF7A73;
    border: 3px solid black;
    border-radius:15px;
}""")
        self.setText('x')


class Bongo(QMainWindow):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent.parent  # Найти родительский каталог проекта
    # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable' / 'bongo'

    def __init__(self):
        super().__init__()

        self.is_close_btn_showing = False
        self.bongo_type = BongoType.CLASSIC

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
        self.setGeometry(100, 100, 100, 100)

        self.root_container = QWidget()

        self.hbox = QHBoxLayout(self.root_container)
        self.hbox.setContentsMargins(0, 0, 0, 0)

        self.cat = QSvgWidget()
        self.cat.setFixedSize(392, 392)
        self.cat.setMouseTracking(True)

        self.cat_piano_pixmap = str(self.resource_path / 'piano' / "cat_piano.svg")
        self.cat_piano_left_pixmap = str(self.resource_path / 'piano' / "cat_piano_left.svg")
        self.cat_piano_right_pixmap = str(self.resource_path / 'piano' / "cat_piano_right.svg")

        self.cat_rock_pixmap = str(self.resource_path / 'rock' / "cat_rock.svg")
        self.cat_rock_left_pixmap = str(self.resource_path / 'rock' / "cat_rock_left.svg")
        self.cat_rock_right_pixmap = str(self.resource_path / 'rock' / "cat_rock_right.svg")

        self.cat_classic_pixmap = str(self.resource_path / 'classic' / "cat_classic.svg")
        self.cat_classic_left_pixmap = str(self.resource_path / 'classic' / "cat_classic_left.svg")
        self.cat_classic_right_pixmap = str(self.resource_path / 'classic' / "cat_classic_right.svg")

        self.cat_guitar_pixmap = str(self.resource_path / 'guitar' / "cat_guitar.svg")
        self.cat_guitar_left_pixmap = str(self.resource_path / 'guitar' / "cat_guitar_left.svg")
        self.cat_guitar_right_pixmap = str(self.resource_path / 'guitar' / "cat_guitar_right.svg")

        self.cat_bongo_pixmap = str(self.resource_path / 'bongo' / "cat_bongo.svg")
        self.cat_bongo_left_pixmap = str(self.resource_path / 'bongo' / "cat_bongo_left.svg")
        self.cat_bongo_right_pixmap = str(self.resource_path / 'bongo' / "cat_bongo_right.svg")

        self.flag = True

        match self.bongo_type:
            case (BongoType.ROCK):
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

        self.cat.load(self.cat_main_pixmap)
        self.hbox.addWidget(self.cat)
        self.setCentralWidget(self.root_container)
        # СЛУШАТЕЛЬ КЛАВИАТУРЫ
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    # ОБРАБОТКА НАЖАТИЯ НА КЛАВИАТУРУ
    def on_press(self, key):
        if self.flag:
            self.cat.load(self.left_pixmap)
            self.flag = False
        else:
            self.cat.load(self.right_pixmap)
            self.flag = True

    # ОБРАБОТКА ОТПУСКАНИЯ КЛАВИШИ КЛАВИАТУРЫ
    def on_release(self, key):
        self.cat.load(self.cat_main_pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPos()
        if event.button() == Qt.MouseButton.RightButton:
            if not self.is_close_btn_showing:
                self.close = CloseButton(self)
                self.close.setGeometry(280, 100, 30, 30)
                self.close.clicked.connect(self.close)
                self.close.show()
                self.is_close_btn_showing = True
            else:
                self.close.close()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_pos:
                # Вычисляем новую позицию
                new_pos = self.pos() + event.globalPos() - self.drag_pos

                # Получаем геометрию родительского окна
                parent_rect = QApplication.primaryScreen().geometry()

                left_maximum = parent_rect.left() - 100
                right_maximum = parent_rect.right() - 300
                top_maximum = parent_rect.top() - 140
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
                self.drag_pos = event.globalPos()
                event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def getSettingWindow(self, root_container):
        return AlertWindow(root_container)


if __name__ == "__main__":
    app = BongoApp(sys.argv)
    sys.exit(app.exec())
