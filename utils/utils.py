from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtSvg import QSvgRenderer


def svg_to_icon(path, size=100):
    renderer = QSvgRenderer(path)
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)