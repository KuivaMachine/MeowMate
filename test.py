import sys

from PyQt6.QtGui import QColor
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(500,500,300,400)

        # Настройка WebView
        self.webview = QWebEngineView()
        self.webview.page().setBackgroundColor(QColor(0, 0, 0, 0))  # Полностью прозрачный
        file_path = os.path.abspath("./card.html")  # Путь к HTML-файлу
        self.webview.load(QUrl.fromLocalFile(file_path))
        self.webview.setStyleSheet("background: transparent;")
        self.webview.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, False)  # Отключаем тач-события
        self.webview.setAttribute(Qt.WidgetAttribute.WA_Hover, True)  # Включаем hover
        self.webview.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Разрешаем фокус
        self.webview.settings().setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled, True
        )
        self.webview.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
        )
        self.setCentralWidget( self.webview)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL)
    window = MainWindow()
    window.show()
    app.exec()