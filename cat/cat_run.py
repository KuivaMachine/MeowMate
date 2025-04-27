from PyQt6.QtCore import QPropertyAnimation, Qt, QPoint, QTimer, QEasingCurve
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QApplication, QLabel


class CatRun(QLabel):
    def __init__(self, cat_instance):
        super().__init__()
        self.cat = cat_instance
        self.setup_ui()
        self.setup_animation()

    def setup_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(self.cat.pos().x() + 140, screen.height() - 450, 1900, 450)

        # Оптимизация QLabel для анимации
        self.crazy_label = QLabel(self)
        self.crazy_label.setGeometry(0, 0, 900, 450)
        self.crazy_label.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.crazy_label.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        # Оптимизация загрузки GIF
        self.crazy_gif = QMovie("./cat/drawable/cat/cat_crazy.gif")
        self.crazy_gif.setCacheMode(QMovie.CacheMode.CacheAll)
        self.crazy_label.setMovie(self.crazy_gif)

    def setup_animation(self):
        # Анимация движения
        self.cat_run_animation = QPropertyAnimation(self.crazy_label, b"pos")
        self.cat_run_animation.setDuration(1800)
        self.cat_run_animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.cat_run_animation.setStartValue(QPoint(0, 0))
        self.cat_run_animation.setEndValue(QPoint(1200, 0))
        self.cat_run_animation.finished.connect(self.cleanup)

    def run_crazy_start(self):
        # Предварительная буферизация
        if self.crazy_gif.state() != QMovie.MovieState.Running:
            self.crazy_gif.jumpToFrame(0)
            QApplication.processEvents()  # Принудительная обработка событий

        self.show()
        self.raise_()
        self.crazy_gif.start()
        self.cat_run_animation.start()

    def cleanup(self):
        # Плавное завершение
        self.crazy_gif.stop()
        self.hide()

        # Отложенное удаление
        QTimer.singleShot(100, lambda: (
            self.crazy_label.deleteLater(),
            self.crazy_gif.deleteLater(),
            self.cat.cat_preparing(),
            self.cat.show(),
            self.deleteLater()
        ))