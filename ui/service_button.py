from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QPushButton

from utils.utils import svg_to_icon


class ServiceButton(QPushButton):
    def __init__(self, path):
        super().__init__()

        self.setFixedSize(30, 30)
        self.setObjectName('service_buttons')
        self.setIcon(svg_to_icon(path))
        self.setIconSize(QSize(30, 30))

