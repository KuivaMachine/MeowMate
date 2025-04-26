from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QMovie, QPainter, QBrush, QColor, QConicalGradient, QPen
from PyQt6.QtWidgets import QLabel, QGraphicsDropShadowEffect, QGraphicsBlurEffect


class AnimalCart(QLabel):
    def __init__(self, gif_path, size):
        super().__init__()
        # Загрузка гифки
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(size)
        self.setMovie(self.movie)
        self.movie.start()
        self.setFixedSize(200, 200)
        self.angle = 0
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(255, 153, 102, 150))
        self.shadow.setOffset(6, 6)
        self.setGraphicsEffect(self.shadow)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(4)  # Начальное значение - нет размытия

        # Применяем эффект ко всему виджету
        # self.setGraphicsEffect(self.blur_effect)

        # Таймер для анимации
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_angle)
        self.timer.start(11)  # ~33 FPS

    def update_angle(self):
        self.angle = (self.angle + 2) % 360  # Плавное изменение угла
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Рисуем фон карточки
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#00312121")))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 20, 20)

        # 2. Создаем градиент для обводки
        gradient = QConicalGradient()  # Конический градиент (для кругового движения)
        gradient.setCenter(QPointF(self.rect().center()))
        gradient.setAngle(self.angle)  # Текущий угол анимации

        # Цвета градиента (прозрачный -> цвет -> прозрачный)
        gradient.setColorAt(0.09, QColor(255, 211, 0, 0))
        gradient.setColorAt(0.15, QColor(255, 211, 0, 255))
        gradient.setColorAt(0.20, QColor(255, 211, 0, 255))
        gradient.setColorAt(0.29, QColor(255, 255, 255, 0))

        gradient.setColorAt(0.59, QColor(255, 211, 0, 0))
        gradient.setColorAt(0.65, QColor(255, 211, 0, 255))
        gradient.setColorAt(0.70, QColor(255, 211, 0, 255))
        gradient.setColorAt(0.79, QColor(255, 211, 0, 0))

        gradient.setColorAt(0.90, QColor(255, 255, 255, 0))

        # 3. Рисуем обводку с градиентом
        pen = QPen(QBrush(gradient), 2)
        painter.setPen(pen)
        painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 20, 20)

        super().paintEvent(event)