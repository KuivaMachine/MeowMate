import os
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from pynput import keyboard


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Настройки окна
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 300)

        # Настройка WebView
        self.webview = QWebEngineView()
        self.webview.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        self.webview.setAttribute(Qt.WA_TranslucentBackground, True)
        self.webview.page().setBackgroundColor(Qt.transparent)

        # Загрузка HTML
        html_path = os.path.abspath("cat.html")
        self.webview.load(QUrl.fromLocalFile(html_path))

        self.setCentralWidget(self.webview)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())