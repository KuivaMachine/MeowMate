import os

from PyQt6.QtCore import QProcess
import ctypes
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bongo_process = None
        self.setup_ui()

    def setup_ui(self):
        self.start_btn = QPushButton("Запустить Bongo")
        self.start_btn.clicked.connect(self.toggle_bongo)

        layout = QVBoxLayout()
        layout.addWidget(self.start_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_bongo(self):
        if self.bongo_process:
            self.stop_bongo()
            self.start_btn.setText("Запустить Bongo")
        else:
            self.start_bongo()
            self.start_btn.setText("Остановить Bongo")

    def start_bongo(self):
        self.bongo_process = QProcess()

        # Для упакованного приложения
        if getattr(sys, '_MEIPASS', None):
            app_path = sys.executable
            path = ["--bongo"]
        else:
            app_path = sys.executable
            path = str(Path(__file__).parent / 'bongo'/'bongo.py')
            self.bongo_process.startDetached(app_path,[path])

    def stop_bongo(self):
        if self.bongo_process:
            print('ЗАКРЫВАЮ')
            self.bongo_process.terminate()
            # self.bongo_process.waitForFinished(1000)

    def closeEvent(self, event):
        self.stop_bongo()
        super().closeEvent(event)

if __name__=="__main__":
    app = QApplication(sys.argv)
    bongo = MainApp()
    bongo.show()
    sys.exit(app.exec())