import ctypes
from ctypes import wintypes

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QApplication

# Константы WinAPI
ABM_GETTASKBARPOS = 0x00000005
ABE_BOTTOM = 3







def svg_to_icon(path, size):
    renderer = QSvgRenderer(path)
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


def svg_to_pixmap(svg_path: str, size: int) -> QPixmap:
    renderer = QSvgRenderer(svg_path)
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)  # Прозрачный фон
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap
