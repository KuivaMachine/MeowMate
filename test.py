import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget

from utils.utils import get_taskbar_height, svg_to_pixmap

QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)

class Test(QMainWindow):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent  # Найти родительский каталог проекта
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
        self.setMouseTracking(True)

        self.screen_scale = self.get_screen_scale()
        self.base_size = 200
        self.scaled_size = int(self.base_size * self.screen_scale)
        content = QWidget()
        self.hbox = QHBoxLayout(content)


        self.flork_main = QSvgWidget( str(self.resource_path / "flork.svg"))
        self.flork_main.setFixedSize(self.scaled_size,self.scaled_size)


        self.flork_main_pixmap2 = QPixmap(str(self.resource_path / "flork_main_BIG.png")).scaled(200, 200,
                                                                                            Qt.AspectRatioMode.KeepAspectRatio,
                                                                                            Qt.TransformationMode.SmoothTransformation)

        self.flork_main2 = QLabel()
        self.flork_main2.setMouseTracking(True)
        self.flork_main2.setPixmap(self.flork_main_pixmap2)


        self.setGeometry(100, screen.height()-get_taskbar_height()-self.scaled_size, self.scaled_size, self.scaled_size)
        self.hbox.addWidget(self.flork_main)
        self.hbox.addWidget(self.flork_main2)

        self.setCentralWidget(content)


    def get_screen_scale(self):
        screen = QGuiApplication.primaryScreen()
        logical_dpi = screen.logicalDotsPerInch()
        return logical_dpi / 96.0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    flork = Test()
    flork.show()
    sys.exit(app.exec())