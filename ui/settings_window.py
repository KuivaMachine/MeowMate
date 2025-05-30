import json
import sys
from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton


class OkButton(QPushButton):
    def __init__(self,parent,name):
        super().__init__(parent)
        self.setFixedSize(90, 40)
        self.setObjectName(name)
        self.setText('Готово')


class SettingsWindow(QLabel):


    def __init__(self, parent):
        super().__init__(parent)
        self.drag_position = None
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput)

        self.setGeometry((parent.size().width() - self.width())//3, (parent.size().height() - self.height())//8,
                         320, 460)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_position is not None:
                # Новая позиция окна относительно родительского виджета
                new_position = event.globalPos() - self.drag_position
                parent_geometry = self.parent().frameGeometry()
                window_size = self.geometry()

                # Ограничиваем перемещение окна внутри родительского виджета
                x = max(0, min(new_position.x(), parent_geometry.width() - window_size.width()))
                y = max(0, min(new_position.y(), parent_geometry.height() - window_size.height()))

                # Перемещаем окно
                self.move(x, y)
                event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()

