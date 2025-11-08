from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton


class InstructionWindow(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setGeometry((parent.size().width() - self.width()) // 4, (parent.size().height() - self.height()) // 5,
                        450, 400)

        self.setObjectName('question_window_root')
        self.vbox = QVBoxLayout(self)

        self.info = QLabel("1. Чтобы закрыть персонажа, нажмите на него правой кнопкой мыши - \"ЗАКРЫТЬ\"\n2. Чтобы закрыть приложение вместе со всеми персонажами - откройте панель трея в правом нижнем углу панели задач")
        self.info.setObjectName('question')
        self.info.setWordWrap(True)


        self.ok_btn = QPushButton("Понял")
        self.ok_btn.setObjectName('yes_btn')
        self.ok_btn.clicked.connect(self.close)

        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.ok_btn)