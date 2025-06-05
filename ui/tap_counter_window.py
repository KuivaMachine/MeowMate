from PyQt5.QtWidgets import QLabel


class Counter(QLabel):
    def __init__(self, count, parent):
        super().__init__(parent)

        self.setStyleSheet("""QLabel {
    color: #FF7A81;
    font-size: 16px;
    text-align: center;
    font-weight: light;
    font-family: 'JetBrains Mono';
}
}""")

        self.setText(str(count))
        self.move(250,100)


