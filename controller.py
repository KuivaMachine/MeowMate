from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QApplication,QGraphicsDropShadowEffect,QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QSize, QRect, pyqtSignal,QTimer,QPointF
from PyQt6.QtGui import QColor, QPainter, QPen, QMovie, QCursor,QPixmap
import sys, os, math,win32api,random
from PyQt6.QtGui import QPainter, QBrush, QColor, QConicalGradient, QPen, QPolygonF


class CustomButton(QPushButton):
    def __init__(self, parent, text, color):
        super().__init__(text, parent)
        self.color = color
        self.setFixedSize(30, 30)
        self.setStyleSheet("""
            QPushButton {
                background-color: %s;
                color: white;
                border-radius: 15px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: %s;
            }
        """ % (self.color.name(), self.color.darker(120).name()))


class CustomMenuButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(150, 50)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border-radius: 10px;
                border: 2px solid #5a5a5a;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
                border: 2px solid #6a6a6a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
        """)


class ClickableGifLabel(QLabel):
    clicked = pyqtSignal()
    
    def __init__(self, gif_path, size):
        super().__init__()
        self.setFixedSize(size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Загрузка гифки
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(size)
        self.setMovie(self.movie)
        self.movie.start()
        
        # Рамка
        self.setStyleSheet("""
            QLabel {
                border: 6px solid #5a5a5a;
                border-radius: 5px;
                padding: 5px;
            }
        """)
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                border: 2px solid #7a7a7a;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                border: 2px solid #5a5a5a;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        super().leaveEvent(event)


class AnimalCart(QLabel):
    def __init__(self,gif_path,size):
        super().__init__()
          # Загрузка гифки
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(size)
        self.setMovie(self.movie)
        self.movie.start()
        self.setFixedSize(200, 200)
        self.angle = 0 
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(255, 153, 102, 150))
        self.shadow.setOffset(6, 6)
        self.setGraphicsEffect(self.shadow) 
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(4)  # Начальное значение - нет размытия
        
        # Применяем эффект ко всему виджету
        # self.setGraphicsEffect(self.blur_effect)


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
        painter.setBrush(QBrush(QColor("#00312121")))
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

        
class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Убираем стандартные рамки окна
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Основные параметры окна
        self.setFixedSize(800, 600)
        
        # Создаем основной контейнер
        self.main_container = QWidget(self)
        self.main_container.setGeometry(0, 0, 800, 600)
        
        # Настройка стилей
        self.setup_styles()
        
        # Создаем элементы интерфейса
        self.setup_ui()
        
        # Переменные для перемещения окна
        self.drag_pos = None
    
    def setup_styles(self):
        # Устанавливаем стили через CSS
        self.main_container.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 15px;
                border: 2px solid #4a4a4a;
            }
        """)
    
    def setup_ui(self):
        # Макет заголовка
        self.header = QWidget(self.main_container)
        self.header.setGeometry(0, 0, 800, 40)
        self.header.setStyleSheet("""
            background-color: #3a3a3a;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
        """)
        
        # Кнопки управления окном
        self.setup_window_controls()
        
        # Основной контент
        self.setup_content()
    
    def setup_window_controls(self):
        # Кнопка закрытия
        self.close_btn = CustomButton(self.header, "✕", QColor(255, 95, 87))
        self.close_btn.setGeometry(750, 5, 30, 30)
        self.close_btn.clicked.connect(self.close)
        
        # Кнопка свернуть
        self.minimize_btn = CustomButton(self.header, "—", QColor(255, 189, 46))
        self.minimize_btn.setGeometry(710, 5, 30, 30)
        self.minimize_btn.clicked.connect(self.showMinimized)
    
    def setup_content(self):
        # Основной макет
        main_layout = QVBoxLayout(self.main_container)
        main_layout.setContentsMargins(20, 50, 20, 20)
        
        # Заголовок
        title = QLabel("Выбери персонажа")
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                font-family: 'PT Mono';
            }
        """)
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Контейнер с гифками
        self.setup_gif_container(main_layout)
        
        # Кастомизированные кнопки меню
        self.setup_menu_buttons(main_layout)
    
    def setup_gif_container(self, parent_layout):
        # Контейнер для гифок с рамкой
        gif_container = QWidget()
        gif_container.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 0px solid #4a4a4a;
                border-radius: 20px;
            }
        """)
        
        gif_layout = QHBoxLayout(gif_container)
        
        # Первая гифка
        gif1 = AnimalCart("./cat/drawable/flork/flork_shy.gif", QSize(160, 160))
        # gif1.clicked.connect(lambda: print("GIF 1 clicked"))
        gif_layout.addWidget(gif1)
        
        # Вторая гифка
        gif2 = AnimalCart("./cat/drawable/cat/lapa.gif", QSize(160, 160))
        # gif2.clicked.connect(lambda: print("GIF 2 clicked"))
        gif_layout.addWidget(gif2)
        
        parent_layout.addWidget(gif_container)
    
    def setup_menu_buttons(self, parent_layout):
        # Контейнер для кнопок
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        
        # Кастомизированные кнопки
        btn1 = CustomMenuButton("Start Game")
        btn1.clicked.connect(self.start_game)
        
        btn2 = CustomMenuButton("Settings")
        btn2.clicked.connect(self.open_settings)
        
        btn3 = CustomMenuButton("Exit")
        btn3.clicked.connect(self.close)
        
        buttons_layout.addWidget(btn1)
        buttons_layout.addWidget(btn2)
        buttons_layout.addWidget(btn3)
        
        parent_layout.addWidget(buttons_container)
    
    # Обработчики событий для перемещения окна
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.pos().y() < 40:
            self.drag_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        self.drag_pos = None
    
    # Методы меню
    def start_game(self):
        print("Starting game...")
    
    def open_settings(self):
        print("Opening settings...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Для лучшего отображения
    
    window = CustomWindow()
    window.show()
    
    app.exec()