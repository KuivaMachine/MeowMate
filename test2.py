from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtCore import Qt, QSize,QEvent
from PyQt6.QtGui import QPixmap, QTransform,QMovie, QColor, QPalette
from PyQt6.QtGui import QMovie, QPainter

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Настройки прозрачности
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        
        # 2. Сохраняем обработку событий мыши
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setMouseTracking(True)

       
       
       
       
        # 3. Пример содержимого (ваша лапа кота)
        self.main_cat = QPixmap("./cat/PET_t.png")
        self.cat = QLabel(self)
        self.cat.setGeometry(0, 0, 300, 300)
        self.cat.setPixmap(self.main_cat)
        self.cat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cat.setMouseTracking(True)

        
        # 4. Размеры окна
        self.setFixedSize(800, 600)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseMove:
            global_pos = event.globalPos()
            print(f"Global mouse: {global_pos.x()}, {global_pos.y()}")
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication([])
    window = TransparentWindow()
    window.show()
    app.exec()