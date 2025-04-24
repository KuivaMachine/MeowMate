from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QApplication,QScrollArea,QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QSize, QRect, pyqtSignal,Qt, QTimer, QPointF
from PyQt6.QtGui import QColor, QPainter, QPen, QMovie, QCursor,QPixmap,QPainter, QBrush, QColor, QConicalGradient, QPen, QPolygonF
import sys, os, math,win32api,random

import sys, os, math,win32api,random
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel,QGraphicsBlurEffect
from PyQt6.QtGui import QPixmap, QTransform,QMovie
from PyQt6.QtCore import QPropertyAnimation, Qt, QRect, QPoint, QTimer, QThread, pyqtSignal, QEasingCurve,QSize,QVariantAnimation,QObject
from pynput import keyboard, mouse
from PyQt6.QtGui import QPainterPath
from PyQt6.QtCore import QPointF



from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty


from PyQt6.QtWidgets import QWidget, QApplication

from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QPen




class AnimalGallery(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animal Cards Gallery")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 2px solid #4a4a4a;
                border-radius: 20px;
            }
        """)
        
        # Создаем главный виджет и макет
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # Создаем скроллируемую область
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            /* Вертикальный скроллбар */
            QScrollBar:vertical {
                border: none;
                background: #212121;
                width: 30px;
                margin: 5px 5px 5px 0px;
                border-radius: 12px;
            }
            
            QScrollBar::handle:vertical {
                background: #ff9966;
                min-height: 20px;
                border-radius: 12px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #212121;
            }
            
        
        """)
        
      
        # Контейнер для карточек
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Добавляем контейнер в скролл-область
        self.scroll_area.setWidget(self.cards_container)
        
        # Добавляем скролл-область в главный макет
        self.main_layout.addWidget(self.scroll_area)
        
        # Устанавливаем главный виджет
        self.setCentralWidget(self.main_widget)
        
        # Добавляем тестовые карточки
        self.add_cards([
            "./cat/drawable/flork/flork_shy.gif", "./cat/drawable/flork/flork_shy.gif", 
            "./cat/drawable/flork/flork_shy.gif", "./cat/drawable/flork/flork_shy.gif",
            "./cat/drawable/flork/flork_shy.gif"  # Для демонстрации скролла
        ])
    
    def add_cards(self, gif_paths):
        # Очищаем предыдущие карточки
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Создаем ряды по 2 карточки
        row = None
        for i, path in enumerate(gif_paths):
            if i % 2 == 0:
                # Создаем новый ряд для каждой пары карточек
                row = QWidget()
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(0, 0, 0, 20)  # Отступ снизу
                self.cards_layout.addWidget(row)
            
            # Создаем и добавляем карточку в текущий ряд
            card = AnimalCart(path, QSize(160, 160))
            row.layout().addWidget(card, alignment=Qt.AlignmentFlag.AlignLeft)



        
        
class AnimalCart(QLabel):
    def __init__(self,gif_path,size):
        super().__init__()

        self.setMouseTracking(True)
       
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(size)
        self.setMovie(self.movie)
        self.movie.start()
        self.setFixedSize(200, 200)
        
        self.angle = 0 
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(255, 255, 255,255))
        self.shadow.setOffset(5, 5)
        self.setGraphicsEffect(self.shadow) 
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Исходные позиции для анимации
        self.normal_pos = QPoint(5, 5)
        self.pressed_pos = QPoint(0, 0)
        # Анимация нажатия
        self.press_animation = QPropertyAnimation(self.shadow, b"offset")
        self.press_animation.setDuration(20)
        self.press_animation.setStartValue(self.normal_pos)
        self.press_animation.setEndValue(self.pressed_pos)
        
        # Анимация отпускания
        self.release_animation = QPropertyAnimation(self.shadow, b"offset")
        self.release_animation.setDuration(20)
        self.release_animation.setStartValue(self.pressed_pos)
        self.release_animation.setEndValue(self.normal_pos)


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_angle)
        self.timer.start(11)

       

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + QPoint(6, 6))
            self.press_animation.start()
            # self.blur_animation.start()
           
     
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.release_animation.start()
            self.move(self.pos() - QPoint(6, 6))
            
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        event.accept()
        # self.blur_animation.start()

    def update_angle(self):
        self.angle = (self.angle + 2) % 360  # Плавное изменение угла
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 1. Рисуем фон карточки
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#414141")))
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
        painter.drawRoundedRect(1,1, self.width()-2, self.height()-2, 20, 20)

        super().paintEvent(event)


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimalGallery()
    window.show()
    app.exec()