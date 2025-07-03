from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton


class QuestionWindow(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(350, 110)
        self.move(parent.frameGeometry().center() - self.rect().center())

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(0,0,0,0)

        self.hbox = QHBoxLayout()

        self.update_question = QLabel("Тут обновления подъехали))\nЗагрузим? 😎")
        self.update_question.setStyleSheet("""
        QLabel{
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            font-family: 'PT Mono';
            color: #000000;
            border: 2px solid #000000;
            border-radius:15px;
            background-color: #FFBC75;
}""")
        self.yes_btn = QPushButton("Давай ☺️")
        self.yes_btn.setStyleSheet("""
        QPushButton{
            font-size: 20px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
            color: #000000;
            border:3px solid #000000;
            background-color:#FFBC75;
            border-radius: 8px;
            padding: 8px;
        }
        QPushButton:hover{
            background-color: #B3B3B3
        }
        QPushButton:pressed{
            background-color: #666666
        }""")