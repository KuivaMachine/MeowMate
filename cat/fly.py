import math
import random

from PyQt6.QtCore import QPointF, pyqtSignal
from PyQt6.QtCore import QPropertyAnimation, Qt, QPoint, QTimer, QEasingCurve, QVariantAnimation
from PyQt6.QtGui import QPainterPath
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel


class Fly(QLabel):
    position_changed = pyqtSignal(int, int)
    def __init__(self, cat_instance):
        super().__init__()

        # Настройка окна
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
            # |Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 0, QApplication.primaryScreen().geometry().width(),
                         QApplication.primaryScreen().geometry().height() - 50)
        self.start_position = QPointF(random.randint(0, 1980), -50)
        # self.start_position = QPointF(200, 200)
        self.last_position = self.start_position

        # Настройка QLabel с мухой
        self.fly = QLabel(self)
        self.fly.setPixmap(QPixmap("./drawable/fly/fly.png"))
        self.fly.setGeometry(int(self.start_position.x()), int(self.start_position.y()), 50, 50)
        self.setMouseTracking(True)
        self.fly.setMouseTracking(True)



        self.anim = QVariantAnimation()
        self.anim.setDuration(9000)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.anim.valueChanged.connect(self.update_pos)
        self.anim.finished.connect(self.save_last_position)

        self.fly_move = QPropertyAnimation(self.fly, b"pos")
        self.fly_move.setDuration(20)

        self.isFlying = False
        self.cat = cat_instance
        self.path = QPainterPath()
        QTimer.singleShot(100, self.fly_path_init)  # Отложенная инициализация

    def update_pos(self, progress):
        point = self.path.pointAtPercent(progress)
        x, y = round(point.x()), round(point.y())
        self.fly.move(x, y)
        self.position_changed.emit(x, y)
        self.last_position = QPointF(self.fly.pos().x(), self.fly.pos().y())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(self.cat.pos())
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        event.accept()
        self.fly_move.setStartValue(self.fly.pos())
        self.fly_move.setEndValue(QPoint(event.pos().x(), event.pos().y()))
        # self.fly_move.start()

    def fly_path_init(self):
        self.path = self.create_complex_path()

    def create_complex_path(self):
        path = QPainterPath()

        # Стартовая точка
        path.moveTo(self.last_position)

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

        path.addPath(self.create_sine_wave_path(end_point, 60, 800, 3))

        return path

    def create_sine_wave_path(self,
                              start_point: QPointF,
                              amplitude: float,
                              wavelength: float,
                              num_oscillations: int,
                              step_pixels: int = 10
                              ) -> QPainterPath:

        """
        Создает QPainterPath в виде синусоиды.

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

            path.lineTo(QPointF(current_x, current_y))

        return path

    def save_last_position(self):
        self.last_position = QPointF(self.fly.pos().x(), self.fly.pos().y())
        self.path = self.create_complex_path()
        self.isFlying = False
        # self.anim.start()