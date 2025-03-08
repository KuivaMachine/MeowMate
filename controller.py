import sys
import subprocess

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class CatController(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Управление котом")
        self.setGeometry(100, 100, 200, 100)

        layout = QVBoxLayout()

        # Кнопка "Активировать кота"
        self.activate_button = QPushButton("Активировать кота", self)
        self.activate_button.clicked.connect(self.activate_cat)
        layout.addWidget(self.activate_button)

        # Кнопка "Убрать кота"
        self.deactivate_button = QPushButton("Убрать кота", self)
        self.deactivate_button.clicked.connect(self.deactivate_cat)
        layout.addWidget(self.deactivate_button)

        self.setLayout(layout)

        # Переменная для хранения процесса
        self.cat_process = None

    def activate_cat(self):
        if self.cat_process is None:
            # Запуск фонового процесса
            self.cat_process = subprocess.Popen([sys.executable, "D:/py/cat2.py"])
            QMessageBox.information(self, "Информация", "Кот активирован!")
        else:
            QMessageBox.warning(self, "Ошибка", "Кот уже активирован!")

    def deactivate_cat(self):
        if self.cat_process is not None:
            # Завершение процесса
            self.cat_process.terminate()
            self.cat_process = None
            QMessageBox.information(self, "Информация", "Кот убран!")
        else:
            QMessageBox.warning(self, "Ошибка", "Кот не активирован!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = CatController()
    controller.show()
    sys.exit(app.exec_())