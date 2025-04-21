from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QApplication,QScrollArea
from PyQt6.QtCore import Qt, QSize, QRect, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen, QMovie, QCursor,QPixmap
import sys, os, math,win32api,random

import sys, os, math,win32api,random
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QTransform,QMovie
from PyQt6.QtCore import QPropertyAnimation, Qt, QRect, QPoint, QTimer, QThread, pyqtSignal, QEasingCurve,QSize,QVariantAnimation,QObject
from pynput import keyboard, mouse
from PyQt6.QtGui import QPainterPath
from PyQt6.QtCore import QPointF
from enum import Enum


from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QPen

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QConicalGradient, QPen, QPolygonF

class AnimalCart(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(190, 254)
        self.angle = 0 
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(255, 153, 102, 150))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow) 

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
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
        painter.setBrush(QBrush(QColor("#212121")))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        
        # 2. Создаем градиент для обводки
        gradient = QConicalGradient()  # Конический градиент (для кругового движения)
        gradient.setCenter(QPointF(self.rect().center()))
        gradient.setAngle(self.angle)  # Текущий угол анимации
        
        # Цвета градиента (прозрачный -> цвет -> прозрачный)
        gradient.setColorAt(0.09, QColor(255, 211, 0, 0))   
        gradient.setColorAt(0.10, QColor(255, 211, 0, 255))   
        gradient.setColorAt(0.20, QColor(255, 211, 0, 255))  
        gradient.setColorAt(0.29, QColor(255, 255, 255, 0)) 

        gradient.setColorAt(0.59, QColor(255, 211, 0, 0))
        gradient.setColorAt(0.60, QColor(255, 211, 0, 255)) 
        gradient.setColorAt(0.70, QColor(255, 211, 0, 255)) 
        gradient.setColorAt(0.79, QColor(255, 211, 0, 0))  
  


        gradient.setColorAt(0.90, QColor(255, 255, 255, 0))  
        
        # 3. Рисуем обводку с градиентом
        pen = QPen(QBrush(gradient), 5)
        painter.setPen(pen)
        painter.drawRoundedRect(3, 3, self.width()-9, self.height()-9, 20, 20)
        
        # # 4. Рисуем внутреннюю часть (чтобы граница была только по краям)
        # painter.setBrush(QBrush(QColor("#212121")))
        # painter.setPen(Qt.PenStyle.NoPen)
        # painter.drawRoundedRect(3, 3, self.width()-7, self.height()-7, 10, 10)

# Запуск приложения
if __name__ == "__main__":
    app = QApplication([])
    window = AnimalCart()
    window.show()
    app.exec()