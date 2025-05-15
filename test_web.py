import os
import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag_pos = None
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(500, 500, 200, 200)

        self.webview = QWebEngineView()
        self.webview.setAttribute(Qt.WA_TranslucentBackground, True)
        self.webview.setStyleSheet("background: transparent;")

        file_path = os.path.abspath("./card.html")  # Путь к HTML-файлу
        self.webview.load(QUrl.fromLocalFile(file_path))

        self.setCentralWidget(self.webview)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
