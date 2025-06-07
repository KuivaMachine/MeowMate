import sys
from pathlib import Path

from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, pyqtSignal
from PyQt5.QtGui import QMovie, QPainter, QBrush, QColor, QLinearGradient, QPen
from PyQt5.QtWidgets import QLabel, QPushButton, QGraphicsDropShadowEffect

from utils.enums import ThemeColor


class CircularLabel(QLabel):

    def __init__(self, parent, gif_path):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setObjectName('circle_in_start_settings_buttons')
        self.size = QSize(40, 40)
        self.movie = None
        self.setFixedSize(self.size)
        self.gif = QMovie(gif_path)
        self.gif.setScaledSize(self.size)
        self.setMovie(self.gif)
        self.gif.start()
        self.gif.stop()
        self.movie = self.gif

    def set_gif(self, path):
        new_movie = QMovie(path)
        new_movie.setScaledSize(self.size)
        self.setMovie(new_movie)
        new_movie.start()
        new_movie.stop()
        self.movie = new_movie



class CustomAnimatedButton(QPushButton):
    settings_button_clicked = pyqtSignal()
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'menu'
    def __init__(self, text, gif_path, parent):
        super().__init__(parent)
        self.setObjectName('custom_buttons')
        self._pressed = None
        self.setFixedSize(170, 55)
        self.setText(text)
        self.menu_window = parent
        self.menu_window.parent.theme_change_signal.connect(self.update_gif_on_theme_change)
        self.setMouseTracking(True)
        self._hover = False
        self._radius_inner = self.height() // 2
        self._radius_upper = (self.height() + 4) // 2

        # Настройка гифки в круге
        self.gif_label = CircularLabel(self, gif_path)
        self.gif_label.setMouseTracking(True)
        self.gif_label.move(
            self.width() - (self.gif_label.width() + ((self.height() + 2) - self.gif_label.height()) // 2),
            (self.height() - self.gif_label.height()) // 2)

        # Тень при наведении
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(0)
        self.shadow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow_effect)

        # Анимация тени
        self.shadow_animation = QPropertyAnimation(self.shadow_effect, b"blurRadius")
        self.shadow_animation.setDuration(120)

    def update_gif_on_theme_change(self, new_theme):
        if self.text() == 'НАСТРОИТЬ':
            if new_theme == ThemeColor.DARK:
                self.gif_label.set_gif(str(self.resource_path/'gears_mini_white.gif'))
            else:
                self.gif_label.set_gif(str(self.resource_path/'gears_mini.gif'))

    def mousePressEvent(self, event, ):
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
        if self.menu_window.parent.theme_color == ThemeColor.LIGHT:
            self.shadow_effect.setColor(QColor(0, 0, 0, 250))
        else:
            if self.text() == 'НАСТРОИТЬ':
                self.shadow_effect.setColor(QColor(85, 212, 0, 250))
            if self.text() == 'ЗАПУСТИТЬ':
                self.shadow_effect.setColor(QColor(251, 6, 173, 250))

        self.shadow_animation.setStartValue(0)
        self.shadow_animation.setEndValue(15)
        self.shadow_animation.start()
        self.gif_label.movie.start()
        if self.text() == 'НАСТРОИТЬ':
            self.menu_window.start_gears_animation()
        if self.text() == 'ЗАПУСТИТЬ':
            self.menu_window.start_rockets_animation()

        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        # Анимация исчезновения тени
        self.shadow_animation.stop()
        self.shadow_animation.setStartValue(15)
        self.shadow_animation.setEndValue(0)
        self.shadow_animation.start()
        self.gif_label.movie.stop()

        if self.text() == 'НАСТРОИТЬ':
            self.menu_window.hide_gears_animation()
        if self.text() == 'ЗАПУСТИТЬ':
            self.menu_window.hide_rockets_animation()

        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._hover:
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            painter.setPen(Qt.PenStyle.NoPen)
            if self.text() == 'ЗАПУСТИТЬ':
                gradient.setColorAt(0, QColor("#FF9100"))
                gradient.setColorAt(1, QColor("#FB06AD"))
                painter.setBrush(QBrush(gradient))
                painter.drawRoundedRect(0, 0, self.width(), self.height(), self._radius_upper, self._radius_upper)
            elif self.text() == 'НАСТРОИТЬ':
                gradient.setColorAt(0, QColor("#55D400"))
                gradient.setColorAt(1, QColor("#07B6FB"))
                painter.setBrush(QBrush(gradient))
                painter.drawRoundedRect(0, 0, self.width(), self.height(), self._radius_upper, self._radius_upper)

        if not self._pressed:
            if self.menu_window.parent.theme_color==ThemeColor.LIGHT:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor("#FFBC75")))
                painter.drawRoundedRect(3, 3, self.width() - 6, self.height() - 6, self._radius_inner, self._radius_inner)
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor("#666666")))
                painter.drawRoundedRect(3, 3, self.width() - 6, self.height() - 6, self._radius_inner,
                                        self._radius_inner)

        if self.menu_window.parent.theme_color == ThemeColor.LIGHT:
            painter.setPen(QPen(QColor("black")))
        else:
            painter.setPen(QPen(QColor("white")))
        text_rect = self.rect().adjusted(20, 0, 0, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text())
