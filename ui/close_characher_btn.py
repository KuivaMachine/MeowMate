from PyQt5.QtWidgets import QPushButton


class CloseButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(100, 30)
        self.setStyleSheet("""QPushButton {
    color: black;
    font-size: 15px;
    font-weight: bold;
    font-family: 'JetBrains Mono';
    background-color: #FFE5BD;
    border: 2px solid black;
    border-radius:5px;
}
QPushButton:pressed {
    color: black;
    font-size: 15px;
    font-weight: bold;
    font-family: 'JetBrains Mono';
    background-color: #A89271;
    border: 2px solid black;
    border-radius:5px;
}""")
        self.setText('закрыть')
