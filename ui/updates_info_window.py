from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout


class UpdateInfoWindow(QLabel):

    def __init__(self, parent, title, whats_new):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(490, 370)
        self.move(parent.frameGeometry().center() - self.rect().center())
        self.setObjectName('updates_info_window')
        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(20, 0, 20, 0)
        self.title = QLabel(title)
        self.title.setObjectName('updates_info_window_title')
        self.whats_new = QLabel(whats_new)
        self.whats_new.setObjectName('updates_info_window_whats_new')
        self.ok_button = QPushButton("Ясненько")
        self.ok_button.setObjectName('updates_info_window_ok_button')
        self.ok_button.clicked.connect(self.close)
        self.vbox.addWidget(self.title, alignment=Qt.AlignCenter)
        self.vbox.addWidget(self.whats_new)
        self.vbox.addWidget(self.ok_button, alignment=Qt.AlignCenter)
