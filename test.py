from PyQt6.QtWidgets import QStackedLayout,QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QScrollArea,QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QSize, QRect, pyqtSignal,Qt, QTimer, QPointF,pyqtProperty,QPropertyAnimation, QPoint,QRectF
from PyQt6.QtGui import QColor, QPainter, QPen, QMovie, QCursor,QPixmap,QPainter, QBrush, QColor, QConicalGradient, QPen, QPolygonF,QFontDatabase, QFont, QPainterPath, QRegion
import sys, os, math,win32api,random

import sys, os, math,win32api,random
from pynput import keyboard, mouse





class CircularLabel(QLabel):
    def __init__(self,parent,gif_path,color ):
        super().__init__(parent)
        self.setFixedSize(50, 50)
        self.color = color
        # Убираем стандартную рамку и фон
        self.setStyleSheet("""
            QLabel {
                background-color: #FFF2D6;
                border-radius: 25px;
                border-width:0px;
               
            }
        """)
        
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(QSize(50,50))
        self.setMovie(self.movie)
        self.movie.start()
        self.movie.stop()

 

class CustomAnimatedButton(QPushButton):
    def __init__(self, text, gif_path, parent):
        super().__init__(parent)
        self.setFixedSize(230, 70)
        self.setText(text)
        self.menu_window =parent
        
        self._angle = 0
        self._hover = False
        self._radius_inner = self.height() // 2
        self._radius_upper = (self.height()+4) // 2
        # Настройка шрифта
        self.font = QFont("JetBrains Mono",18)
        self.font.setWeight(QFont.Weight.ExtraBold)
        self.setFont(self.font)


        # Настройка гифки в круге
        self.gif_label = CircularLabel(self, gif_path,"#FFF2D6")
        self.gif_label.move(self.width() - 60, (self.height() -50) // 2)

        
        # Тень при наведении
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(0)
        self.shadow_effect.setColor(QColor(0, 0, 0, 250))
        self.shadow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow_effect)
        
        
        # Анимация тени
        self.shadow_animation = QPropertyAnimation(self.shadow_effect, b"blurRadius")
        self.shadow_animation.setDuration(120)
        
    
    def update_angle(self):
        self._angle = (self._angle + 2) % 360
        if self._hover:  # Обновляем только при наведении
            self.update()
    
    def enterEvent(self, event):
        self._hover = True
        # Анимация появления тени
        self.shadow_animation.stop()
        self.shadow_animation.setStartValue(0)
        self.shadow_animation.setEndValue(15)
        self.shadow_animation.start()
        self.gif_label.movie.start()
        self.menu_window.startGearsAnimation()


        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._hover = False
        # Анимация исчезновения тени
        self.shadow_animation.stop()
        self.shadow_animation.setStartValue(15)
        self.shadow_animation.setEndValue(0)
        self.shadow_animation.start()
        self.gif_label.movie.stop()
        self.menu_window.hideGearsAnimation()

        super().leaveEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
      
        
        # 2. Анимированная обводка при наведении
        if self._hover:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#000000")))
            painter.drawRoundedRect(0, 0, self.width(), self.height(),  self._radius_upper,  self._radius_upper)
        
          # 1. Рисуем фон
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#FFBC75")))
        painter.drawRoundedRect(3, 3, self.width()-6, self.height()-6, self._radius_inner, self._radius_inner)

        # 4. Рисуем текст слева
        painter.setPen(QPen(QColor("black")))
        text_rect = self.rect().adjusted(25, 0, 0, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text())


class AnimalGallery(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animal Cards Gallery")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 600)

       
        # Создаем главный виджет и макет
        self.main_widget = QWidget()
        self.main_widget.setStyleSheet("""
            QWidget {
                background-color: #FFF2D6;
                border: 2px solid #000000;
                border-radius: 20px;
            }
        """)
        self.main_widget.setFixedSize(800,500)
        
        
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
        self.stack = QStackedLayout(self.main_widget)

        self.stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
         
        # 2. Добавляем кнопку (будет спереди)
        self.button = CustomAnimatedButton("ЗАПУСТИТЬ","./cat/drawable/menu/gears_mini.gif",self)
        self.button2 = CustomAnimatedButton("ЗАПУСТИТЬ","./cat/drawable/menu/gears_mini.gif",self)
        self.button_layout = QWidget()
        self.button_layout.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.main_layout = QVBoxLayout(self.button_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.button2)

        self.stack.addWidget(self.button_layout)

        self.gears= QLabel()
        self.movie = QMovie("cat/drawable/menu/rockets.gif")
        self.movie.setScaledSize(QSize(350,190))
        self.gears.setMovie(self.movie)
        self.gears.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gears.hide()

        self.stack.addWidget(self.gears)
       
      

        

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
            "./cat/drawable/flork/flork_shy.gif", 
            "./cat/drawable/flork/flork_shy.gif", 
            "./cat/drawable/flork/flork_shy.gif", 
            "./cat/drawable/flork/flork_shy.gif",
            "./cat/drawable/flork/flork_shy.gif"
        ])

    def startGearsAnimation(self):
        self.movie.start()
        self.gears.show()

    def hideGearsAnimation(self):
        self.gears.hide()
        self.movie.stop()
        
        
        
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