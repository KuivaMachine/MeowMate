import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QPropertyAnimation, Qt, QRect, QPoint, QTimer, QThread, pyqtSignal, QEasingCurve
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve

class FallingCatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
          # РАЗМЕРЫ ОКНА МОНИТОРА
        self.monitor_width = QApplication.primaryScreen().geometry().width()
        self.monitor_height = QApplication.primaryScreen().geometry().height()
        self.cat_window_size = 300
        # Настройки окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(QRect(0, 0, 1000,
                               1000))
        
        # Кот
       
        self.cat = QLabel(self)
        self.cat.setGeometry(0, 0, self.cat_window_size, self.cat_window_size)
        self.main_cat = QPixmap("./cat/PET_stat.png").scaled(self.cat_window_size, self.cat_window_size, 
                                                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cat.setPixmap(self.main_cat)
        self.cat.setAlignment(Qt.AlignCenter)
        
        # Физика падения
        self.is_dragging = False
        self.initial_pos = None
        self.fall_timer = QTimer(self)
        self.fall_timer.timeout.connect(self.update_fall_position)
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.initial_velocity = 3  # Начальная горизонтальная скорость
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.cat.geometry().contains(event.pos()):
            self.is_dragging = True
            self.initial_pos = event.pos()
            self.fall_timer.stop()  # Останавливаем предыдущее падение
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.is_dragging and self.initial_pos:
            delta = event.pos() - self.initial_pos
            self.cat.move(self.cat.x() + delta.x(), self.cat.y() + delta.y())
            self.initial_pos = event.pos()
            event.accept()
    
    def mouseReleaseEvent(self, event):
        if self.is_dragging:
            self.is_dragging = False
            
            # Рассчитываем начальную скорость на основе движения мыши
            if self.initial_pos:
                delta = event.pos() - self.initial_pos
                self.velocity_x = delta.x() * 0.1  # Чувствительность инерции
                self.velocity_y = 0  # Начинаем с 0 по вертикали
            
            # Запускаем анимацию падения
            self.start_falling()
            event.accept()
    
    def start_falling(self):
        """Запускает физическое падение с таймером"""
        self.fall_timer.start(16)  # ~60 FPS
    
    def update_fall_position(self):
        """Обновляет позицию кота с учётом физики"""
        # Применяем гравитацию
        self.velocity_y += self.gravity
        
        # Обновляем позицию
        new_x = self.cat.x() + self.velocity_x
        new_y = self.cat.y() + self.velocity_y
        
        # Проверка на выход за нижнюю границу
        if new_y >= self.monitor_height - self.cat_window_size:
            new_y = self.monitor_height - self.cat_window_size
            self.velocity_y *= -0.5  # Отскок с потерей энергии
            self.velocity_x *= 0.8   # Трение о "землю"
            
            # Если скорость маленькая, останавливаем анимацию
            if abs(self.velocity_y) < 1 and abs(self.velocity_x) < 0.5:
                self.fall_timer.stop()
        
        self.cat.move(int(new_x), int(new_y))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FallingCatWindow()
    window.show()
    sys.exit(app.exec_())