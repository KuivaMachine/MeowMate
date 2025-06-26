import sys
from pathlib import Path

from PyQt5.QtCore import QPropertyAnimation, Qt, QPoint, QEasingCurve, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QLabel


class CatRun(QLabel):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent.parent # Найти родительский каталог проекта
    # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable'/'cat'

    def __init__(self, cat_instance):
        super().__init__()
        self.cat_run_animation = None
        self.cat = cat_instance

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint

        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


        self.crazy_label = QLabel(self)


        # ГИФ КОТА, БЕГУЩЕГО ВПРАВО
        self.crazy_gif = QMovie(str(self.resource_path /"cat_crazy.gif"))
        self.crazy_gif.setScaledSize(QSize(900,450))
        self.crazy_gif.setCacheMode(QMovie.CacheMode.CacheAll)                  # Оптимизация загрузки GIF

        # ГИФ КОТА, БЕГУЩЕГО ВЛЕВО
        self.crazy_gif_backward = QMovie(str(self.resource_path / "cat_crazy_backward.gif"))
        self.crazy_gif_backward.setScaledSize(QSize(900,450))
        self.crazy_gif_backward.setCacheMode(QMovie.CacheMode.CacheAll)         # Оптимизация загрузки GIF


    def setup_animation(self, gif, direction_k=1):
        self.crazy_label.setMovie(gif)
        self.cat_run_animation = QPropertyAnimation(self.crazy_label, b"pos")
        self.cat_run_animation.setDuration(1800)
        self.cat_run_animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.cat_run_animation.setStartValue(QPoint(self.crazy_label.pos().x(), 0))
        self.cat_run_animation.setEndValue(QPoint(direction_k*1200, 0))
        self.cat_run_animation.finished.connect(self.cleanup)

    def run_crazy_start(self, x_cat):
        # Предварительная буферизация
        if self.crazy_gif.state() != QMovie.MovieState.Running:
            self.crazy_gif.jumpToFrame(0)
            QApplication.processEvents()  # Принудительная обработка событий
        self.show()
        self.raise_()  # Окно поверх остальных

        if x_cat<QApplication.primaryScreen().geometry().width()/2:
            self.setGeometry(x_cat, QApplication.primaryScreen().geometry().height() - 450, QApplication.primaryScreen().geometry().width()-x_cat, 450)
            self.crazy_label.setGeometry(0, 0, 900, 450)
            self.setup_animation(self.crazy_gif, 1)
            self.crazy_gif.start()
        else:
            self.setGeometry(0, QApplication.primaryScreen().geometry().height() - 450, x_cat+300, 450)
            self.crazy_label.setGeometry(self.width()-900, 0, 900, 450)
            self.setup_animation(self.crazy_gif_backward, -1)
            self.crazy_gif_backward.start()

        self.cat_run_animation.start()


    def cleanup(self):
        self.crazy_gif.stop()
        self.crazy_gif_backward.stop()
        self.hide()
        self.deleteLater()
        self.cat.cat_preparing()

