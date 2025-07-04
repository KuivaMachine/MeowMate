from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton


class QuestionWindow(QLabel):

    no_event  = pyqtSignal()
    yes_event  = pyqtSignal()
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(450, 200)
        self.move(parent.frameGeometry().center() - self.rect().center())
        self.setObjectName('question_window_root')
        self.vbox = QVBoxLayout(self)


        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(100)
        self.update_question = QLabel("Тут обновления подъехали))\nЗагрузим?")
        self.update_question.setObjectName('question')

        self.yes_btn = QPushButton("Давай")
        self.yes_btn.clicked.connect(self.yes_event.emit)
        self.yes_btn.setObjectName('yes_btn')

        self.no_btn = QPushButton("Потом")
        self.no_btn.clicked.connect(self.no_event.emit)
        self.no_btn.setObjectName('no_btn')

        self.hbox.addWidget(self.yes_btn)
        self.hbox.addWidget(self.no_btn)

        self.vbox.addWidget(self.update_question)
        self.vbox.addLayout(self.hbox)
