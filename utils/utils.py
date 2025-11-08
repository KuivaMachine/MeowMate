import winreg

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtSvg import QSvgRenderer

from utils.enums import BongoType

# Константы WinAPI
ABM_GETTASKBARPOS = 0x00000005
ABE_BOTTOM = 3

# ИЩЕМ ФЛАГ ПЕРВОГО ЗАПУСКА ДЛЯ ОТОБРАЖЕНИЯ ОКНА ИЗМЕНЕНИЙ
def check_is_first_run():
    # Путь к ключу в реестре
    reg_path = r"Software\KuivaMachine\MeowMate"
    key_name = "is_first_run"

    try:
        # Открываем ключ для чтения (HKEY_CURRENT_USER)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ) as key:
            value, reg_type = winreg.QueryValueEx(key, key_name)
            print(value)
            if value == b'\x01':
                print("Первый запуск")
                # Переоткрываем ключ для записи
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as w_key:
                    winreg.SetValueEx(w_key, key_name, 0, winreg.REG_BINARY, b'\x00')  # Записываем 0 (байты)
                return True
            else:
                print("Не первый запуск")
                return False
    except FileNotFoundError:
        print("Ключ реестра не найден!")
        return True

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
