from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtSvg import QSvgRenderer

from utils.enums import BongoType

# Константы WinAPI
ABM_GETTASKBARPOS = 0x00000005
ABE_BOTTOM = 3


def get_taskbar_height(screen):
    screen_rect = screen.geometry()
    available_rect = screen.availableGeometry()
    dpi_scale = screen.devicePixelRatio()

    if screen_rect.bottom() != available_rect.bottom():
        return int((screen_rect.bottom() - available_rect.bottom()) / dpi_scale)
    elif screen_rect.top() != available_rect.top():
        return int((available_rect.top() - screen_rect.top()) / dpi_scale)
    else:
        return int(40 / dpi_scale)


def get_bongo_enum( value):
    for item in BongoType:
        if item.value == value:
            return item




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
