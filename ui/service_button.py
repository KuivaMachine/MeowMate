import re

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget

from PyQt5.QtWidgets import QPushButton, QWidget

from utils.utils import svg_to_icon


class SvgButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, svg_file_path):
        super().__init__()
        self.path = svg_file_path
        self.icon = QSvgWidget(self)
        self.icon.load(svg_file_path)
        self.setFixedSize(30, 30)
        self.icon.setFixedSize(30, 30)

    def setupIcon(self, path):
        self.path=path
        self.icon.load(path)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        match = 'white' in self.path.lower()
        color = '#FFFFFF' if match else '#000000'
        self.setStyleSheet(f"""
        QWidget {{
            border: 2px solid {color};
            border-radius: 6px;
        }}
        """)

    def leaveEvent(self, event):
        self.setStyleSheet("""
        QWidget {
            border: none;
            border-radius: 6px;
        }
        """)

