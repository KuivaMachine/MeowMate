import math
import random
from pathlib import Path

from PyQt5.QtCore import QPropertyAnimation, Qt, QRect, QPoint, QTimer, QThread, pyqtSignal, QEasingCurve, QSize
from PyQt5.QtGui import QPixmap, QTransform, QMovie
from PyQt5.QtWidgets import QApplication, QLabel
from pynput import mouse

from cat.apricot_settings import ApricotSettingsWindow
from cat.cat_run import CatRun
from cat.fly import Fly
from cat.pacman import Pacman
from utils.character_abstract import Character
from utils.enums import CatState


# ПОТОК ДЛЯ ОТСЛЕЖИВАНИЯ МЫШИ
class MouseTrackerThread(QThread):
    mouse_moved = pyqtSignal(int, int)
    left_clicked = pyqtSignal(bool)
    def run(self):
        # движение мыши
        def on_move(x, y):
            self.mouse_moved.emit(x, y)
        # Нажатие/отпускание левой кнопки мыши
        def on_click(x, y, button, pressed):
            if button == mouse.Button.left:
                self.left_clicked.emit(pressed)
        # Слушатель
        with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
            listener.join()


class Cat(Character):
    def __init__(self, settings, is_first_cat_instance):
        super().__init__()

        # ПЕРЕМЕННЫЕ
        self.enable_pacman = settings["pacman"]                             # ПАКМАН РАЗРЕШЕН
        self.enable_fly = settings["fly"]                                   # МУХА РАЗРЕШЕНА
        self.cat_hiding_delay = int(settings["cat_hiding_delay"]) * 1000    # ЗАДЕРЖКА ПЕРЕД ПОЯВЛЕНИЕМ
        self.cat_position = CatState.BOTTOM                                 # ПОЛОЖЕНИЕ КОТА НА ЭКРАНЕ
        self.cat_window_size = 300                                          # РАЗМЕР ОКНА
        self.CAT_GAP = 40                                                   # ВЕЛИЧИНА СМЕЩЕНИЯ КОТА ВНИЗ ЗА ПРЕДЕЛ ЭКРАНА
        self.min_height = self.cat_window_size                              # МИНИМАЛЬНАЯ ВЫСОТА КОТА
        self.max_height = 400                                               # МАКСИМАЛЬНАЯ ВЫСОТА КОТА
        self.original_height = self.cat_window_size                         # НАЧАЛЬНАЯ ВЫСОТА КОТА ПЕРЕД РАСТЯГИВАЕМ
        self.original_width = self.cat_window_size                          # НАЧАЛЬНАЯ ШИРИНА КОТА ПЕРЕД РАСТЯГИВАЕМ
        self.initial_pos = None                                             # НАЧАЛЬНАЯ ПОЗИЦИЯ ДЛЯ РАСТЯГИВАНИЯ КОТА
        self.eyes_distance = 250                                            # МИНИМАЛЬНАЯ ДИСТАНЦИЯ ДЛЯ НАЧАЛА РАСШИРЕНИЯ ГЛАЗ
        self.bottom_lapa_react_zone = QRect(0, 140, 90, 120)                # ЗОНА РЕАКЦИИ ДЛЯ ЛАПЫ КОТА, КОГДА КОТ СНИЗУ
        self.top_lapa_react_zone = QRect(210, 30, 90, 120)                  # ЗОНА РЕАКЦИИ ДЛЯ ЛАПЫ КОТА, КОГДА КОТ СВЕРХУ
        self.left_lapa_react_zone = QRect(40, 0, 120, 90)                   # ЗОНА РЕАКЦИИ ДЛЯ ЛАПЫ КОТА, КОГДА КОТ СЛЕВА
        self.right_lapa_react_zone = QRect(150, 210, 120, 90)               # ЗОНА РЕАКЦИИ ДЛЯ ЛАПЫ КОТА, КОГДА КОТ СПРАВА
        self.lapa_react_zone = self.bottom_lapa_react_zone                  # ТЕКУЩАЯ ЗОНА РЕАКЦИИ ДЛЯ ЛАПЫ КОТА
        self.max_eyes_offset_x = 11                                         # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
        self.max_eyes_offset_y = 5                                          # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ
        self.pointer = 0

        # ФЛАГИ
        self.is_first_cat_instance = is_first_cat_instance                  # ЯВЛЯЕТСЯ ЛИ КОТ ЕДИНСТВЕННЫМ ИЗ СОЗДАННЫХ
        self.is_it_second_click = False                                     # ФЛАГ, ОЗНАЧАЮЩИЙ ПЕРВЫЙ ЭТО КЛИК ПО КОТУ ИЛИ НЕТ
        self.isFlying = False                                               # МУХА ЛЕТАЕТ
        self.isLapaOut = False                                              # ЛАПА ИГРАЕТ
        self.isEyesBig = False                                              # ГЛАЗА РАСШИРЕНЫ
        self.dragging = False                                               # КОТ РАССТЯГИВАЕТСЯ СЕЙЧАС
        self.key_pressed = False                                            # КЛАВИША КЛАВИАТУРЫ НАЖАТА
        self.is_window_dragging = False                                     # КОТ ПЕРЕМЕЩАЕТСЯ
        self.is_stretching = False                                          # ФЛАГ РАССТЯГИВАНИЯ КОТА

        # ПОТОК ДЛЯ ОТСЛЕЖИВАНИЯ МЫШИ
        mouse_tracker = MouseTrackerThread()
        mouse_tracker.mouse_moved.connect(self.update_mouse_position)
        mouse_tracker.left_clicked.connect(self.update_mouse_left_click)
        mouse_tracker.start()

        # РАЗМЕРЫ ОКНА МОНИТОРА
        self.monitor_width = QApplication.primaryScreen().geometry().width()
        self.monitor_height = QApplication.primaryScreen().geometry().height()

        # НАСТРОЙКИ ОКНА

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint|
                            Qt.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(QRect(800, (self.monitor_height - self.cat_window_size) + self.CAT_GAP, self.cat_window_size,
                               self.cat_window_size))

        app_directory = Path(__file__).parent.parent  # Ищет родительский каталог проекта
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
        self.center_l = self.eye_l.geometry().center()  # Центр левого глаза

        # ПРАВЫЙ ГЛАЗ
        self.eye_r = QLabel(self)
        self.eye_r.setPixmap(self.eye_right)
        self.eye_r.setGeometry(0, 0, self.cat_window_size, self.cat_window_size)
        self.center_r = self.eye_r.geometry().center()  # Центр правого глаза

        # КОТ
        self.cat = QLabel(self)
        self.cat.setGeometry(0, 0, self.cat_window_size, self.cat_window_size)
        self.cat.setPixmap(self.main_cat)
        self.cat.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ЛАПА КОТА
        self.lapa = QLabel(self)
        self.lapa.setMouseTracking(False)
        self.lapa_gif = self.bottom_lapa_gif
        self.lapa_gif.setScaledSize(QSize(120, 140))
        self.lapa.setMovie(self.lapa_gif)
        self.lapa.setGeometry(5, 150, 111, 111)
        self.lapa.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # АНИМАЦИЯ ПЕРЕТАСКИВАНИЯ КОТА МЫШКОЙ
        self.move_cat_animation = QPropertyAnimation(self, b"pos")
        self.move_cat_animation.setDuration(20)

        # АНИМАЦИЯ ПАДЕНИЯ КОТА
        self.fall_cat_animation = QPropertyAnimation(self, b"pos")
        self.fall_cat_animation.finished.connect(self.cat_preparing)
        self.fall_cat_animation.setDuration(350)

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
        self.hide_lapa_animation.setEndValue(QPoint(self.lapa.pos().x(), self.lapa.pos().y() + 200))

        # ТАЙМЕР НА РАСШИРЕНИЕ ГЛАЗ (500 мс)
        self.bigeyes_timer = QTimer(self)
        self.bigeyes_timer.setInterval(500)
        self.bigeyes_timer.timeout.connect(self.do_big_eyes)

        # ТАЙМЕР НА СУЖЕНИЕ ГЛАЗ (500 мс)
        self.small_eyes_timer = QTimer(self)
        self.small_eyes_timer.setInterval(500)
        self.small_eyes_timer.timeout.connect(self.do_small_eyes)

        # ТАЙМЕР НА LONG TAP НА КОТЕ
        self.long_drag_timer = QTimer(self)
        self.long_drag_timer.setInterval(150)
        self.long_drag_timer.timeout.connect(self.on_long_drag_timer_out)

    # ЗАПУСК МУХИ
    def start_fly(self):
        self.fly = Fly(self)
        self.fly.position_changed.connect(self.on_fly_update)
        self.fly.finished.connect(self.on_fly_finished)
        self.fly.show()
        self.fly.anim.start()
        self.isFlying = True

    # ПОСЛЕ ПОЛЕТА МУХИ
    def on_fly_finished(self):
        self.isFlying = False
        self.fly.deleteLater()

    # ВО ВРЕМЯ ПОЛЕТА МУХИ
    def on_fly_update(self, x, y):
        mouse_pos = self.cat.mapFromGlobal(QPoint(x, y))
        self.move_eye(self.eye_l, self.center_l, QPoint(mouse_pos.x(), mouse_pos.y()))
        self.move_eye(self.eye_r, self.center_r, QPoint(mouse_pos.x(), mouse_pos.y()))
        window_rect = self.cat.frameGeometry()
        if window_rect.contains(mouse_pos) and not self.isHidden():
            self.hide()
            self.crazy = CatRun(self)
            self.crazy.run_crazy_start(self.pos().x())

    # ГЛОБАЛЬНЫЙ СЛУШАТЕЛЬ НАЖАТИЯ ЛЕВОЙ КНОПКИ
    def update_mouse_left_click(self, pressed):
        if not pressed:
            self.long_drag_timer.stop()

    # СКРЫВАНИЕ КОТА ЗА ЭКРАН
    def hide_cat(self):
        if self.is_it_second_click:
            self.is_it_second_click = False
            self.is_window_dragging = False
            self.long_drag_timer.stop()
            self.hiding_cat_animation.start()
        else:
            self.is_it_second_click = True

    # СЛУШАТЕЛЬ НАЖАТИЯ МЫШИ В ПРЕДЕЛАХ КОТА
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
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

            self.dragging = True
            self.drag_pos = event.globalPos()
            self.initial_pos = event.pos()
            self.original_height = self.cat.height()
            self.original_y = self.cat.y()
            self.bounce_animation.stop()
            if not self.isFlying:
                self.long_drag_timer.start()
            super().mousePressEvent(event)

        elif event.button() == Qt.MouseButton.RightButton:
            if not self.is_window_dragging:
                super().mousePressEvent(event)
            else:
                self.fall()
                self.is_window_dragging = False
                self.long_drag_timer.stop()


    # АНИМАЦИЯ ПАДЕНИЯ КОТА ПОСЛЕ ОТПУСКАНИЯ
    def fall(self):
        if self.is_window_dragging:
            self.is_window_dragging = False
            self.cat.setPixmap(self.cat_fall)
            self.fall_cat_animation.setStartValue(self.pos())
            self.fall_cat_animation.setEndValue(QPoint(self.pos().x(), self.pos().y() + self.monitor_height))
            self.fall_cat_animation.start()
        else:
            return

    # СЛУШАТЕЛЬ ОТПУСКАНИЯ МЫШИ В ПРЕДЕЛАХ КОТА
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.dragging:
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

            if self.is_window_dragging:
                self.fall()
            else:
                self.hide_cat()

    # СЛУШАТЕЛЬ ДВИЖЕНИЯ МЫШИ В ПРЕДЕЛАХ КОТА
    def mouseMoveEvent(self, event):
        if not self.dragging:
            return

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

    # ТАЙМЕР ДОЛГОГО ЗАЖАТИЯ
    def on_long_drag_timer_out(self):
        self.dragging = False
        self.is_window_dragging = True
        self.dragging = False
        self.eye_l.setVisible(False)
        self.eye_r.setVisible(False)
        self.cat.setPixmap(self.cat_dragged)
        self.lapa.setVisible(False)
        self.cat.setGeometry((self.cat_window_size - self.cat_dragged.width()), 0, self.cat_window_size,
                             self.cat_window_size)
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
            match self.cat_position:
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
            match self.cat_position:
                case (CatState.BOTTOM):
                    self.lapa_gif.stop()
                case (CatState.TOP):
                    self.top_lapa_gif.stop()
                case (CatState.LEFT):
                    self.left_lapa_gif.stop()
                case (CatState.RIGHT):
                    self.right_lapa_gif.stop()
            self.hide_lapa_animation.start()
            self.isLapaOut = False

    # СЛУШАТЕЛЬ МЫШИ
    def update_mouse_position(self, mouse_x, mouse_y):
        local_pos = self.mapFromGlobal(QPoint(mouse_x, mouse_y))

        # ЕСЛИ КУРСОР В ПРЕДЕЛАХ ТРИГГЕРНОЙ ЗОНЫ ЛАПЫ
        if self.lapa_react_zone.contains(local_pos):
            # ВЫБРАСЫВАЕМ ЛАПУ ТОЛЬКО ЕСЛИ ЕЕ НЕТ, КОТ НЕ ПЕРЕМЕЩАЕТСЯ И НЕ РАСТЯГИВАЕТСЯ
            if not self.isLapaOut and not self.is_window_dragging and not self.dragging:
                self.lapa.setVisible(True)
                self.throwLapa()
        else:
            if self.isLapaOut:
                self.hideLapa()

        self.move_cat_animation.setStartValue(self.pos())
        self.move_cat_animation.setEndValue(
            QPoint(mouse_x - int(self.cat_window_size / 2), mouse_y - int(self.cat_window_size / 3)))

        # ЕСЛИ КОТ ПЕРЕТАСКИВАЕТСЯ - ПЕРЕМЕЩАЕМ ЕГО
        if self.is_window_dragging:
            self.move(QPoint(mouse_x-int(self.cat.width()/2),mouse_y-int(self.cat.width()/3)))


        if not self.isFlying and not self.dragging and not self.is_window_dragging:
            # Преобразуем глобальные координаты мыши в координаты относительно окна
            mouse_pos = self.mapFromGlobal(QPoint(mouse_x, mouse_y))
            # Вычисляем расстояние от мыши до центра окна
            distance = math.sqrt((mouse_pos.x() - self.center_l.x()) ** 2 +
                                 (mouse_pos.y() - self.center_l.y()) ** 2)

            # ЕСЛИ МЫШЬ В ПРЕДЕЛАХ 250 пикселей
            if distance > self.eyes_distance and not self.small_eyes_timer.isActive():
                self.small_eyes_timer.start()

            if distance <= self.eyes_distance and not self.bigeyes_timer.isActive():
                self.bigeyes_timer.start()

            self.move_eye(self.eye_l, self.center_l, mouse_pos)
            self.move_eye(self.eye_r, self.center_r, mouse_pos)

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
        self.is_it_second_click = False
        QTimer.singleShot(self.cat_hiding_delay, lambda: self.cat_coming(position))

    # ПОЯВЛЕНИЕ КОТА ПОСЛЕ СКРЫТИЯ
    def cat_coming(self, position):
        self.cat_coming_animation.start(),
        self.start_fly() if self.enable_fly and position == CatState.BOTTOM and random.randint(1, 6)==1 else None,
        self.show()

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
                self.max_eyes_offset_x = 5  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
                self.max_eyes_offset_y = 10  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ
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
                self.max_eyes_offset_x = 5  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ГОРИЗОНТАЛИ
                self.max_eyes_offset_y = 10  # ДИАПАЗОН ДВИЖЕНИЯ ГЛАЗ ПО ВЕРТИКАЛИ
                self.cat_position = CatState.RIGHT

        return values

    # ФУНКЦИЯ СЛЕЖЕНИЯ ГЛАЗ ЗА МЫШЬЮ
    def move_eye(self, eye_label, center, mouse_pos):

        delta_x = mouse_pos.x() - center.x()
        delta_y = mouse_pos.y() - center.y()

        # Вычисляем процентное соотношение для смещения глаза
        percent_x = delta_x / (self.width() / 2)  # Процент по горизонтали
        percent_y = delta_y / (self.height() / 2)  # Процент по вертикали

        # Ограничиваем процентное соотношение в диапазоне [-1, 1]
        percent_x = max(-1, min(1, percent_x))
        percent_y = max(-1, min(1, percent_y))

        # Вычисляем новое положение глаза
        new_x = center.x() + percent_x * self.max_eyes_offset_x
        new_y = center.y() + percent_y * self.max_eyes_offset_y

        # Ограничиваем движение глаза в пределах области
        min_x = center.x() - self.max_eyes_offset_x  # Минимальное положение по X
        max_x = center.x() + self.max_eyes_offset_x  # Максимальное положение по X
        min_y = center.y() - self.max_eyes_offset_y  # Минимальное положение по Y
        max_y = center.y() + self.max_eyes_offset_y  # Максимальное положение по Y

        new_x = max(min_x, min(max_x, new_x))  # Ограничиваем new_x в пределах [min_x, max_x]
        new_y = max(min_y, min(max_y, new_y))  # Ограничиваем new_y в пределах [min_y, max_y]

        # Устанавливаем новое положение глаза
        new_pos = QPoint(int(new_x - eye_label.width() / 2), int(new_y - eye_label.height() / 2))

        # # Запускаем анимацию
        eye_label.move(new_pos)

    # СЛУШАТЕЛЬ НАЖАТИЙ КЛАВИАТУРЫ (ТОЛЬКО КОГДА КОТ В ФОКУСЕ)
    def keyPressEvent(self, event):
        if not self.enable_pacman and not self.is_first_cat_instance:
            return
        try:
            char = event.text().lower()
        except AttributeError:
            return
        # ДВА ВИДА СЛОВ, НА СЛУЧАЙ, ЕСЛИ РАСКЛАДКА ПЕРЕПУТАНА
        word = 'пакмен'
        second_word = 'gfrvty'

        if char == word[self.pointer] or char == second_word[self.pointer]:
            self.pointer += 1
        else:
            self.pointer = 0

        if self.pointer == 6:
            self.pacman = Pacman()
            self.pacman.show_and_start()
            self.pointer = 0

    # ВОЗВРАЩАЕТ ОКНО НАСТРОЕК
    @staticmethod
    def getSettingWindow(root_container, settings):
        return ApricotSettingsWindow(root_container, settings)
