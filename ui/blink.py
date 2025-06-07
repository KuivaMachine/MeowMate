from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush
from PyQt5.QtWidgets import QLabel

class Blinker(QLabel):
    def __init__(self,parent):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint| Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.parent_window = parent
        self.setFixedSize( self.parent_window.size())

        self.blink_ratio= -0.2
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gradient)
        self.timer.start(15)


    def update_gradient(self):
        self.blink_ratio += 0.09
        if self.blink_ratio >= 0.99:
            self.timer.stop()
            self.blink_ratio = -0.2
            return
        self.update()


    def paintEvent(self, a0):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(Qt.PenStyle.NoPen)
            gradient = QLinearGradient(0,0, self.parent_window.width(), self.parent_window.height())

            gradient.setColorAt(self.blink_ratio, QColor(0, 0, 0, 0))
            gradient.setColorAt(self.blink_ratio + 0.05, QColor(255, 255, 255, 200))
            gradient.setColorAt(self.blink_ratio + 0.1, QColor(0, 0, 0, 0))

            gradient.setColorAt(self.blink_ratio, QColor(0, 0, 0, 0))
            gradient.setColorAt(self.blink_ratio + 0.1, QColor(255, 255, 255, 200))
            gradient.setColorAt(self.blink_ratio + 0.2, QColor(0, 0, 0, 0))

            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(0, 0, self.parent_window.width(), self.parent_window.height(), 20, 20)
        finally:
            painter.end()
