from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from pathlib import Path

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        movie = QMovie(str("C:/Users/olegz/Java/MeowMate/drawable/flork/flork_dance.gif)"))

        # Устанавливаем фильм в QLabel
        label = QLabel(self)
        label.setMovie(movie)
        movie.start()

        # Подписываемся на сигнал смены кадров
        movie.frameChanged.connect(self.check_frame_change)

        # Добавляем QLabel в окно
        self.setCentralWidget(label)
        self.setFixedSize(300, 300)
        self.show()

    def check_frame_change(self, frame_number):
        """
        Проверяет смену кадров и выводит сообщение, когда анимация закончена.
        """
        current_frame = frame_number
        previous_frame = getattr(self, "_previous_frame", None)

        # Сохраняем предыдущий кадр
        setattr(self, "_previous_frame", current_frame)

        # Если кадр больше не меняется, значит анимация завершилась
        if previous_frame == current_frame:
            print("Анимация закончилась!")

if __name__ == '__main__':
    app = QApplication([])
    ex = MyWindow()
    app.exec()

