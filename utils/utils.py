import ctypes
from ctypes import wintypes

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication

# Константы WinAPI
ABM_GETTASKBARPOS = 0x00000005
ABE_BOTTOM = 3


class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", wintypes.RECT),
        ("lParam", wintypes.LPARAM),
    ]


def get_taskbar_height():
    """Альтернативный метод через Qt"""
    screen = QApplication.primaryScreen()
    screen_rect = screen.geometry()
    available_rect = screen.availableGeometry()
    dpi_scale = screen.devicePixelRatio()

    if screen_rect.bottom() != available_rect.bottom():  # Панель снизу
        return int((screen_rect.bottom() - available_rect.bottom()) / dpi_scale)
    elif screen_rect.top() != available_rect.top():  # Панель сверху
        return int((available_rect.top() - screen_rect.top()) / dpi_scale)
    else:  # Панель слева/справа или скрыта
        return int(40 / dpi_scale)  # Стандартное значение с масштабом

def svg_to_icon(path, size=30):
    renderer = QSvgRenderer(path)
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)



