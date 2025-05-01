import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QSize, QPoint, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, \
    QStackedLayout

from character import Character
from test import SwitchButton
from ui.description_plus_buttons_window import DescriptionWindow
from ui.scroll_area import CharactersGallery
from ui.service_button import ServiceButton

from utils.enums import Characters



class MainMenuWindow(QMainWindow):
    # Определяем путь к каталогу с данными в зависимости от режима исполнения
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        # Мы находимся в упакованном виде (PyInstaller)
        app_directory = Path(base_path)
    else:
        # Обычный режим разработки
        app_directory = Path(__file__).parent  # Найти родительский каталог проекта

    # Теперь можем обратиться к нужным ресурсам
    resource_path = app_directory / 'drawable'

    def __init__(self):
        super().__init__()
        self.drag_pos = None
        # Убираем стандартные рамки окна
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        with open('light-theme.qss', 'r') as f:
            self.style_sheet = f.read()
        self.setStyleSheet(self.style_sheet)

        # Основные параметры окна
        self.setFixedSize(800, 600)

        # Создаем основной контейнер
        self.main_container = QWidget(self)
        self.main_container.setGeometry(0, 0, 800, 600)
        self.main_container.setObjectName('main_container')

        self.main_vbox = QVBoxLayout(self.main_container)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.main_vbox.setSpacing(0)  # Убираем промежутки между элементами

        # ЗАГОЛОВОК
        self.main_vbox.addWidget(self.setup_header())

        # ОСНОВНОЙ КОНТЕНТ
        self.main_vbox.addWidget(self.setup_content())

        # ФОНОВАЯ СЕТКА ДЛЯ DESCRIPTION
        self.right_shadow = QLabel(self.main_container)
        self.right_shadow.setStyleSheet("QLabel { background: transparent; border: none; }")
        self.right_shadow.setPixmap(QPixmap(str(self.resource_path / 'menu' / "right_shadow.png")).scaled(
            260, 380,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.right_shadow.lower()
        QTimer.singleShot(50, self.update_bg_position)

        # ФОНОВАЯ СЕТКА ДЛЯ CHARACTERS
        self.left_shadow = QLabel(self.main_container)
        self.left_shadow.setStyleSheet("QLabel { background: transparent; border: none; }")
        self.left_shadow.setPixmap(QPixmap(str(self.resource_path / 'menu' / "left_shadow.png")).scaled(
            450, 485,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.left_shadow.lower()
        QTimer.singleShot(50, self.update_bg_position)

        # Читаем и применяем стиль
        with open('light-theme.qss', 'r') as f:
            style_sheet = f.read()
        self.setStyleSheet(style_sheet)

    def on_start_button_push(self):
        print(self.left_panel.selected_card.character)

    def on_settings_button_push(self):
        print(self.left_panel.selected_card.character)

    def update_bg_position(self):
        # УСТАНОВКА КООРДИНАТ ДЛЯ DESCRIPTION
        global_pos = self.right_panel.mapToGlobal(QPoint(0, 0))
        local_pos = self.main_container.mapFromGlobal(global_pos)
        self.right_shadow.setGeometry(local_pos.x() - 5, local_pos.y() + 10, 260, 345)
        # УСТАНОВКА КООРДИНАТ ДЛЯ CHARACTERS
        global_pos = self.left_panel.mapToGlobal(QPoint(0, 0))
        local_pos = self.main_container.mapFromGlobal(global_pos)
        self.left_shadow.setGeometry(local_pos.x() - 5, local_pos.y() + 5, 450, 485)

    def change_theme(self):
        print('change')


    # ЗАГОЛОВОК
    def setup_header(self):
        header = QWidget()
        header.setObjectName('header')
        header.setFixedHeight(45)


        hlayout = QHBoxLayout(header)
        hlayout.setSpacing(10)
        hlayout.setContentsMargins(20, 0, 15, 0)

        # ПЕРЕКЛЮЧАТЕЛЬ ТЕМЫ
        switch_container = QWidget()
        switch_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        switch_layout = QHBoxLayout(switch_container)
        switch_button = SwitchButton()
        switch_button.clicked.connect(self.change_theme)
        switch_layout.addWidget(switch_button)
        switch_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayout.addWidget(switch_container)

        # ВЫБЕРИТЕ ПЕРСОНАЖА
        title = QLabel("Выберите персонажа")
        title.setObjectName('title')
        title.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hlayout.addWidget(title)

        # КНОПКИ СВЕРНУТЬ/ЗАКРЫТЬ
        buttons_widget = QWidget()
        buttons_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        buttons_container = QHBoxLayout(buttons_widget)
        buttons_container.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_container.setSpacing(10)

        close_btn = ServiceButton(str(self.resource_path / 'menu' / "close_but.svg"))
        close_btn.clicked.connect(self.close)

        minimize_btn = ServiceButton(str(self.resource_path / 'menu' / "minimize_but.svg"))
        minimize_btn.clicked.connect(self.showMinimized)

        buttons_container.addWidget(minimize_btn)
        buttons_container.addWidget(close_btn)
        hlayout.addWidget(buttons_widget)

        return header

    # ОСНОВНОЙ КОНТЕНТ
    def setup_content(self):
        content = QWidget()
        content.setContentsMargins(25, 25, 25, 25)

        content_layout = QHBoxLayout(content)
        content_layout.setSpacing(15)

        self.right_panel = DescriptionWindow(self, "","")
        self.left_panel = self.setup_gif_container()

        self.right_panel.start_button_clicked.connect(self.on_start_button_push)
        self.right_panel.settings_button_clicked.connect(self.on_settings_button_push)
        content_layout.addWidget(self.left_panel, stretch=6)
        content_layout.addWidget(self.right_panel, stretch=4)

        return content




    def setup_gif_container(self):

        characters = CharactersGallery(
            [
            Character(Characters.FLORK, str(self.resource_path / 'flork' / 'flork_dance.gif'), QSize(160, 160), 100),
             Character(Characters.CAT, str(self.resource_path / 'cat' / 'cat_preview.gif'), QSize(170, 170), 130),Character(Characters.FLORK, str(self.resource_path / 'flork' / 'flork_dance.gif'), QSize(160, 160), 100),
             Character(Characters.CAT, str(self.resource_path / 'cat' / 'cat_preview.gif'), QSize(170, 170), 130),Character(Characters.FLORK, str(self.resource_path / 'flork' / 'flork_dance.gif'), QSize(160, 160), 100),
             Character(Characters.CAT, str(self.resource_path / 'cat' / 'cat_preview.gif'), QSize(170, 170), 130)
             ])
        characters.character_signal.connect(self.update_character_info)
        return characters

    def update_character_info(self, character):
        self.right_panel.update_info(character)

    # Обработчики событий для перемещения окна
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.pos().y() < 40:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenuWindow()
    window.show()

    app.exec()
