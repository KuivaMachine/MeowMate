import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush, QMovie
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton


class OkButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(60, 30)
        self.setObjectName('ok_button')
        self.setText('Ok')

class AlertWindow(QLabel):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent.parent  # Найти родительский каталог проекта
    # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable' / 'menu'

    def __init__(self,parent,scale_factor):
        super().__init__(parent)
        self.setObjectName('alert')
        self.parent_window = parent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint|Qt.WindowType.WindowTransparentForInput)
        self.root_hbox = QHBoxLayout(self)

        self.root_hbox.setContentsMargins(20,10,20,10)
        self.text = QLabel(f'Для корректного отображения \nперсонажей требуется масштаб \nэкрана 100% \nВаш масштаб - {scale_factor}%')
        self.text.setObjectName('alert_text')

        self.text.setWordWrap(True)
        self.vbox = QVBoxLayout()

        self.duck = QLabel()
        self.duck_gif = QMovie(str(self.resource_path / 'duck.gif'))
        self.duck_gif.setSpeed(120)
        self.duck_gif.setScaledSize(QSize(100, 80))
        self.duck.setMovie(self.duck_gif)
        self.duck_gif.setSpeed(120)
        self.duck_gif.start()


        self.ok = OkButton()
        self.ok.clicked.connect(self.close)
        self.vbox.addWidget(self.duck, alignment=Qt.AlignmentFlag.AlignCenter, stretch=8)
        self.vbox.addWidget(self.ok, alignment=Qt.AlignmentFlag.AlignRight, stretch=2)

        self.root_hbox.addWidget(self.text)
        self.root_hbox.addLayout(self.vbox)

        self.setGeometry((parent.size().width() - self.width()) // 6, (parent.size().height() - self.height()) // 3,
                         550, 150)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_position is not None:
                # Новая позиция окна относительно родительского виджета
                new_position = event.globalPosition().toPoint() - self.drag_position
                parent_geometry = self.parent().frameGeometry()
                window_size = self.geometry()

                # Ограничиваем перемещение окна внутри родительского виджета
                x = max(0, min(new_position.x(), parent_geometry.width() - window_size.width()))
                y = max(0, min(new_position.y(), parent_geometry.height() - window_size.height()))

                # Перемещаем окно
                self.move(x, y)
                event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()