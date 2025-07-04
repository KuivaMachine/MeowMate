from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar, QLabel, QVBoxLayout


class DownloadWindow(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint)

        self.setFixedSize(450, 140)
        self.move(parent.frameGeometry().center() - self.rect().center())
        self.setObjectName('download_window_root')
        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(35,20,35,20)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName('download_progress_bar')
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)

        self.title = QLabel("Загружаю всякое...")
        self.title.setObjectName('download_title')

        self.vbox.addWidget(self.progress_bar)
        self.vbox.addWidget(self.title)


    def update_value(self, value):
        self.title.setText(f"Загружаю всякое...    {value}%")
        self.progress_bar.setValue(value)

    def finish_download(self):
        self.title.setText("Загрузил, устанавливаю...")