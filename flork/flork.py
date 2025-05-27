import os
import sys

from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QMainWindow
from pynput import keyboard




class Flork(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(1200, QApplication.primaryScreen().geometry().height()-self.get_taskbar_height()-200, 200, 200)

        # Настройка WebView
        self.webview = QWebEngineView()
        self.setMouseTracking(True)
        self.webview.setMouseTracking(True)
        self.webview.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        self.webview.setAttribute(Qt.WA_TranslucentBackground, True)
        self.webview.page().setBackgroundColor(Qt.transparent)

        # Загрузка HTML
        html_path = os.path.abspath("flork.html")
        self.webview.load(QUrl.fromLocalFile(html_path))

        self.setCentralWidget(self.webview)

        self.flag = True

        self.isAnimationPlaying = False

        # СЛУШАТЕЛЬ КЛАВИАТУРЫ
        self.listener = keyboard.Listener(
            on_press=self.on_press, 
            on_release=self.on_release
        )
        self.listener.start()


    def get_taskbar_height(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        available_rect = screen.availableGeometry()
        dpi_scale = screen.devicePixelRatio()

        if screen_rect.bottom() != available_rect.bottom():  # Панель снизу
            return int((screen_rect.bottom() - available_rect.bottom()) / dpi_scale)
        elif screen_rect.top() != available_rect.top():  # Панель сверху
            return int((available_rect.top() - screen_rect.top()) / dpi_scale)
        else:  # Панель слева/справа или скрыта
            return int(40 / dpi_scale)  # Стандартное значение с масштабом

    # ОБРАБОТКА НАЖАТИЯ НА КЛАВИАТУРУ
    def on_press(self,key):
        QTimer.singleShot(0, self.change_flork_hand)

    # ОБРАБОТКА ОТПУСКАНИЯ КЛАВИШИ КЛАВИАТУРЫ
    def on_release(self, key):
        QTimer.singleShot(0, self.set_default_image)


    def change_flork_hand(self):
        if self.flag:
            direction = "left"
            self.flag = False
        else:
            direction = "right"
            self.flag = True
        script_code = f"changeState('{direction}');"
        self.webview.page().runJavaScript(script_code)

    def set_default_image(self):
        self.webview.page().runJavaScript(
                "changeState('idle');")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    flork = Flork()
    flork.show()
    sys.exit(app.exec())