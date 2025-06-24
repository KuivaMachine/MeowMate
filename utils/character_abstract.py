from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

from ui.close_characher_btn import CloseButton


class Character (QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag_pos = None
        self.close_button = None
        self.is_close_btn_showing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPos()
            self.close_button.close()
            self.is_close_btn_showing = False

        if event.button() == Qt.MouseButton.RightButton:
            if not self.is_close_btn_showing:
                self.close_button = CloseButton(self)

                # Размеры кнопки
                btn_width = self.close_button.width()
                btn_height = self.close_button.height()

                # Получаем позицию курсора относительно виджета
                local_pos = event.pos()

                # Корректируем позицию, чтобы кнопка не выходила за границы
                x = local_pos.x() - btn_width // 2  # Центрируем по горизонтали
                y = local_pos.y() - btn_height - 5  # Смещаем выше курсора

                # Ограничиваем по правому краю
                if x + btn_width > self.width():
                    x = self.width() - btn_width

                # Ограничиваем по нижнему краю
                if y + btn_height > self.height():
                    y = self.height() - btn_height

                # Ограничиваем по левому и верхнему краям
                x = max(0, x)
                y = max(0, y)

                self.close_button.setGeometry(x, y, btn_width, btn_height)
                self.close_button.clicked.connect(self.close)
                self.close_button.show()
                self.is_close_btn_showing = True
            else:
                self.close_button.close()
                self.is_close_btn_showing = False

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_pos:
                # Вычисляем новую позицию
                new_pos = self.pos() + event.globalPos() - self.drag_pos

                # Получаем геометрию родительского окна
                parent_rect = QApplication.primaryScreen().geometry()

                left_maximum = parent_rect.left() - 100
                right_maximum = parent_rect.right() - 300
                top_maximum = parent_rect.top() - 140
                bottom_maximum = parent_rect.bottom() - 240

                # Ограничиваем перемещение
                x = max(left_maximum,
                        min(new_pos.x(),
                            right_maximum))

                y = max(top_maximum,
                        min(new_pos.y(),
                            bottom_maximum))

                # Перемещаем виджет
                self.move(x, y)
                self.drag_pos = event.globalPos()
                event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None