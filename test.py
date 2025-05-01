from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtWidgets import QPushButton, QLabel


class SwitchButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self._checked = False
        self.circle_diameter = 20
        self._animation_duration = 200
        self._rect_height = self.circle_diameter + int(self.circle_diameter * 0.2)
        self._rect_width = int(self.circle_diameter * 2.5) + self._rect_height - self.circle_diameter

        self.setStyleSheet(f"""
        QPushButton {{
    background-color: transparent;
    border: 2px solid #000000;
    border-radius:{self._rect_height // 2}px;
   }}
        """)
        self.circle = QLabel(self)
        self.circle.setMouseTracking(True)
        self.circle.setGeometry(int((self._rect_height - self.circle_diameter) / 2),
                                int((self._rect_height - self.circle_diameter) / 2), self.circle_diameter,
                                self.circle_diameter)
        self.circle.setStyleSheet(f"""
        QLabel{{
        background-color: #313131;
        border-radius: {self.circle_diameter // 2}px;
        border:1px solid #000000;
        }}""")
        self.position_animation = QPropertyAnimation(self.circle, b"pos")
        self.position_animation.setDuration(self._animation_duration)

        # Начальное положение и непрозрачность
        self._position = 0
        self._opacity = 1.0

        # Внешний вид кнопки
        self.setFixedSize(self._rect_width, self._rect_height)
        self.setCheckable(True)
        self.setChecked(False)
       
       
       
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(self._checked)
            if not self._checked:
                self.position_animation.setStartValue( QPoint(self.circle.geometry().x(), self.circle.geometry().y()))
                self.position_animation.setEndValue(QPoint(self.circle.geometry().x() + int(self.circle_diameter*1.5), self.circle.geometry().y()))
            else:
                self.position_animation.setStartValue(QPoint(self.circle.geometry().x(), self.circle.geometry().y()))
                self.position_animation.setEndValue(QPoint(self.circle.geometry().x() - int(self.circle_diameter*1.5),
                                                           self.circle.geometry().y()))
            self.position_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
            self.position_animation.start()
            self._checked = not self._checked
            super().mousePressEvent(event)



# class ExampleWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowFlags(
#             Qt.WindowType.FramelessWindowHint |
#             Qt.WindowType.WindowStaysOnTopHint
#
#         )
#
#         self.switch_button = SwitchButton(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = ExampleWindow()
#     ex.show()
#     app.exec()
