import os
import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

from ui.custom_button import CircularLabel


class CharacterCart(QLabel):


    def __init__(self):
        super().__init__()

        self.setFixedSize(70, 70)





class BongoApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.bongo = CircularLabel(self,'ds')
        self.bongo.show()

if __name__ == "__main__":

    app = BongoApp(sys.argv)
    sys.exit(app.exec())