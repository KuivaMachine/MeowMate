from PyQt6.QtCore import QSize, Qt, QPropertyAnimation, pyqtSignal
from PyQt6.QtGui import QMovie, QPainter, QBrush, QColor, QPen, QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QGraphicsDropShadowEffect


class CircularLabel(QLabel):

    def __init__(self, parent, gif_path, color):
        super().__init__(parent)
        size = QSize(40, 40)
        self.setFixedSize(size)
        border_radius = self.height() // 2
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border-radius: {border_radius}px;
                border-width:0px;
            }}
        """)

        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(size)
        self.setMovie(self.movie)
        self.movie.start()
        self.movie.stop()


class CustomAnimatedButton(QPushButton):
    def __init__(self, text, gif_path, parent):
        super().__init__(parent)
        self._pressed = None
        self.setFixedSize(170, 55)
        self.setText(text)
        self.menu_window = parent
        self.setMouseTracking(True)
        self._hover = False
        self._radius_inner = self.height() // 2
        self._radius_upper = (self.height() + 4) // 2
        # Настройка шрифта
        self.font = QFont("JetBrains Mono", 13)

        self.font.setWeight(QFont.Weight.Bold)
        self.setFont(self.font)

        # Настройка гифки в круге
        self.gif_label = CircularLabel(self, gif_path, "#FFF2D6")
        self.gif_label.setMouseTracking(True)
        self.gif_label.move(
            self.width() - (self.gif_label.width() + ((self.height() + 2) - self.gif_label.height()) // 2),
            (self.height() - self.gif_label.height()) // 2)

        # Тень при наведении
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(0)
        self.shadow_effect.setColor(QColor(0, 0, 0, 250))
        self.shadow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow_effect)

        # Анимация тени
        self.shadow_animation = QPropertyAnimation(self.shadow_effect, b"blurRadius")
        self.shadow_animation.setDuration(120)



    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self._hover = True
        # Анимация появления тени
        self.shadow_animation.stop()
        self.shadow_animation.setStartValue(0)
        self.shadow_animation.setEndValue(15)
        self.shadow_animation.start()
        self.gif_label.movie.start()
        if (self.text() == 'НАСТРОИТЬ'):
            self.menu_window.startGearsAnimation()
        if (self.text() == 'ЗАПУСТИТЬ'):
            self.menu_window.startRocketsAnimation()

        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        # Анимация исчезновения тени
        self.shadow_animation.stop()
        self.shadow_animation.setStartValue(15)
        self.shadow_animation.setEndValue(0)
        self.shadow_animation.start()
        self.gif_label.movie.stop()

        if (self.text() == 'НАСТРОИТЬ'):
            self.menu_window.hideGearsAnimation()
        if (self.text() == 'ЗАПУСТИТЬ'):
            self.menu_window.hideRocketsAnimation()

        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._pressed:

            # 1. Рисуем фон
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#FFBC75")))
            painter.drawRoundedRect(3, 3, self.width() - 6, self.height() - 6, self._radius_inner, self._radius_inner)

            # 4. Рисуем текст слева
            painter.setPen(QPen(QColor("black")))
            text_rect = self.rect().adjusted(25, 0, 0, 0)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text())
        else:
            # 2. Анимированная обводка при наведении
            if self._hover:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor("#000000")))
                painter.drawRoundedRect(0, 0, self.width(), self.height(), self._radius_upper, self._radius_upper)

            # 1. Рисуем фон
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#FFBC75")))
            painter.drawRoundedRect(3, 3, self.width() - 6, self.height() - 6, self._radius_inner, self._radius_inner)

            # 4. Рисуем текст слева
            painter.setPen(QPen(QColor("black")))
            text_rect = self.rect().adjusted(25, 0, 0, 0)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text())
