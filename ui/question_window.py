import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class Question (QWidget):

    app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'menu'
    def __init__(self, hint):
        super().__init__()
        self.setFixedSize(22,22)
        self.hint = hint
        self.question = QSvgWidget(self)
        self.question.load(str(self.resource_path / "question.svg"))

        self.hint_label = QWidget()
        self.label = QLabel(self.hint_label)
        self.label.setText(self.hint)
        self.hint_label.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.hint_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label.setStyleSheet("""
        QLabel{
            border:2px solid #692D00;
            border-radius:6px;
            color: #000000;
            background-color: #FFD8BA;
            font-size: 13px;
            font-weight: light;
            font-family: 'PT Mono';
            text-align: left;
            padding: 10px 6px;
}
        """)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.hint_label.setLayout(layout)

    def enterEvent(self, e):
        self.hint_label.adjustSize()
        pos = self.mapToGlobal(self.rect().topLeft())
        self.hint_label.move(pos.x() + (self.width() - self.hint_label.width()) // 2,
                             pos.y() - self.hint_label.height() - 5),
        self.hint_label.show()



    def leaveEvent(self, e):
        self.hint_label.hide()
