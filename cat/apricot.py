import math
import random
import sys
from pathlib import Path

import win32api
from PyQt5.QtCore import QPropertyAnimation, Qt, QRect, QPoint, QTimer, QThread, pyqtSignal, QEasingCurve, QSize
from PyQt5.QtGui import QPixmap, QTransform, QMovie
from PyQt5.QtWidgets import QApplication, QLabel
from pynput import keyboard, mouse

from cat.apricot_settings import ApricotSettingsWindow
from cat.cat_run import CatRun
from cat.fly import Fly
from cat.pacman import Pacman
from utils.character_abstract import Character
from utils.enums import CatState


# Дополнительны поток для отслеживания движения мыши
class MouseTrackerThread(QThread):
    mouse_moved = pyqtSignal(int, int)
    left_clicked = pyqtSignal(int, int, bool)

    def run(self):
        # Функция при движении мыши
        def on_move(x, y):
            self.mouse_moved.emit(x, y)

        # Функция при нажатии/отпускании кнопки мыши
        def on_click(x, y, button, pressed):
            if button == mouse.Button.left:
                self.left_clicked.emit(x, y, pressed)

        # Слушатель мыши
        with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
            listener.join()


class Cat(Character):
    def __init__(self, settings):
        super().__init__()

        # ПЕРЕМЕННЫЕ
        self.enable_pacman = settings["pacman"]
        self.enable_fly = settings["fly"]
        self.cat_hiding_delay = int(settings["cat_hiding_delay"])*1000    # ЗАДЕРЖКА ПЕРЕД ПОЯВЛЕНИЕМ
        self.isFlying = False
        self.cat_position = CatState.BOTTOM  # ПОЛОЖЕНИЕ КОТА НА ЭКРАНЕ
        self.cat_window_size = 300
        self.CAT_GAP = 40
        self.min_height = self.cat_window_size
        self.max_height = 400
        self.original_height = self.cat_window_size
        self.original_width = self.cat_window_size
        self.initial_pos = None
        self.eyes_distance = 250
        self.bottom_lapa_react_zone = QRect(0, 140, 90, 120)
        self.left_lapa_react_zone = QRect(40, 0, 120, 90)
        self.right_lapa_react_zone = QRect(150, 210, 120, 90)
        self.top_lapa_react_zone = QRect(210, 30, 90, 120)
        self.lapa_react_zone = self.bottom_lapa_react_zone
        self.pacman = Pacman()
        self.max_offset_x = 11  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
        self.max_offset_y = 5  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ
        self.pointer = 0
        self.crazy = CatRun(self)


        # ФЛАГИ
        self.isOne = False
        self.isLapaOut = False
        self.isEyesBig = False
        self.isTimerStarted = False
        self.setMouseTracking(True)
        self.dragging = False
        self.key_pressed = False         # КЛАВИША КЛАВИАТУРЫ НАЖАТА
        self.long_tap = False            # ФЛАГ ДОЛГОГО ЗАЖАТИЯ
        self.is_window_dragging = False  # КОТ ПЕРЕМЕЩАЕТСЯ
        self.is_stretching = False       # ФЛАГ РАССТЯГИВАНИЯ КОТА

        # ПОТОК ДЛЯ ОТСЛЕЖИВАНИЯ МЫШИ
        self.mouse_tracker = MouseTrackerThread()
        self.mouse_tracker.mouse_moved.connect(self.update_mouse_position)
        self.mouse_tracker.start()
        self.mouse_tracker.left_clicked.connect(self.handle_left_click)

        # РАЗМЕРЫ ОКНА МОНИТОРА
        self.monitor_width = QApplication.primaryScreen().geometry().width()
        self.monitor_height = QApplication.primaryScreen().geometry().height()

        # Настройки окна
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(QRect(100, (self.monitor_height - self.cat_window_size) + self.CAT_GAP, self.cat_window_size,
                               self.cat_window_size))

        # Определяем путь к каталогу с данными в зависимости от режима исполнения
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path is not None:
            # Мы находимся в упакованном виде (PyInstaller)
            app_directory = Path(base_path)
        else:
            # Обычный режим разработки
            app_directory = Path(__file__).parent.parent  # Найти родительский каталог проекта
        resource_path = app_directory / 'drawable' / 'cat'

        # ЗАГРУЖАЕМ ИЗОБРАЖЕНИЯ
        self.eye_left = QPixmap(str(resource_path / "eye.png"))
        self.eye_right = QPixmap(str(resource_path / "eye2.png"))
        self.eye_left_big = QPixmap(str(resource_path / "eye_big.png"))
        self.eye_right_big = QPixmap(str(resource_path / "eye2_big.png"))
        self.cat_dragged = QPixmap(str(resource_path / "cat_dragged.png"))
        self.cat_fall = QPixmap(str(resource_path / "cat_fall.png"))
        self.main_cat = QPixmap(str(resource_path / 'main_cat.png'))
        self.cat_pixmap_stat = QPixmap(str(resource_path / "cat_stat.png"))

        # ЗАГРУЖАЕМ ГИФКИ
        self.top_lapa_gif = QMovie(str(resource_path / "lapa_top.gif"))
        self.bottom_lapa_gif = QMovie(str(resource_path / "lapa.gif"))
        self.left_lapa_gif = QMovie(str(resource_path / "lapa_left.gif"))
        self.right_lapa_gif = QMovie(str(resource_path / "lapa_right.gif"))

        # ЛЕВЫЙ ГЛАЗ
        self.eye_l = QLabel(self)
        self.eye_l.setPixmap(self.eye_left)
        self.eye_l.setGeometry(0, 0, self.cat_window_size, self.cat_window_size)
        self.eye_l.setMouseTracking(True)

        # АНИМАЦИЯ ДВИЖЕНИЯ ЛЕВОГО ГЛАЗА
        self.eye_l_animation = QPropertyAnimation(self.eye_l, b"pos")
        self.eye_l_animation.setDuration(200)
        self.center_l = self.eye_l.geometry().center()  # Центр левого глаза

        # ПРАВЫЙ ГЛАЗ
        self.eye_r = QLabel(self)
        self.eye_r.setPixmap(self.eye_right)
        self.eye_r.setGeometry(0, 0, self.cat_window_size, self.cat_window_size)
        self.eye_r.setMouseTracking(True)

        # АНИМАЦИЯ ДВИЖЕНИЯ ПРАВОГО ГЛАЗА
        self.eye_r_animation = QPropertyAnimation(self.eye_r, b"pos")
        self.eye_r_animation.setDuration(200)
        self.center_r = self.eye_r.geometry().center()  # Центр правого глаза

        # КОТ
        self.cat = QLabel(self)
        self.cat.setGeometry(0, 0, self.cat_window_size, self.cat_window_size)
        self.cat.setPixmap(self.main_cat)
        self.cat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cat.setMouseTracking(True)

        # ЛАПА КОТА
        self.lapa = QLabel(self)
        self.lapa_gif = self.bottom_lapa_gif
        self.lapa_gif.setScaledSize(QSize(120, 140))
        self.lapa.setMovie(self.lapa_gif)
        self.lapa.setGeometry(5, 150, 111, 111)
        self.lapa.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lapa.setMouseTracking(True)

        # АНИМАЦИЯ ПЕРЕТАСКИВАНИЯ КОТА МЫШКОЙ
        self.move_cat_animation = QPropertyAnimation(self, b"pos")
        self.move_cat_animation.setDuration(20)

        # АНИМАЦИЯ ПАДЕНИЯ КОТА
        self.fall_cat_animation = QPropertyAnimation(self, b"pos")
        self.fall_cat_animation.finished.connect(self.cat_preparing)
        self.fall_cat_animation.setDuration(400)

        # АНИМАЦИЯ ВЫГЛЯДЫВАНИЯ КОТА ИЗ РАЗНЫХ МЕСТ
        self.cat_coming_animation = QPropertyAnimation(self, b"pos")
        self.cat_coming_animation.setDuration(1500)

        # АНИМАЦИЯ СКРЫВАЮЩЕГОСЯ КОТА
        self.hiding_cat_animation = QPropertyAnimation(self, b"pos")
        self.hiding_cat_animation.finished.connect(self.cat_preparing)
        self.hiding_cat_animation.setDuration(300)

        # АНИМАЦИЯ КОТА-ПРУЖИНКИ
        self.bounce_animation = QPropertyAnimation(self.cat, b"geometry")
        self.bounce_animation.setDuration(800)
        self.bounce_animation.setEasingCurve(QEasingCurve.Type.OutElastic)

        # АНИМАЦИЯ ПОЯВЛЕНИЯ ЛАПЫ
        self.throw_lapa_animation = QPropertyAnimation(self.lapa, b"pos")
        self.throw_lapa_animation.setDuration(200)
        self.throw_lapa_animation.setStartValue(QPoint(self.lapa.pos().x(), self.lapa.pos().y() + 100))
        self.throw_lapa_animation.setEndValue(self.lapa.pos())

        # АНИМАЦИЯ СКРЫТИЯ ЛАПЫ
        self.hide_lapa_animation = QPropertyAnimation(self.lapa, b"pos")
        self.hide_lapa_animation.setDuration(200)
        self.hide_lapa_animation.setStartValue(self.lapa.pos())
        self.hide_lapa_animation.setEndValue(QPoint(self.lapa.pos().x(), self.lapa.pos().y() + 100))

        # ТАЙМЕР НА РАСШИРЕНИЕ ГЛАЗ (500 мс)
        self.bigeyes_timer = QTimer(self)
        self.bigeyes_timer.setInterval(500)
        self.bigeyes_timer.timeout.connect(self.do_big_eyes)

        # ТАЙМЕР НА СУЖЕНИЕ ГЛАЗ (500 мс)
        self.small_eyes_timer = QTimer(self)
        self.small_eyes_timer.setInterval(500)
        self.small_eyes_timer.timeout.connect(self.do_small_eyes)

        # ТАЙМЕР НА LONG TAP НА КОТЕ (2 секунды)
        self.long_drag_timer = QTimer(self)
        self.long_drag_timer.setInterval(1000)
        self.long_drag_timer.timeout.connect(self.on_long_drag_timer_out)

        # СЛУШАТЕЛЬ КЛАВИАТУРЫ
        if self.enable_pacman:
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            self.listener.start()


    def start_fly(self):
        self.fly = Fly(self)
        self.fly.position_changed.connect(self.on_fly_update)
        self.fly.finished.connect(self.on_fly_finished)
        self.fly.show()
        self.fly.anim.start()
        self.isFlying = True

    def on_fly_finished(self):
        self.isFlying = False
        self.fly.deleteLater()

    def on_fly_update(self, x, y):
        mouse_pos = self.cat.mapFromGlobal(QPoint(x, y))
        self.move_eye(self.eye_l, self.center_l, QPoint(mouse_pos.x(), mouse_pos.y()), self.eye_l_animation)
        self.move_eye(self.eye_r, self.center_r, QPoint(mouse_pos.x(), mouse_pos.y()), self.eye_r_animation)
        window_rect = self.cat.frameGeometry()
        if window_rect.contains(mouse_pos) and not self.isHidden():
            self.hide()
            self.crazy.run_crazy_start(self.pos().x())



    # СЛУШАТЕЛЬ НАЖАТИЯ МЫШИ В ПРЕДЕЛАХ КОТА
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.isOne = not self.isOne
            self.initial_pos = event.pos()
            self.original_height = self.cat.height()
            self.original_y = self.cat.y()
            self.bounce_animation.stop()
        else:
            super().mousePressEvent(event)


    # СЛУШАТЕЛЬ ДВИЖЕНИЯ МЫШИ В ПРЕДЕЛАХ КОТА
    def mouseMoveEvent(self, event):
        if self.dragging and self.initial_pos is not None:
            match self.cat_position:
                case (CatState.TOP):
                    # Вычисляем разницу в положении курсора
                    delta = event.pos().y() - self.initial_pos.y()
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
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation).transformed(transform))

                case (CatState.BOTTOM):
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
                    new_y = self.original_y - (new_height - self.original_height)

                    # Обновляем геометрию изображения
                    self.cat.setGeometry(
                        self.cat.x(),
                        new_y,
                        self.cat.width(),
                        new_height
                    )
                    transform = QTransform().rotate(0)

                    # Масштабируем изображение
                    self.cat.setPixmap(self.cat_pixmap_stat.scaled(
                        self.cat.width(), new_height,
                        Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation).transformed(
                        transform))

                case (CatState.LEFT):
                    # Разница по горизонтали (движение вправо увеличивает ширину)
                    delta = event.pos().x() - self.initial_pos.x()

                    new_height = self.original_width + delta
                    # Ограничения
                    if new_height < self.cat_window_size:  # Минимальный размер
                        new_height = self.cat_window_size
                    if new_height > self.max_height:  # Максимальный размер
                        new_height = self.max_height

                    # Обновляем геометрию
                    self.cat.setGeometry(
                        self.cat.x(),
                        self.cat.y(),
                        new_height,
                        self.cat.height()
                    )

                    transform = QTransform().rotate(90)
                    self.cat.setPixmap(self.cat_pixmap_stat.scaled(
                        self.cat.height(),
                        new_height,
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    ).transformed(transform))

                case (CatState.RIGHT):

                    delta = self.initial_pos.x() - event.pos().x()

                    new_height = self.original_width + delta

                    # Ограничения
                    if new_height < self.cat_window_size:
                        new_height = self.cat_window_size
                    if new_height > self.max_height:
                        new_height = self.max_height

                    # Обновляем геометрию (ширина остаётся прежней, меняется высота)
                    self.cat.setGeometry(
                        self.cat.x() - (new_height - self.cat.width()),
                        self.cat.y(),
                        new_height,
                        self.cat.height()
                    )

                    transform = QTransform().rotate(270)
                    self.cat.setPixmap(self.cat_pixmap_stat.scaled(
                        self.cat.height(),
                        new_height,
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    ).transformed(transform))

            event.accept()


    # СЛУШАТЕЛЬ ОТПУСКАНИЯ МЫШИ В ПРЕДЕЛАХ КОТА
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            self.dragging = False
            self.initial_pos = None

            self.cat.setPixmap(self.main_cat)

            target_rect = QRect(
                0,
                self.height() - self.cat_window_size,
                self.cat_window_size,
                self.cat_window_size
            )

            self.bounce_animation.setStartValue(self.cat.geometry())
            self.bounce_animation.setEndValue(target_rect)
            self.bounce_animation.start()

            event.accept()


    # СЛУШАТЕЛЬ ЛЕВОГО КЛИКА МЫШИ
    def handle_left_click(self, x, y, left_pressed):
        # if not left_pressed:
        #     print (f"{x}  {y}")

        # РАМКИ ОКНА КОТА
        window_rect = self.frameGeometry()
        # СРАБАТЫВАЕТ ПРИ ПРОСТОМ КЛИКЕ НА КОТА
        if not self.is_window_dragging and not left_pressed and window_rect.contains(QPoint(x, y)):
            self.hiding_cat_animation.setStartValue(self.pos())
            match self.cat_position:
                case (CatState.BOTTOM):
                    self.hiding_cat_animation.setEndValue(QPoint(self.pos().x(), self.pos().y() + self.cat_window_size))
                case (CatState.TOP):
                    self.hiding_cat_animation.setEndValue(QPoint(self.pos().x(), self.pos().y() - self.cat_window_size))
                case (CatState.LEFT):
                    self.hiding_cat_animation.setEndValue(QPoint(self.pos().x() - self.cat_window_size, self.pos().y()))
                case (CatState.RIGHT):
                    self.hiding_cat_animation.setEndValue(QPoint(self.pos().x() + self.cat_window_size, self.pos().y()))
            if not self.isOne:
                self.hiding_cat_animation.start()

        # СРАБАТЫВАЕТ, КОГДА КОТ ПЕРЕМЕЩАЕТСЯ ЗА КУРСОРОМ И ЛЕВАЯ КНОПКА ОТПУСКАЕТСЯ
        if self.is_window_dragging:
            if not left_pressed:
                self.cat.setPixmap(self.cat_fall)
                self.fall_cat_animation.setStartValue(self.pos())
                self.fall_cat_animation.setEndValue(QPoint(self.pos().x(), self.pos().y() + self.monitor_height))
                self.fall_cat_animation.start()

        # СРАБАТЫВАЕТ КОГДА ЛЕВАЯ КНОПКА НАЖАТА В ОБЛАСТИ КОТА
        if left_pressed:
            if window_rect.contains(QPoint(x, y)):
                self.long_drag_timer.start()

        else:
            self.long_tap = False
            self.is_window_dragging = False
            self.long_drag_timer.stop()

    # ТАЙМЕР ДОЛГОГО ЗАЖАТИЯ
    def on_long_drag_timer_out(self):
        self.long_tap = True
        self.long_drag_timer.stop()

    # ФУНКЦИЯ ПЕРЕКЛЮЧЕНИЯ БОЛЬШИХ ГЛАЗ
    def do_big_eyes(self):
        self.isEyesBig = True
        self.eye_l.setPixmap(self.eye_left_big)
        self.eye_r.setPixmap(self.eye_right_big)
        self.bigeyes_timer.stop()

    # ФУНКЦИЯ УСТАНОВКИ МАЛЕНЬКИХ ГЛАЗ
    def do_small_eyes(self):
        self.isEyesBig = False
        self.eye_l.setPixmap(self.eye_left)
        self.eye_r.setPixmap(self.eye_right)
        self.small_eyes_timer.stop()

    # ФУНКЦИЯ "ДОСТАТЬ ЛАПУ"
    def throwLapa(self):
        if not self.isLapaOut:
            match (self.cat_position):
                case (CatState.BOTTOM):
                    self.lapa_gif.start()
                case (CatState.TOP):
                    self.top_lapa_gif.start()
                case (CatState.LEFT):
                    self.left_lapa_gif.start()
                case (CatState.RIGHT):
                    self.right_lapa_gif.start()
            self.throw_lapa_animation.start()
            self.isLapaOut = True

    # ФУНКЦИЯ "СПРЯТАТЬ ЛАПУ"
    def hideLapa(self):
        if self.isLapaOut:
            self.hide_lapa_animation.start()
            self.isLapaOut = False

    # СЛУШАТЕЛЬ МЫШИ
    def update_mouse_position(self, mouse_x, mouse_y):

        local_pos = self.mapFromGlobal(QPoint(mouse_x, mouse_y))

        # Проверяем, находится ли курсор в пределах окна
        if self.lapa_react_zone.contains(local_pos):
            self.lapa.setVisible(True)
            if not self.isLapaOut and self.isEyesBig:
                self.throwLapa()
        else:
            if self.isLapaOut:
                self.hideLapa()

        self.move_cat_animation.setStartValue(self.pos())
        self.move_cat_animation.setEndValue(
            QPoint(mouse_x - int(self.cat_window_size / 2), mouse_y - int(self.cat_window_size / 3)))

        # ПРЯМОУГОЛЬНИК ОКНА КОТА
        window_rect = self.frameGeometry()

        # ЕСЛИ МЫШЬ НАХОДИТСЯ В ПРЕДЕЛАХ ОКНА КОТА
        if window_rect.contains(QPoint(mouse_x, mouse_y)):
            # ЕСЛИ ДОЛГОЕ НАЖАТИЕ (2000 мс)
            if self.long_tap:
                self.is_window_dragging = True
                self.dragging = False
                self.eye_l.setVisible(False)
                self.eye_r.setVisible(False)
                self.cat.setPixmap(self.cat_dragged)
                self.cat.setGeometry((self.cat_window_size - self.cat_dragged.width()), 0, self.cat_window_size,
                                     self.cat_window_size)
                self.lapa.setVisible(False)
                self.move_cat_animation.start()

        # Преобразуем глобальные координаты мыши в координаты относительно окна
        mouse_pos = self.mapFromGlobal(QPoint(mouse_x, mouse_y))

        # Вычисляем расстояние от мыши до центра окна
        distance = math.sqrt((mouse_pos.x() - self.center_l.x()) ** 2 +
                             (mouse_pos.y() - self.center_l.y()) ** 2)

        # Если мышь в пределах 200 пикселей
        if distance > self.eyes_distance and not self.small_eyes_timer.isActive():
            self.small_eyes_timer.start()

        if distance <= self.eyes_distance and not self.bigeyes_timer.isActive():
            self.bigeyes_timer.start()

        if not self.isFlying:
            self.move_eye(self.eye_l, self.center_l, mouse_pos, self.eye_l_animation)
            self.move_eye(self.eye_r, self.center_r, mouse_pos, self.eye_r_animation)

    # ФУНКЦИЯ ПЕРЕВОРОТА И ПОЯВЛЕНИЯ КОТА
    def cat_preparing(self):
        all_cat_states = list(CatState)
        position = random.choice(all_cat_states)
        values = self.random_rotate(self.cat_position, position)
        self.main_cat = values[0]
        self.eye_left = values[1]
        self.eye_right = values[2]
        self.eye_left_big = values[3]
        self.eye_right_big = values[4]
        self.eye_l.setVisible(True)
        self.eye_r.setVisible(True)

        self.cat.setPixmap(self.main_cat)
        self.cat.setGeometry(0, 0, self.cat_window_size, self.cat_window_size)
        self.eye_l.setPixmap(self.eye_left)
        self.eye_r.setPixmap(self.eye_right)
        self.cat_coming_animation.setStartValue(values[5])
        self.cat_coming_animation.setEndValue(values[6])
        self.lapa.setVisible(False)

        QTimer.singleShot(self.cat_hiding_delay, lambda: (
            self.cat_coming_animation.start(),
            self.start_fly() if self.enable_fly and position == CatState.BOTTOM and random.randint(1, 20) == 1 else None
        ))


    # ФУНКЦИЯ ПОВОРОТА КОТА И ГЛАЗ В ЗАВИСИМОСТИ ОТ ВЫБРАННОГО И ТЕКУЩЕГО ПОЛОЖЕНИЯ КОТА
    def random_rotate(self, current_position, direction):
        values = []
        transform = None
        match direction:
            case CatState.TOP:
                random_x = random.randint(0, self.monitor_width - self.cat_window_size)

                # ПРОВЕРКА И ПОВОРОТ В ЗАВИСИМОСТИ ОТ ТЕКУЩЕГО ПОЛОЖЕНИЯ
                match current_position:
                    case (CatState.TOP):
                        transform = QTransform().rotate(0)
                    case (CatState.BOTTOM):
                        transform = QTransform().rotate(180)
                    case (CatState.LEFT):
                        transform = QTransform().rotate(90)
                    case (CatState.RIGHT):
                        transform = QTransform().rotate(270)

                self.top_lapa_gif.setScaledSize(QSize(120, 140))
                self.lapa.setMovie(self.top_lapa_gif)
                self.lapa.setGeometry(190, 40, 111, 111)

                self.lapa_react_zone = self.top_lapa_react_zone
                self.throw_lapa_animation.setStartValue(QPoint(self.lapa.pos().x(), self.lapa.pos().y() - 100))
                self.throw_lapa_animation.setEndValue(self.lapa.pos())

                self.hide_lapa_animation.setStartValue(self.lapa.pos())
                self.hide_lapa_animation.setEndValue(QPoint(self.lapa.pos().x(), self.lapa.pos().y() - 100))

                main_cat_180 = self.main_cat.transformed(transform)
                eye_180 = self.eye_left.transformed(transform)
                eye2_180 = self.eye_right.transformed(transform)
                eye_big_180 = self.eye_left_big.transformed(transform)
                eye2_big_180 = self.eye_right_big.transformed(transform)
                values = [main_cat_180, eye_180, eye2_180, eye_big_180, eye2_big_180,
                          QPoint(random_x, 0 - self.cat_window_size), QPoint(random_x, 0 - self.CAT_GAP)]
                self.cat_position = CatState.TOP

            case CatState.BOTTOM:
                random_x = random.randint(0, self.monitor_width - self.cat_window_size)

                # ПРОВЕРКА И ПОВОРОТ В ЗАВИСИМОСТИ ОТ ТЕКУЩЕГО ПОЛОЖЕНИЯ
                match current_position:
                    case (CatState.TOP):
                        transform = QTransform().rotate(180)
                    case (CatState.BOTTOM):
                        transform = QTransform().rotate(0)
                    case (CatState.LEFT):
                        transform = QTransform().rotate(270)
                    case (CatState.RIGHT):
                        transform = QTransform().rotate(90)

                self.lapa.setMovie(self.lapa_gif)
                self.lapa.setGeometry(5, 150, 111, 111)

                self.lapa_react_zone = self.bottom_lapa_react_zone
                self.throw_lapa_animation.setStartValue(QPoint(self.lapa.pos().x(), self.lapa.pos().y() + 100))
                self.throw_lapa_animation.setEndValue(self.lapa.pos())

                self.hide_lapa_animation.setStartValue(self.lapa.pos())
                self.hide_lapa_animation.setEndValue(QPoint(self.lapa.pos().x(), self.lapa.pos().y() + 100))

                main_cat_0 = self.main_cat.transformed(transform)
                eye_0 = self.eye_left.transformed(transform)
                eye2_0 = self.eye_right.transformed(transform)
                eye_big_0 = self.eye_left_big.transformed(transform)
                eye2_big_0 = self.eye_right_big.transformed(transform)
                values = [main_cat_0, eye_0, eye2_0, eye_big_0, eye2_big_0, QPoint(random_x, self.monitor_height),
                          QPoint(random_x, (self.monitor_height - self.cat_window_size) + self.CAT_GAP)]
                self.cat_position = CatState.BOTTOM

            case CatState.LEFT:
                random_y = random.randint(0, self.monitor_height - self.cat_window_size)

                # ПРОВЕРКА И ПОВОРОТ В ЗАВИСИМОСТИ ОТ ТЕКУЩЕГО ПОЛОЖЕНИЯ
                match current_position:
                    case (CatState.TOP):
                        transform = QTransform().rotate(270)
                    case (CatState.BOTTOM):
                        transform = QTransform().rotate(90)
                    case (CatState.LEFT):
                        transform = QTransform().rotate(0)
                    case (CatState.RIGHT):
                        transform = QTransform().rotate(180)

                self.left_lapa_gif.setScaledSize(QSize(140, 120))
                self.lapa.setMovie(self.left_lapa_gif)
                self.lapa.setGeometry(40, 0, 111, 111)

                self.lapa_react_zone = self.left_lapa_react_zone
                self.throw_lapa_animation.setStartValue(QPoint(self.lapa.pos().x() - 100, self.lapa.pos().y()))
                self.throw_lapa_animation.setEndValue(self.lapa.pos())

                self.hide_lapa_animation.setStartValue(self.lapa.pos())
                self.hide_lapa_animation.setEndValue(QPoint(self.lapa.pos().x() - 100, self.lapa.pos().y()))

                main_cat_90 = self.main_cat.transformed(transform)
                eye_90 = self.eye_left.transformed(transform)
                eye2_90 = self.eye_right.transformed(transform)
                eye_big_90 = self.eye_left_big.transformed(transform)
                eye2_big_90 = self.eye_right_big.transformed(transform)
                values = [main_cat_90, eye_90, eye2_90, eye_big_90, eye2_big_90,
                          QPoint(0 - self.cat_window_size, random_y), QPoint(0 - self.CAT_GAP, random_y)]
                self.max_offset_x = 5  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
                self.max_offset_y = 10  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ
                self.cat_position = CatState.LEFT

            case CatState.RIGHT:
                random_y = random.randint(0, self.monitor_height - self.cat_window_size)

                # ПРОВЕРКА И ПОВОРОТ В ЗАВИСИМОСТИ ОТ ТЕКУЩЕГО ПОЛОЖЕНИЯ
                match current_position:
                    case (CatState.TOP):
                        transform = QTransform().rotate(90)
                    case (CatState.BOTTOM):
                        transform = QTransform().rotate(270)
                    case (CatState.LEFT):
                        transform = QTransform().rotate(180)
                    case (CatState.RIGHT):
                        transform = QTransform().rotate(0)

                self.right_lapa_gif.setScaledSize(QSize(140, 120))
                self.lapa.setMovie(self.right_lapa_gif)
                self.lapa.setGeometry(150, 190, 111, 111)

                self.lapa_react_zone = self.right_lapa_react_zone
                self.throw_lapa_animation.setStartValue(QPoint(self.lapa.pos().x() + 100, self.lapa.pos().y()))
                self.throw_lapa_animation.setEndValue(self.lapa.pos())

                self.hide_lapa_animation.setStartValue(self.lapa.pos())
                self.hide_lapa_animation.setEndValue(QPoint(self.lapa.pos().x() + 100, self.lapa.pos().y()))

                main_cat_270 = self.main_cat.transformed(transform)
                eye_270 = self.eye_left.transformed(transform)
                eye2_270 = self.eye_right.transformed(transform)
                eye_big_270 = self.eye_left_big.transformed(transform)
                eye2_big_270 = self.eye_right_big.transformed(transform)
                values = [main_cat_270, eye_270, eye2_270, eye_big_270, eye2_big_270,
                          QPoint(self.monitor_width, random_y),
                          QPoint((self.monitor_width - self.cat_window_size) + self.CAT_GAP, random_y)]
                self.max_offset_x = 5  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
                self.max_offset_y = 10  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ
                self.cat_position = CatState.RIGHT

        return values

    # ФУНКЦИЯ ДВИЖЕНИЯ ГЛАЗ
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

    # ОБРАБОТКА НАЖАТИЯ НА КЛАВИАТУРУ
    def on_press(self, key):
        try:
            layout_id = 'ru' if win32api.GetKeyboardLayout(0) & 0xFFFF == 0x0419 else 'en'
        except:
            layout_id = 'en'

        try:
            char = key.char.lower()
        except AttributeError:
            return

        word = 'пакмен' if layout_id == 'ru' else 'pacman'

        if char == word[self.pointer]:
            self.pointer += 1
        else:
            self.pointer = 0

        if self.pointer == len(word):
            QTimer.singleShot(0, self.safe_start_pacman)
            self.pointer = 0

    def safe_start_pacman(self):
        self.pacman.show_and_start()

    # ОБРАБОТКА ОТПУСКАНИЯ КЛАВИШИ КЛАВИАТУРЫ
    def on_release(self, key):
        pass

    @staticmethod
    def getSettingWindow(root_container,settings):
        return ApricotSettingsWindow(root_container,settings)

