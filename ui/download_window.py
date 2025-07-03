from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar, QLabel, QVBoxLayout


class DownloadWindow(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint)

        self.setFixedSize(350, 110)
        self.move(parent.frameGeometry().center() - self.rect().center())
        self.setStyleSheet("""
         QLabel{
            color: #000000;
            border:2px solid #000000;
            border-radius:15px;
            background-color: #FFBC75;
}""")
        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(15,20,15,20)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 2px solid black;
                        border-radius: 10px;
                        background: #FFBC75;
                        height: 20px;
                    
                    }
                    QProgressBar::chunk {
                        background-color: #02C92D;
                        border-radius: 10px;
                    }
                """)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)


        self.title = QLabel("Загружаю всякое...")
        self.title.setStyleSheet("""
        QLabel{
            color: #000000;
            font-size: 20px;
            font-weight: light;
            font-family: 'PT Mono';
            border:none;
            
            }
        """)

        self.vbox.addWidget(self.progress_bar)
        self.vbox.addWidget(self.title)



    def update_value(self, value):
        self.progress_bar.setValue(value)
        # print(value)

    def finish_download(self):
        print("Все")