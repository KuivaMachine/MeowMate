from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QLabel


class SwitchButton(QPushButton):
    change_theme = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.is_checked = False
        self.circle_diameter = 16
        self.rect_height = self.circle_diameter + int(self.circle_diameter * 0.5)
        self.rect_width = int(self.circle_diameter * 3) + self.rect_height - self.circle_diameter
        self.setObjectName('switch_button')

        self.circle = QLabel(self)
        self.circle.setObjectName('toggle')
        self.circle.setMouseTracking(True)
        self.circle.setGeometry(int((self.rect_height - self.circle_diameter) / 2),
                                int((self.rect_height - self.circle_diameter) / 2), self.circle_diameter,
                                self.circle_diameter)

        self.position_animation = QPropertyAnimation(self.circle, b"pos")
        self.position_animation.setEasingCurve(QEasingCurve.Type.OutInQuad)
        self.position_animation.setDuration(350)
        # Внешний вид кнопки
        self.setFixedSize(self.rect_width, self.rect_height)


       
       
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.is_checked:
                self.position_animation.setStartValue( QPoint(self.circle.geometry().x(), self.circle.geometry().y()))
                self.position_animation.setEndValue(QPoint(self.circle.geometry().x() + int(self.circle_diameter*2), self.circle.geometry().y()))
            else:
                self.position_animation.setStartValue(QPoint(self.circle.geometry().x(), self.circle.geometry().y()))
                self.position_animation.setEndValue(QPoint(self.circle.geometry().x() - int(self.circle_diameter*2),
                                                           self.circle.geometry().y()))



            self.position_animation.start()
            self.is_checked = not self.is_checked
            self.change_theme.emit(self.is_checked)
            super().mousePressEvent(event)
