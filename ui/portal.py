import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, QSize, QPoint
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush, QMovie
from PyQt5.QtWidgets import QWidget, QApplication, QLabel

class Portal(QWidget):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent.parent # Найти родительский каталог проекта

    # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable'/'menu'

    def __init__(self,position=QPoint(1500,700)):
        super().__init__()


        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(position.x(),position.y(),360,400)

        self.portal = QLabel(self)

        self.portal_gif = QMovie(str(self.resource_path /'portal.gif') )
        self.portal_gif.setScaledSize(QSize(360,400))
        self.portal.setMovie(self.portal_gif)
        self.portal_gif.setSpeed(120)
        self.portal_gif.start()


        QTimer.singleShot(3350, self.on_gif_finished)

    def on_gif_finished(self):
        self.portal_gif.stop()
        self.portal_gif.deleteLater()
        self.hide()
        self.deleteLater()