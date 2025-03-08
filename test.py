import sys, math
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QPoint, QSize, QParallelAnimationGroup
from PyQt5.QtGui import QPixmap
from pynput import mouse

# Поток для отслеживания движения мыши
class MouseTrackerThread(QThread):
    # Сигнал для передачи координат мыши
    mouse_moved = pyqtSignal(int, int)  # x, y

    def run(self):
        # Функция, которая вызывается при движении мыши
        def on_move(x, y):
            self.mouse_moved.emit(x, y)

        # Создаем слушатель мыши
        with mouse.Listener(on_move=on_move) as listener:
            listener.join()

# Основное окно
class EyeTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Создаем и запускаем поток для отслеживания мыши
        self.mouse_tracker = MouseTrackerThread()
        self.mouse_tracker.mouse_moved.connect(self.update_eye_position)
        self.mouse_tracker.start()

    def initUI(self):
        # Настройки окна
        self.setGeometry(0, 0, 300, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
       # self.setAttribute(Qt.WA_TranslucentBackground)

        # Загружаем изображение глаза
        self.eye_image = QPixmap("D://eye.png")  # Укажите путь к изображению глаза

        # Создаем два глаза
        self.eye_l = QLabel(self)
        self.eye_l.setPixmap(self.eye_image)
        self.eye_l.setGeometry(120, 50, 100,100)

        # self.eye_r = QLabel(self)
        # self.eye_r.setPixmap(self.eye_image)
        # self.eye_r.setGeometry(50, 50, 100,100)

        # Анимации для плавного движения глаз
        self.eye_l_animation = QPropertyAnimation(self.eye_l, b"pos")
        self.eye_l_animation.setDuration(200)  # Длительность анимации: 200 мс

        self.eye_l_size= QPropertyAnimation(self.eye_l, b"size")
        self.eye_l_size.setDuration(1000)  # Длительность анимации: 1 секунда
        self.eye_l_size.setStartValue(QSize(100, 100))  # Начальный размер
        self.eye_l_size.setEndValue(QSize(600, 600))    # Конечный размер



        # # Анимации для плавного движения глаз
        # self.eye_r_animation = QPropertyAnimation(self.eye_r, b"pos")
        # self.eye_r_animation.setDuration(200)  # Длительность анимации: 200 мс
       
        # Центры глаз (примерные координаты)
        self.center_l = self.eye_l.geometry().center() # Центр левого глаза
       # self.center_r = self.eye_r.geometry().center() # Центр левого глаза
      
        self.flag = True
        # Максимальное смещение глаз (в пикселях)
        self.max_offset = 10  # Глаза могут двигаться на 50 пикселей от центра

    def update_eye_position(self, mouse_x, mouse_y):
        # Преобразуем глобальные координаты мыши в координаты относительно окна
        mouse_pos = self.mapFromGlobal(QPoint(mouse_x, mouse_y))
        
        distance = math.sqrt((mouse_pos.x() - self.center_l.x()) ** 2 +
                            (mouse_pos.y() - self.center_l.y()) ** 2)
        
        # Если мышь в пределах 200 пикселей
        if distance <= 200 and self.flag:
            self.eye_l_size.start()
            self.flag=False

        # Обновляем положение левого глаза
        self.move_eye(self.eye_l, self.center_l, mouse_pos,self.eye_l_animation)
        # self.move_eye(self.eye_r, self.center_r, mouse_pos,self.eye_r_animation)
       

    def move_eye(self, eye_label, center, mouse_pos, animation):
        # Вычисляем разницу между положением мыши и центром глаза
        delta_x = mouse_pos.x() - center.x()
        delta_y = mouse_pos.y() - center.y()

        # Вычисляем процентное соотношение для смещения глаза
        percent_x = delta_x / (self.width() / 2)  # Процент по горизонтали
        percent_y = delta_y / (self.height() / 2)  # Процент по вертикали

        # Вычисляем новое положение глаза
        new_x = center.x() + percent_x * self.max_offset
        new_y = center.y() + percent_y * self.max_offset

        animation.setStartValue(eye_label.pos())
        animation.setEndValue(QPoint(int(new_x - eye_label.width() / 2),
                              int(new_y - eye_label.height() / 2)))
        # animation.start()

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EyeTrackerWindow()
    window.show()
    sys.exit(app.exec_())