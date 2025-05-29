import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush, QMovie, QPixmap
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QDialog, QToolBar, \
    QComboBox


class OkButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(60, 30)
        self.setObjectName('ok_button')
        self.setText('Ok')


class AlertWindow(QLabel):
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'menu'

    on_close = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.drag_position = None
        self.setObjectName('alert')
        self.parent_window = parent
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput)


        self.root_hbox = QHBoxLayout(self)
        self.root_hbox.setContentsMargins(20, 10, 20, 10)
        self.vbox = QVBoxLayout()

        toolbar = QToolBar()
        toolbar.setObjectName('toolbar_bongo')
        toolbar.setFixedSize(260,50)

        self.combo = QComboBox()
        self.combo.setObjectName('toolbar_bongo_combo')
        self.combo.addItems(["Классика", "Пианино", "Электрогитара","Бонго","Гитара"])
        toolbar.addWidget(self.combo)


        self.duck = QLabel()
        self.duck_gif = QMovie(str(self.resource_path / 'duck.gif'))
        self.duck_gif.setSpeed(120)
        self.duck_gif.setScaledSize(QSize(100, 80))
        self.duck.setMovie(self.duck_gif)
        self.duck_gif.setSpeed(120)
        self.duck_gif.start()

        self.ok = OkButton()
        self.ok.clicked.connect(self.on_close_window)

        self.vbox.addWidget(toolbar, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.ok, alignment=Qt.AlignmentFlag.AlignRight)


        self.root_hbox.addLayout(self.vbox)

        self.setGeometry((parent.size().width() - self.width())//3, (parent.size().height() - self.height())//8,
                         320, 460)

    def on_close_window(self):
        self.on_close.emit()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_position is not None:
                # Новая позиция окна относительно родительского виджета
                new_position = event.globalPos() - self.drag_position
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
