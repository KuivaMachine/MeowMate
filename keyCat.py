import sys, os, math
import win32gui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QPropertyAnimation,Qt, QRect, QPoint, QTimer, QThread, pyqtSignal,QEasingCurve
from pynput import keyboard,  mouse
from enum import Enum
import random



class CatState(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT ="right"


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


# Основное окно
class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cat_window_size=300
        self.CAT_GAP=40
        self.min_height = self.cat_window_size
        self.max_height=400
        self.original_height = self.cat_window_size
        self.original_width = self.cat_window_size
        self.dragging = False
        self.initial_pos = None
        self.isOne=False

        # Флаги для отслеживания
        self.cat_position=CatState.BOTTOM         # ПОЛОЖЕНИЕ КОТА НА ЭКРАНЕ
        self.key_pressed = False                # КЛАВИША КЛАВИАТУРЫ НАЖАТА
        self.long_tap = False                   # ФЛАГ ДОЛГОГО ЗАЖАТИЯ
        self.is_window_dragging = False         # КОТ ПЕРЕМЕЩАЕТСЯ
        self.is_stretching = False              # ФЛАГ РАССТЯГИВАНИЯ КОТА

        
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
        self.setGeometry(QRect(1500, (self.monitor_height-self.cat_window_size)+self.CAT_GAP, self.cat_window_size, self.cat_window_size))  # Размещаем окно над панелью задач

        # Определяем путь к каталогу с данными в зависимости от режима исполнения
        if getattr(sys, 'frozen', False):
            # Выполнение из собранного исполняемого файла
            datadir = sys._MEIPASS
        else:
            # Выполнение в режиме разработки
            datadir = '.'    
        try:
            self.cat = QPixmap(os.path.join("D://py/cat/", "cat.png"))
            print("Изображение cat.png успешно загружено.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения cat.png: {e}")
  
        try:
            self.cat_1 = QPixmap(os.path.join("D://py/cat/", "cat1.png")) 
            print("Изображение cat1.png успешно загружено.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения cat1.png: {e}")

        try:
            self.cat_2 = QPixmap(os.path.join("D://py/cat/", "cat2.png"))
            print("Изображение cat2.png успешно загружено.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения cat2.png: {e}")

  
        
        # Загружаем изображение глаза
        self.eye = QPixmap("D://py/cat/eye.png") 
        self.eye2 = QPixmap("D://py/cat/eye2.png")  
        self.eye_big = QPixmap("D://py/cat/eye_big.png") 
        self.eye2_big = QPixmap("D://py/cat/eye2_big.png")  
        self.cat_dragged = QPixmap("D://py/cat/cat_dragged.png") 
        self.cat_fall= QPixmap("D://py/cat/cat_fall.png")  
        self.main_cat = QPixmap("D://py/cat/PET_t.png") 
        self.cat_pixmap_stat=QPixmap("D://py/cat/PET_stat.png") 

        # Создаем 1 глаз
        self.eye_l = QLabel(self)
        self.eye_l.setPixmap(self.eye)
        self.eye_l.setGeometry(0, 0, self.cat_window_size,self.cat_window_size)

        #Анимации для плавного движения глаз
        self.eye_l_animation = QPropertyAnimation(self.eye_l, b"pos")
        self.eye_l_animation.setDuration(200)  # Длительность анимации: 200 мс
        
        
         # Создаем 2 глаз
        self.eye_r = QLabel(self)
        self.eye_r.setPixmap(self.eye2)
        self.eye_r.setGeometry(0,  0, self.cat_window_size,self.cat_window_size)
        self.eye_r_animation = QPropertyAnimation(self.eye_r, b"pos")
        self.eye_r_animation.setDuration(200)  # Длительность анимации: 200 мс
        

        self.center_l = self.eye_l.geometry().center() # Центр левого глаза
        self.center_r = self.eye_r.geometry().center() # Центр левого глаза

        self.max_offset_x = 10  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
        self.max_offset_y = 5  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ

          # Загружаем изображение
        self.cat = QLabel(self)
        self.cat.setGeometry(0, 0, self.cat_window_size, self.cat_window_size) 
        self.cat.setPixmap(self.main_cat)
        self.cat.setAlignment(Qt.AlignCenter)

        #АНИМАЦИЯ ПЕРЕТАСКИВАНИЯ КОТА МЫШКОЙ
        self.move_cat_animation=  QPropertyAnimation(self, b"pos")
        self.move_cat_animation.setDuration(20)

        #АНИМАЦИЯ ПАДЕНИЯ КОТА
        self.fall_cat_animation=  QPropertyAnimation(self, b"pos")
        self.fall_cat_animation.finished.connect(self.cat_preparing)
        self.fall_cat_animation.setDuration(400)

        #АНИМАЦИЯ ВЫГЛЯДЫВАНИЯ КОТА ИЗ РАЗНЫХ МЕСТ
        self.cat_comming_animation=  QPropertyAnimation(self, b"pos")
        self.cat_comming_animation.setDuration(500)
        
        #АНИМАЦИЯ СКРЫВАЮЩЕГОСЯ КОТА
        self.hiding_cat_animation=  QPropertyAnimation(self, b"pos")
        self.hiding_cat_animation.finished.connect(self.cat_preparing)
        self.hiding_cat_animation.setDuration(300)
        
        #АНИМАЦИЯ КОТА-ПРУЖИНКИ
        self.animation = QPropertyAnimation(self.cat, b"geometry")
        self.animation.setDuration(800)
        self.animation.setEasingCurve(QEasingCurve.OutElastic)
      


        # Создание слушателя событий клавиатуры
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        #Таймер для установки больших глаз
        self.bigyeys_timer = QTimer(self)
        self.bigyeys_timer.setInterval(1000)
        self.bigyeys_timer.timeout.connect(self.on_timer_out)
        self.isEyesBig=False

        #Таймер для длительного зажатия на коте
        self.long_drag_timer = QTimer(self)
        self.long_drag_timer.setInterval(2000)
        self.long_drag_timer.timeout.connect(self.on_long_drag_timer_out)
        
        #СЛУШАТЕЛЬ КЛАВИАТУРЫ
        #self.listener.start()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.cat.geometry().contains(event.pos()):
            self.dragging = True
            self.isOne=not self.isOne
            self.initial_pos = event.pos()
            self.original_height = self.cat.height()
            self.original_y = self.cat.y()
            self.animation.stop()
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.dragging and self.initial_pos is not None:
            match(self.cat_position):
                case(CatState.TOP):
                    # Вычисляем разницу в положении курсора
                    delta = event.pos().y()-self.initial_pos.y()
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
                        self.cat.y(),
                        self.cat.width(),
                        new_height
                    )
                    transform = QTransform().rotate(180)
                    
                    # Масштабируем изображение
                    self.cat.setPixmap(self.cat_pixmap_stat.scaled(
                    self.cat.width(), new_height, 
                    Qt.IgnoreAspectRatio, Qt.SmoothTransformation).transformed(transform))
 


                case(CatState.BOTTOM):
                     # Вычисляем разницу в положении курсора
                    delta = self.initial_pos.y()-event.pos().y()
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
                    transform = QTransform().rotate(0)
                
                    # Масштабируем изображение
                    self.cat.setPixmap(self.cat_pixmap_stat.scaled(
                    self.cat.width(), new_height, 
                    Qt.IgnoreAspectRatio, Qt.SmoothTransformation).transformed(transform))


                case(CatState.LEFT):
                    # Разница по горизонтали (движение вправо увеличивает ширину)
                    delta = event.pos().x() - self.initial_pos.x()
                    new_width = self.original_width + delta
                    
                    # Ограничения
                    if new_width < 300:
                        new_width = 300
                    if new_width > 400:  
                        new_width = 400
                    
                    # Меняем только ширину (левый край и Y остаются)
                    self.cat.setGeometry(
                        self.cat.x(),          # X не меняется
                        self.cat.y(),          # Y не меняется
                        new_width,            # Новая ширина
                        self.cat.height()      # Высота не меняется
                    )
                    transform = QTransform().rotate(90)
                    # Масштабируем изображение
                    self.cat.setPixmap(self.cat_pixmap_stat.scaled(new_width, self.cat.height(),Qt.IgnoreAspectRatio, Qt.SmoothTransformation).transformed(transform))

            event.accept()    


        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.initial_pos = None
            match(self.cat_position):
                case(CatState.TOP):
                     transform = QTransform().rotate(180)
                case(CatState.BOTTOM):
                     transform = QTransform().rotate(0)
                case(CatState.LEFT):
                     transform = QTransform().rotate(90)


            
            self.cat.setPixmap(QPixmap(self.cat_pixmap_stat).scaled(
                self.cat.width(), self.cat_window_size, 
                Qt.KeepAspectRatio, Qt.SmoothTransformation).transformed(transform))
            
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



    #ФУНКЦИЯ ПОДГОТОВКИ И ВЫЛЕЗАНИЯ КОТА ИЗ СЛУЧАЙНОГО МЕСТА
    def cat_preparing(self):
        all_cat_states = list(CatState)
       #random.choice(all_cat_states)
        values = self.random_rotate(self.cat_position, CatState.LEFT )
        self.main_cat=values[0]
        self.eye=values[1]
        self.eye2=values[2]
        self.eye_big=values[3]
        self.eye2_big=values[4]
        self.eye_l.setVisible(True)
        self.eye_r.setVisible(True)

        self.cat.setPixmap(self.main_cat)
        self.eye_l.setPixmap(self.eye)
        self.eye_r.setPixmap(self.eye2)
        
        self.cat_comming_animation.setStartValue(values[5])
        self.cat_comming_animation.setEndValue(values[6])
        self.cat_comming_animation.start()

        
    #ФУНКЦИЯ ПОВОРОТА КОТА И ГЛАЗ В ЗАВИСИМОСТИ ОТ ВЫБРАННОГО И ТЕКУЩЕГО ПОЛОЖЕНИЯ КОТА
    def random_rotate(self,current_position, direction):
        values = []
        match(direction):
            case CatState.TOP:
                random_x = random.randint(0, self.monitor_width-self.cat_window_size) 

                #ПРОВЕРКА И ПОВОРОТ В ЗАВИСИМОСТИ ОТ ТЕКУЩЕГО ПОЛОЖЕНИЯ 
                match(current_position):
                    case(CatState.TOP):
                        transform = QTransform().rotate(0)
                    case(CatState.BOTTOM):
                        transform = QTransform().rotate(180)
                    case(CatState.LEFT):
                        transform = QTransform().rotate(90)
                    case(CatState.RIGHT):
                        transform = QTransform().rotate(270)

                main_cat_180 = self.main_cat.transformed(transform)
                eye_180=self.eye.transformed(transform)
                eye2_180=self.eye2.transformed(transform)
                eye_big_180=self.eye_big.transformed(transform)
                eye2_big_180=self.eye2_big.transformed(transform)
                values=[main_cat_180, eye_180, eye2_180, eye_big_180, eye2_big_180, QPoint(random_x,0-self.cat_window_size), QPoint(random_x,0-self.CAT_GAP)]
                self.cat_position=CatState.TOP

            case CatState.BOTTOM:
                random_x = random.randint(0, self.monitor_width-self.cat_window_size) 

                #ПРОВЕРКА И ПОВОРОТ В ЗАВИСИМОСТИ ОТ ТЕКУЩЕГО ПОЛОЖЕНИЯ 
                match(current_position):
                    case(CatState.TOP):
                        transform = QTransform().rotate(180)
                    case(CatState.BOTTOM):
                        transform = QTransform().rotate(0)
                    case(CatState.LEFT):
                        transform = QTransform().rotate(270)
                    case(CatState.RIGHT):
                        transform = QTransform().rotate(90)

                main_cat_0 = self.main_cat.transformed(transform)
                eye_0=self.eye.transformed(transform)
                eye2_0=self.eye2.transformed(transform)
                eye_big_0=self.eye_big.transformed(transform)
                eye2_big_0=self.eye2_big.transformed(transform)
                values=[main_cat_0, eye_0, eye2_0, eye_big_0, eye2_big_0, QPoint(random_x,self.monitor_height), QPoint(random_x,(self.monitor_height-self.cat_window_size)+self.CAT_GAP)]
                self.cat_position=CatState.BOTTOM

            case CatState.LEFT:
                random_y = random.randint(0, self.monitor_height-self.cat_window_size) 

                #ПРОВЕРКА И ПОВОРОТ В ЗАВИСИМОСТИ ОТ ТЕКУЩЕГО ПОЛОЖЕНИЯ 
                match(current_position):
                    case(CatState.TOP):
                        transform = QTransform().rotate(270)
                    case(CatState.BOTTOM):
                        transform = QTransform().rotate(90)
                    case(CatState.LEFT):
                        transform = QTransform().rotate(0)
                    case(CatState.RIGHT):
                        transform = QTransform().rotate(180)

                main_cat_90 = self.main_cat.transformed(transform)
                eye_90=self.eye.transformed(transform)
                eye2_90=self.eye2.transformed(transform)
                eye_big_90=self.eye_big.transformed(transform)
                eye2_big_90=self.eye2_big.transformed(transform)
                values=[main_cat_90, eye_90, eye2_90, eye_big_90, eye2_big_90, QPoint(0-self.cat_window_size, random_y), QPoint(0-self.CAT_GAP,random_y)]
                self.max_offset_x = 5  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
                self.max_offset_y = 10  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ
                self.cat_position=CatState.LEFT

            case CatState.RIGHT:
                random_y = random.randint(0, self.monitor_height-self.cat_window_size) 

                #ПРОВЕРКА И ПОВОРОТ В ЗАВИСИМОСТИ ОТ ТЕКУЩЕГО ПОЛОЖЕНИЯ 
                match(current_position):
                    case(CatState.TOP):
                        transform = QTransform().rotate(90)
                    case(CatState.BOTTOM):
                        transform = QTransform().rotate(270)
                    case(CatState.LEFT):
                        transform = QTransform().rotate(180)
                    case(CatState.RIGHT):
                        transform = QTransform().rotate(0)
                
                main_cat_270 = self.main_cat.transformed(transform)
                eye_270=self.eye.transformed(transform)
                eye2_270=self.eye2.transformed(transform)
                eye_big_270=self.eye_big.transformed(transform)
                eye2_big_270=self.eye2_big.transformed(transform)
                values=[main_cat_270, eye_270, eye2_270, eye_big_270, eye2_big_270, QPoint(self.monitor_width, random_y), QPoint((self.monitor_width-self.cat_window_size)+self.CAT_GAP,random_y)]
                self.max_offset_x = 5  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
                self.max_offset_y = 10  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ
                self.cat_position=CatState.RIGHT

        return values
        


    #СЛУШАТЕЛЬ ЛЕВОГО КЛИКА МЫШИ
    def handle_left_click(self, x,y,left_pressed):
        
        
        #РАМКИ ОКНА КОТА
        window_rect = self.frameGeometry()

        #СРАБАТЫВАЕТ ПРИ ПРОСТОМ КЛИКЕ НА КОТА
        if not self.is_window_dragging and not left_pressed and window_rect.contains(QPoint(x, y)):
            self.hiding_cat_animation.setStartValue(self.pos())
            match(self.cat_position):
                case(CatState.BOTTOM):
                     self.hiding_cat_animation.setEndValue(QPoint(self.pos().x(),self.pos().y()+self.cat_window_size))
                case(CatState.TOP):
                    self.hiding_cat_animation.setEndValue(QPoint(self.pos().x(),self.pos().y()-self.cat_window_size))
                case(CatState.LEFT):
                    self.hiding_cat_animation.setEndValue(QPoint(self.pos().x()-self.cat_window_size,self.pos().y()))
                case(CatState.RIGHT):
                    self.hiding_cat_animation.setEndValue(QPoint(self.pos().x()+self.cat_window_size,self.pos().y()))
            if(not self.isOne):
                self.hiding_cat_animation.start()
            
        

        #СРАБАТЫВАЕТ КОГДА КОТ ПЕРЕМЕЩАЕТСЯ ЗА КУРСОРОМ И ЛЕВАЯ КНОПКА ОТПУСКАЕТСЯ
        if self.is_window_dragging:
           if not left_pressed:
                self.cat.setPixmap(self.cat_fall)
                self.fall_cat_animation.setStartValue(self.pos())
                self.fall_cat_animation.setEndValue(QPoint(self.pos().x(), self.pos().y()+self.monitor_height))
                self.fall_cat_animation.start()
                
        #СРАБАТЫВАЕТ КОГДА ЛЕВАЯ КНОПКА НАЖАТА В ОБЛАСТИ КОТА
        if left_pressed:
            if window_rect.contains(QPoint(x, y)):
                self.long_drag_timer.start()
                self.long_tap_x=x
                self.long_tap_y=y
        else:
            self.long_tap = False
            self.is_window_dragging = False
            self.long_drag_timer.stop()
        
    #ТАЙМЕР ДОЛГОГО ЗАЖАТИЯ
    def on_long_drag_timer_out(self):
        self.long_tap = True
        self.long_drag_timer.stop()
        
    #ФУНКЦИЯ ПЕРЕКЛЮЧЕНИЯ БОЛЬШИХ И МАЛЕНЬКИХ ГЛАЗ
    def on_timer_out(self):
        if self.isEyesBig:
            self.eye_l.setPixmap(self.eye_big)
            self.eye_r.setPixmap(self.eye2_big)
        else:
            self.eye_l.setPixmap(self.eye)
            self.eye_r.setPixmap(self.eye2)
        self.bigyeys_timer.stop()
        
    #СЛУШАТЕЛЬ МЫШИ
    def update_mouse_position(self, mouse_x, mouse_y):

        if(not self.dragging):
            self.cat.setPixmap(self.main_cat)
        self.move_cat_animation.setStartValue(self.pos())
        self.move_cat_animation.setEndValue(QPoint(mouse_x-int(self.cat_window_size/2), mouse_y-int(self.cat_window_size/3)))


    
        #ПРЯМОУГОЛЬНИК ОКНА КОТА
        window_rect = self.frameGeometry()
        self.original_size = self.cat.size()
        #ЕСЛИ МЫШЬ НАХОДИТСЯ В ПРЕДЕЛАХ ОКНА КОТА
        if window_rect.contains(QPoint(mouse_x, mouse_y)):

            #ЕСЛИ ДОЛГОЕ НАЖАТИЕ (2000 мс)
            if self.long_tap:
                    self.is_window_dragging = True
                    self.dragging=False
                    self.eye_l.setVisible(False)
                    self.eye_r.setVisible(False)
                    self.cat.setPixmap(self.cat_dragged)
                    self.move_cat_animation.start()

       

        # Преобразуем глобальные координаты мыши в координаты относительно окна
        mouse_pos = self.mapFromGlobal(QPoint(mouse_x, mouse_y))

         # Вычисляем расстояние от мыши до центра окна
        distance = math.sqrt((mouse_pos.x() - self.center_l.x()) ** 2 +
                            (mouse_pos.y() - self.center_l.y()) ** 2)
        
        
        # Если мышь в пределах 200 пикселей
        if self.isEyesBig:
            if distance > 200:
                self.bigyeys_timer.start()
                self.isEyesBig = False
        else:
            if distance <= 200:
                self.bigyeys_timer.start()
                self.isEyesBig = True

        # Обновляем положение левого глаза
        self.move_eye(self.eye_l, self.center_l, mouse_pos, self.eye_l_animation)
        self.move_eye(self.eye_r, self.center_r, mouse_pos, self.eye_r_animation)
       


    def move_eye(self, eye_label, center, mouse_pos, animation):
        delta_x = mouse_pos.x() - center.x()
        delta_y = mouse_pos.y() - center.y()

        # Вычисляем процентное соотношение для смещения глаза
        percent_x = delta_x / (self.width() / 2)  # Процент по горизонтали
        percent_y = delta_y / (self.height() / 2)  # Процент по вертикали

        # Ограничиваем процентное соотношение в диапазоне [-1, 1]
        percent_x = max(-1, min(1, percent_x))
        percent_y = max(-1, min(1, percent_y))

        # Вычисляем новое положение глаза
        new_x = center.x() + percent_x * self.max_offset_x
        new_y = center.y() + percent_y * self.max_offset_y

        # Ограничиваем движение глаза в пределах области
        min_x = center.x() - self.max_offset_x  # Минимальное положение по X
        max_x = center.x() + self.max_offset_x  # Максимальное положение по X
        min_y = center.y() - self.max_offset_y  # Минимальное положение по Y
        max_y = center.y() + self.max_offset_y  # Максимальное положение по Y

        new_x = max(min_x, min(max_x, new_x))  # Ограничиваем new_x в пределах [min_x, max_x]
        new_y = max(min_y, min(max_y, new_y))  # Ограничиваем new_y в пределах [min_y, max_y]

        # Устанавливаем новое положение глаза
        new_pos = QPoint(int(new_x - eye_label.width() / 2), int(new_y - eye_label.height() / 2))

        # Запускаем анимацию
        animation.setStartValue(eye_label.pos())
        animation.setEndValue(new_pos)
        animation.start()

    # Обработка нажатия клавиши
    def on_press(self, key):
        try:
            if not self.key_pressed:  # Нажатие клавиши
                if self.catTap:
                    self.cat.setPixmap(self.cat_1)  # Меняем изображение на третье
                    self.catTap = False
                else:
                    self.cat.setPixmap(self.cat_2)  # Меняем изображение на второе
                    self.catTap = True
                self.key_pressed = True
        except AttributeError:
            print(f"Нажата специальная клавиша: {key}")

    # Обработка отпускания клавиши
    def on_release(self, key):
        if self.key_pressed:
            self.cat.setPixmap(self.cat)  # Возвращаемся к первому изображению
            self.key_pressed = False

# Запуск приложения
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())