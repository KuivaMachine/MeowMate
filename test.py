import sys, os, math
import win32gui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QPropertyAnimation,Qt, QRect, QPoint, QTimer, QThread, pyqtSignal
from pynput import keyboard,  mouse
from enum import Enum
import random

# Поток для отслеживания движения мыши
class MouseTrackerThread(QThread):
    # Сигнал для передачи координат мыши
    mouse_moved = pyqtSignal(int, int)  # x, y
    left_clicked = pyqtSignal(int, int, bool)      # Левая кнопка
   

    def run(self):
        # Функция, которая вызывается при движении мыши
        def on_move(x, y):
            self.mouse_moved.emit(x, y)

         # Функция, которая вызывается при нажатии/отпускании кнопки мыши
        def on_click(x, y, button, pressed):
            if button == mouse.Button.left:
                self.left_clicked.emit(x,y,pressed)

        # Создаем слушатель мыши
        with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
            listener.join()



class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cat_window_size=171

         # Создаем и запускаем поток для отслеживания мыши
        self.mouse_tracker = MouseTrackerThread()
        self.mouse_tracker.mouse_moved.connect(self.update_mouse_position)
        self.mouse_tracker.start()
        self.mouse_tracker.left_clicked.connect(self.handle_left_click)

        #РАЗМЕРЫ ОКНА МОНИТОРА 
        self.monitor_width=QApplication.primaryScreen().geometry().width()
        self.monitor_height=QApplication.primaryScreen().geometry().height()


        # Настройки окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(QRect(1500, 500, self.cat_window_size, self.cat_window_size)) 

        self.cat = QLabel(self)
        self.cat.setGeometry(0, 0, self.cat_window_size, self.cat_window_size) 
        self.cat.setPixmap(QPixmap("D://py/cat/test.png"))
        self.cat.setAlignment(Qt.AlignCenter)
           
 #СЛУШАТЕЛЬ МЫШИ
    def update_mouse_position(self, mouse_x, mouse_y):
         #ПРЯМОУГОЛЬНИК ОКНА КОТА
        window_rect = self.frameGeometry()
        self.original_size = self.cat.size()
        #ЕСЛИ МЫШЬ НАХОДИТСЯ В ПРЕДЕЛАХ ОКНА КОТА
        if window_rect.contains(QPoint(mouse_x, mouse_y)):
            print("SSSSS")


 #СЛУШАТЕЛЬ ЛЕВОГО КЛИКА МЫШИ
    def handle_left_click(self,mouse_x,mouse_y,left_pressed):
          #ПРЯМОУГОЛЬНИК ОКНА КОТА
        window_rect = self.frameGeometry()
        self.original_size = self.cat.size()
        #ЕСЛИ МЫШЬ НАХОДИТСЯ В ПРЕДЕЛАХ ОКНА КОТА
        if left_pressed and window_rect.contains(QPoint(mouse_x, mouse_y)):
            print("qqqqqq")


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())