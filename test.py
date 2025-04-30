import sys

from PyQt6.QtWidgets import QAbstractButton, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QPen

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel


class SwitchButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(60, 30)

        # Цвета для разных состояний
        self._bg_color = QColor("#cccccc")
        self._circle_color = QColor("#ffffff")
        self._active_color = QColor("#4cd964")

        # Позиция кружка (0-1)
        self._circle_position = 0.0

        # Анимация
        self._position_animation = QPropertyAnimation(self, b"circle_position")
        self._position_animation.setDuration(200)
        self._position_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self._color_animation = QPropertyAnimation(self, b"bg_color")
        self._color_animation.setDuration(200)

        self.toggled.connect(self._start_animations)

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    @pyqtProperty(QColor)
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color
        self.update()

    def _start_animations(self, checked):
        # Анимация позиции кружка
        self._position_animation.stop()
        self._position_animation.setStartValue(self._circle_position)
        self._position_animation.setEndValue(1.0 if checked else 0.0)
        self._position_animation.start()

        # Анимация цвета фона
        self._color_animation.stop()
        self._color_animation.setStartValue(self._bg_color)
        self._color_animation.setEndValue(self._active_color if checked else QColor("#cccccc"))
        self._color_animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Рисуем фон (прямоугольник со скругленными краями)
        bg_rect = self.rect()
        radius = bg_rect.height() / 2
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._bg_color)
        painter.drawRoundedRect(bg_rect, radius, radius)

        # Рисуем кружок
        circle_diameter = bg_rect.height() - 6
        circle_x = 3 + self._circle_position * (bg_rect.width() - 6 - circle_diameter)
        circle_y = 3

        painter.setBrush(self._circle_color)
        painter.drawEllipse(circle_x, circle_y, circle_diameter, circle_diameter)





class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.switch = SwitchButton()
        self.switch.setChecked(False)
        self.switch.toggled.connect(self.on_switch_toggled)

        self.label = QLabel("Switch is OFF")

        layout.addWidget(self.switch, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def on_switch_toggled(self, state):
        self.label.setText("Switch is ON" if state else "Switch is OFF")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    app.exec()