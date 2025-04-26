from PyQt6.QtWidgets import QStackedLayout,QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QScrollArea,QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QSize, QRect, pyqtSignal,Qt, QTimer, QPointF,pyqtProperty,QPropertyAnimation, QPoint,QRectF
from PyQt6.QtGui import QColor, QPainter, QPen, QMovie, QCursor,QPixmap,QPainter, QBrush, QColor, QConicalGradient, QPen, QPolygonF,QFontDatabase, QFont, QPainterPath, QRegion
import sys, os, math,win32api,random

import sys, os, math,win32api,random
from pynput import keyboard, mouse








class AnimalGallery(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #FFF2D6;
                border: 2px solid #000000;
                border-radius: 20px;
            }
        """)
        self.setFixedSize(800,500)
        
        
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
        # self.main_layout.addWidget(self.scroll_area)
       

        
        # Устанавливаем главный виджет
        self.setCentralWidget(self.main_widget)
        
        # Добавляем тестовые карточки
        self.add_cards([
            "./drawable/flork/flork_shy.gif",
            "./drawable/flork/flork_shy.gif",
            "./drawable/flork/flork_shy.gif",
            "./drawable/flork/flork_shy.gif",
            "./drawable/flork/flork_shy.gif"
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



        


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimalGallery()
    window.show()
    app.exec()