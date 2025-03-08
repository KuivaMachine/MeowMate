import sys
import os
import win32gui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap,  QCursor
from PyQt5.QtCore import QPropertyAnimation,Qt, QRect, QPoint, QTimer, QThread, pyqtSignal
from pynput import keyboard,  mouse

# Функция для получения положения и размеров панели задач
def get_taskbar_info():
    taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
    rect = win32gui.GetWindowRect(taskbar)
    return rect

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
class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем и запускаем поток для отслеживания мыши
        self.mouse_tracker = MouseTrackerThread()
        self.mouse_tracker.mouse_moved.connect(self.update_mouse_position)
        self.mouse_tracker.start()


        # Получаем информацию о панели задач
        taskbar_rect = get_taskbar_info()
        taskbar_y = taskbar_rect[1]

        # Настройки окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(QRect(1800, 200, 170, 170))  # Размещаем окно над панелью задач

        # Определяем путь к каталогу с данными в зависимости от режима исполнения
        if getattr(sys, 'frozen', False):
            # Выполнение из собранного исполняемого файла
            datadir = sys._MEIPASS
        else:
            # Выполнение в режиме разработки
            datadir = '.'    
        try:
            self.cat = QPixmap(os.path.join("D:/", "cat.png"))  # Первое изображение
            print("Изображение cat.png успешно загружено.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения cat.png: {e}")
  
        try:
            self.cat_1 = QPixmap(os.path.join("D:/", "cat1.png"))  # Второе изображение
            print("Изображение cat1.png успешно загружено.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения cat1.png: {e}")

        try:
            self.cat_2 = QPixmap(os.path.join("D:/", "cat2.png"))  # Третье изображение
            print("Изображение cat2.png успешно загружено.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения cat2.png: {e}")

        # Загружаем изображение с прозрачностью
        self.label = QLabel(self)
        pixmap = QPixmap(self.cat)  # Укажите путь к вашему изображению (PNG с прозрачностью)
        self.label.setGeometry(0, 0, 170, 170)  # Размер метки
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        self.pos_animation = QPropertyAnimation(self, b"pos")
        self.pos_animation.setDuration(5000)
        self.pos_animation.setStartValue(self.pos())  # Текущее положение
        self.pos_animation.setEndValue(self.pos() + QPoint(-2000, 0))  # Смещение на 100x100
        self.pos_animation.setLoopCount(3)
        #self.pos_animation.start()
      
        # Флаг для отслеживания состояния клавиши
        self.key_pressed = False
        self.catTap = True
        # Создание слушателя событий клавиатуры
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
      
        #self.listener.start()


        # Создаем таймер для смены картинок
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)  # Связываем таймер с функцией смены изображения
        self.timer.start(200)  # Интервал смены картинок: 500 мс (0.5 секунды)

        self.eye_offset = QPoint(50, 30)  # Примерные координаты глаз
        
    def update_mouse_position(self, x, y):
        # Обновляем текст метки с координатами
        print(f"Мышь: {x}, {y}")


    # Функция для смены изображения
    def change_image(self):
        if self.catTap:
            self.label.setPixmap(self.cat_1)
           
        else:
             self.label.setPixmap(self.cat_2)
        self.catTap=not self.catTap
       
        


    # Обработка нажатия клавиши
    def on_press(self, key):
        try:
            if not self.key_pressed:  # Нажатие клавиши
                if self.catTap:
                    self.label.setPixmap(self.cat_1)  # Меняем изображение на третье
                    self.catTap = False
                else:
                    self.label.setPixmap(self.cat_2)  # Меняем изображение на второе
                    self.catTap = True
                self.key_pressed = True
        except AttributeError:
            print(f"Нажата специальная клавиша: {key}")

    # Обработка отпускания клавиши
    def on_release(self, key):
        if self.key_pressed:
            self.label.setPixmap(self.cat)  # Возвращаемся к первому изображению
            self.key_pressed = False

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    print("Программа стартовала!")
    sys.exit(app.exec_())