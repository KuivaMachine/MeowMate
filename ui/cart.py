from PyQt6.QtCore import Qt, QTimer, QPointF, pyqtSignal
from PyQt6.QtGui import QMovie, QPainter, QBrush, QColor, QConicalGradient, QPen
from PyQt6.QtWidgets import QLabel, QGraphicsDropShadowEffect

from utils.enums import Characters


class CharacterCart(QLabel):
    clicked = pyqtSignal(Characters)
    character = None
    def __init__(self, character, gif_path, size):
        super().__init__()
        self.character = character
        self.setStyleSheet("""
            QWidget {
                background-color: #FFE5BD;
                border: 2px solid #000000;
                border-radius: 20px;
            }
        """)
        self.isSelected = False

        self.movie = QMovie(gif_path)
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
        self.timer.start(11)  # ~33 FPS

    def update_angle(self):
        self.angle = (self.angle + 2) % 360  # Плавное изменение угла
        self.update()

    def mousePressEvent(self, event):
        self.movie.start()
        self.isSelected = True
        self.clicked.emit(self.character)  # Отправляем сигнал при клике
        event.accept()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)



        if self.isSelected:
            self.movie.start()
            # 1. Рисуем фон карточки
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#20ffffff")))
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)
            # 2. Создаем градиент для обводки
            gradient = QConicalGradient()  # Конический градиент (для кругового движения)
            gradient.setCenter(QPointF(self.rect().center()))
            gradient.setAngle(self.angle)  # Текущий угол анимации

            # Цвета градиента (прозрачный -> цвет -> прозрачный)
            gradient.setColorAt(0.05, QColor(255, 211, 0, 0))
            gradient.setColorAt(0.15, QColor(255, 211, 0, 255))
            gradient.setColorAt(0.20, QColor(255, 250, 0, 255))
            gradient.setColorAt(0.39, QColor(255, 255, 255, 0))

            gradient.setColorAt(0.59, QColor(255, 211, 0, 0))
            gradient.setColorAt(0.65, QColor(255, 211, 0, 255))
            gradient.setColorAt(0.70, QColor(255, 211, 0, 255))
            gradient.setColorAt(0.79, QColor(255, 211, 0, 0))

            gradient.setColorAt(0.90, QColor(255, 255, 255, 0))

            # 3. Рисуем обводку с градиентом
            pen = QPen(QBrush(gradient), 3)
            painter.setPen(pen)
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 15, 15)
        else:
            self.movie.stop()
            self.movie.start()
            self.movie.stop()
            # 1. Рисуем фон карточки
            painter.setPen(Qt.PenStyle.NoPen)
            # painter.setBrush(QBrush(QColor("#FFD09E")))
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        super().paintEvent(event)