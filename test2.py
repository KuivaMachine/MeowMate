import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPropertyAnimation,Qt, QRect, QEasingCurve, QSize, QPointF




class StretchableImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Начальные параметры
        self.cat_window_size = 300
        self.new_h=0
        self.new_y=0
        self.min_height = self.cat_window_size
        self.max_height=400
        self.original_height = self.cat_window_size
        self.dragging = False
        self.initial_pos = None
        self.monitor_height=QApplication.primaryScreen().geometry().height()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(QRect(1500, 580+30, self.cat_window_size, 500)) 
        
        self.cat = QLabel(self)
        self.cat.setGeometry(0, 0, self.cat_window_size, self.cat_window_size) 
        self.cat_pixmap=QPixmap("D://py/cat/PET_t.png")
        self.cat.setPixmap(self.cat_pixmap)
        self.cat.setAlignment(Qt.AlignCenter)
       
        self.animation = QPropertyAnimation(self.cat, b"geometry")
        self.animation.setDuration(800)
        self.animation.setEasingCurve(QEasingCurve.OutElastic)
        




    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.cat.geometry().contains(event.pos()):
            self.dragging = True
            self.initial_pos = event.pos()
            self.original_height = self.cat.height()
            self.original_y = self.cat.y()
            self.animation.stop()
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.dragging and self.initial_pos is not None:
            # Вычисляем разницу в положении курсора
            delta = self.initial_pos.y() - event.pos().y()
            
            # Вычисляем новую высоту
            new_height = self.original_height + delta
            
            # Ограничиваем минимальную высоту
            if new_height < self.min_height:
                new_height = self.min_height
             # Ограничиваем максимальную высоту
            if new_height > self.max_height:
                new_height = self.max_height
            
            # Вычисляем новую позицию Y (верхняя граница)
            self.new_y = self.original_y - (new_height - self.original_height)
            
            # Обновляем геометрию изображения
            self.cat.setGeometry(
                self.cat.x(),
                self.new_y,
                self.cat.width(),
                new_height
            )
            
            # Масштабируем изображение
            self.cat.setPixmap(QPixmap(self.cat_pixmap).scaled(
                self.cat.width(), new_height, 
                Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.new_h=new_height
            event.accept()
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.initial_pos = None

        
            self.cat.setPixmap(QPixmap(self.cat_pixmap).scaled(
                self.cat.width(), self.cat_window_size, 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            target_rect = QRect(
                0, 
                self.height() - self.cat_window_size,
                self.cat_window_size,
                self.cat_window_size
            )
            
            self.animation.setStartValue(self.cat.geometry())
            self.animation.setEndValue(target_rect)
            self.animation.start()

            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def resizeEvent(self, event):
        # При изменении размера окна обновляем положение изображения
        self.cat.move(0, self.height() - self.cat.height())
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StretchableImageWindow()
    window.show()
    sys.exit(app.exec_())