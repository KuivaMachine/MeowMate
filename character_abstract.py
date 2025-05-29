from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from ui.close_characher_btn import CloseButton


class Character (QMainWindow):
    def __init__(self):
        super().__init__()
        self.close_button = None
        self.is_close_btn_showing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.close_button.close()
            self.is_close_btn_showing = False
        if event.button() == Qt.MouseButton.RightButton:
            if not self.is_close_btn_showing:
                self.close_button = CloseButton(self)
                self.close_button.setGeometry(event.globalPos().x()-self.pos().x(), event.globalPos().y()-self.pos().y()-30, 30, 30)
                self.close_button.clicked.connect(self.close)
                self.close_button.show()
                self.is_close_btn_showing = True
            else:
                self.close_button.close()
                self.is_close_btn_showing = False