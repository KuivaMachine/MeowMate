from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtSvg import QSvgRenderer

from utils.enums import ThemeColor


def svg_to_icon(path, size=30):
    renderer = QSvgRenderer(path)
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)



