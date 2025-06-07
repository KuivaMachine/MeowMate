from PyQt5.QtCore import Qt, QTimer, QPointF, pyqtSignal
from PyQt5.QtGui import QPainter, QBrush, QColor, QConicalGradient, QPen, QMovie
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect, QApplication

from utils.enums import ThemeColor


class CharacterCart(QLabel):
    clicked = pyqtSignal()
    character_name = None

    def __init__(self, parent, character_name, gif_path, size, speed):
        super().__init__()
        self.character_name = character_name
        self.setObjectName('card')
        self.scroll_area_instance = parent
        self.scroll_area_instance.controller_instance.theme_change_signal.connect(self.on_theme_change)
        self.isSelected = False
        self.current_theme = ThemeColor.LIGHT

        self.movie = QMovie(gif_path)
        self.movie.setSpeed(speed)
        self.movie.setCacheMode(QMovie.CacheMode.CacheAll)
        self.movie.setScaledSize(size)
        self.setMovie(self.movie)
        self.movie.start()
        self.movie.stop()

        self.setFixedSize(170, 170)
        self.angle = 0

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(255, 153, 102, 150))
        self.shadow.setOffset(-6, 6)
        self.setGraphicsEffect(self.shadow)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Таймер для анимации
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_angle)
        self.timer.start(11)

    def on_theme_change(self, theme):
        self.current_theme = theme
        if theme == ThemeColor.LIGHT:
            self.shadow.setColor(QColor(255, 153, 102, 150))
            self.shadow.setOffset(-6, 6)
            self.shadow.setBlurRadius(0)
        else:
            self.shadow.setColor(QColor(0, 0, 0, 0))
            if self.isSelected:
                self.shadow.setColor(QColor(255, 0, 98, 255))
                self.shadow.setOffset(0, 6)
                self.shadow.setBlurRadius(15)

    def update_angle(self):
        self.angle = (self.angle + 2) % 360  # Плавное изменение угла
        self.update()

    def mousePressEvent(self, event):
        if self.movie.state() != QMovie.MovieState.Running:
            self.movie.jumpToFrame(0)
            QApplication.processEvents()
        self.movie.start()
        self.isSelected = True
        self.clicked.emit()  # Отправляем сигнал при клике

        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.isSelected:
            self.movie.start()
            # 20% ПРОЗРАЧНЫЙ ОСВЕТЛЯЮЩИЙ КВАДРАТ
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 18, 18)

            # ГРАДИЕНТНАЯ ЦВЕТНАЯ ОБВОДКА
            gradient = QConicalGradient()  # Конический градиент
            gradient.setCenter(QPointF(self.rect().center()))
            gradient.setAngle(self.angle)  # Текущий угол анимации

            if self.current_theme == ThemeColor.LIGHT:
                painter.setBrush(QBrush(QColor("#20FFFFFF")))
                gradient.setColorAt(0.05, QColor(255, 211, 0, 0))
                gradient.setColorAt(0.15, QColor(255, 211, 0, 255))
                gradient.setColorAt(0.20, QColor(255, 250, 0, 255))
                gradient.setColorAt(0.39, QColor(255, 255, 255, 0))

                gradient.setColorAt(0.59, QColor(255, 211, 0, 0))
                gradient.setColorAt(0.65, QColor(255, 211, 0, 255))
                gradient.setColorAt(0.70, QColor(255, 211, 0, 255))
                gradient.setColorAt(0.79, QColor(255, 211, 0, 0))

                gradient.setColorAt(0.90, QColor(255, 255, 255, 0))
            else:
                painter.setBrush(QBrush(QColor("#20000000")))
                gradient.setColorAt(0.0, QColor(255, 51, 51, 255))
                gradient.setColorAt(0.5, QColor(255, 174, 0, 255))
                gradient.setColorAt(0.99, QColor(255, 51, 51, 255))
                if self.current_theme == ThemeColor.DARK:
                    self.shadow.setColor(QColor(255, 129, 45, 255))
                    self.shadow.setOffset(0, 4)
                    self.shadow.setBlurRadius(10)

            # 3. Рисуем обводку с градиентом
            pen = QPen(QBrush(gradient), 5)
            painter.setPen(pen)
            painter.drawRoundedRect(2, 2, self.width() - 4, self.height() - 4, 18, 18)
        else:
            if self.current_theme == ThemeColor.DARK:
                self.shadow.setColor(QColor(0, 0, 0, 0))
            self.movie.stop()
            self.movie.start()
            self.movie.stop()
            # 1. Рисуем фон карточки
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        super().paintEvent(event)
