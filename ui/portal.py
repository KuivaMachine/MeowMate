import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, QSize, QPoint
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QLabel


class Portal(QWidget):

    app_directory = Path(__file__).parent.parent
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
        QTimer.singleShot(2400, self.close)

    def closeEvent(self, event):
        self.portal_gif.stop()
        self.portal_gif.deleteLater()
        self.hide()
        self.deleteLater()