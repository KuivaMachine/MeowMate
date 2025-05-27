import math
import random
import sys
from pathlib import Path

from PyQt6.QtCore import QPointF, pyqtSignal
from PyQt6.QtCore import QPropertyAnimation, Qt, QTimer, QEasingCurve, QVariantAnimation
from PyQt6.QtGui import QPainterPath
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel

from utils.enums import Direction


class Fly(QLabel):
    position_changed = pyqtSignal(int, int)
    finished = pyqtSignal()
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent.parent  # Найти родительский каталог проекта
        # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable' / 'fly'

    def __init__(self, cat_instance):
        super().__init__()

        # Настройка окна
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 0, QApplication.primaryScreen().geometry().width(),
                         QApplication.primaryScreen().geometry().height() - 50)
        self.start_position = self.init_start_position()
        self.last_position = self.start_position

        # Настройка QLabel с мухой
        self.fly = QLabel(self)
        self.fly.setPixmap(QPixmap(str(self.resource_path / "fly.png")))
        self.fly.setGeometry(int(self.start_position.x()), int(self.start_position.y()), 50, 50)
        self.setMouseTracking(True)
        self.fly.setMouseTracking(True)

        self.anim = QVariantAnimation()
        self.anim.setDuration(9000)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.anim.valueChanged.connect(self.update_pos)
        self.anim.finished.connect(self.cleanup)

        self.fly_move = QPropertyAnimation(self.fly, b"pos")
        self.fly_move.setDuration(20)
        self.cat = cat_instance
        self.path = QPainterPath()
        QTimer.singleShot(100, self.fly_path_init)  # Отложенная инициализация


    def init_start_position(self):
       return  QPointF(random.randint(0, 1980), -50)

    def update_pos(self, progress):
        point = self.path.pointAtPercent(progress)
        x, y = round(point.x()), round(point.y())
        self.fly.move(x, y)
        self.position_changed.emit(x, y)
        self.last_position = QPointF(self.fly.pos().x(), self.fly.pos().y())



    def fly_path_init(self):
        self.path = self.create_complex_path()

    def create_complex_path(self):
        path = QPainterPath()

        # Стартовая точка
        path.moveTo(self.init_start_position())

        for i in range(1, random.randint(6, 10)):
            radius = 50 * random.randint(3, 6)
            path.arcTo(700 - radius, 300 - radius,
                       2 * radius, 2 * radius,
                       0, random.randint(60, 300) * (i % 2 == 0 and 1 or -1))

        start_point = QPointF(200, 200)
        end_point = QPointF(self.cat.pos().x() + self.cat.cat_window_size,
                            self.cat.pos().y() - self.cat.cat_window_size / 4)
        width = abs(end_point.x() - start_point.x())
        height = abs(end_point.y() - start_point.y())

        control1 = QPointF(start_point.x() + width / 2, start_point.y() - height)
        control2 = QPointF(end_point.x() - width / 2, end_point.y() + height)
        path.cubicTo(control1, control2, end_point)

        if self.cat.pos().x()<QApplication.primaryScreen().geometry().width()/2:
            path.addPath(self.create_sine_wave_path( end_point, 60, 1500, 2, direction=Direction.POSITIVE))
        else:
            path.addPath(self.create_sine_wave_path(end_point, 60, 1500, 2, direction=Direction.NEGATIVE))
        return path

    def create_sine_wave_path(self,
                              start_point: QPointF,
                              amplitude: float,
                              wavelength: float,
                              num_oscillations: int,
                              step_pixels: int = 10,
                              direction: Direction = Direction.POSITIVE
                              ) -> QPainterPath:

        """
        Создает QPainterPath в виде синусоиды.

        :param direction: Направление синусоиды
        :param start_point: Начальная точка (QPointF)
        :param amplitude: Амплитуда (высота волны)
        :param wavelength: Длина волны (расстояние между пиками)
        :param num_oscillations: Количество полных колебаний
        :param step_pixels: Шаг аппроксимации (чем меньше, тем плавнее кривая)
        :return: QPainterPath, представляющий синусоиду
        """

        path = QPainterPath()
        path.moveTo(start_point)
        total_length = wavelength * num_oscillations
        x_start = start_point.x()
        y_start = start_point.y()

        for x in range(0, int(total_length), step_pixels):
            # Вычисляем y по формуле синуса: y = amplitude * sin(2πx / wavelength)
            relative_x = x / wavelength * (2 * math.pi)  # Переводим в радианы
            y_offset = amplitude * math.sin(relative_x)

            current_x = x_start + x
            current_y = y_start + y_offset

            match direction:
                case(Direction.POSITIVE):
                    path.lineTo(QPointF(current_x, current_y))
                case (Direction.NEGATIVE):
                    path.lineTo(QPointF(-current_x, current_y))

        return path





    def cleanup(self):
        self.finished.emit()
        self.hide()
        # self.deleteLater()