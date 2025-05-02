import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication

from ui.blink import Blinker
from ui.description_plus_buttons_window import DescriptionWindow
from ui.scroll_area import CharactersGallery
from ui.service_button import ServiceButton
from ui.switch_button import SwitchButton
from utils.enums import ThemeColor, CharactersList


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
    theme_color = ThemeColor.LIGHT
    theme_change_signal = pyqtSignal(ThemeColor)

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(800, 600)



        # ФОН ОКНА
        self.root_container = QWidget(self)

        self.root_container.setGeometry(0, 0, 800, 600)
        self.root_container.setObjectName('main_container')

        self.main_vbox = QVBoxLayout(self.root_container)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.main_vbox.setSpacing(0)

        # ЗАГОЛОВОК
        self.main_vbox.addWidget(self.setup_header())

        # ОСНОВНОЙ КОНТЕНТ
        self.main_vbox.addWidget(self.setup_content())

        # ФОНОВАЯ СЕТКА ДЛЯ DESCRIPTION
        self.right_shadow = QLabel(self.root_container)
        self.right_shadow_pixmap_light = QPixmap(str(self.resource_path / 'menu' / "right_shadow.png")).scaled(
            260, 380,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.right_shadow_pixmap_dark = QPixmap(str(self.resource_path / 'menu' / "right_shadow_white.png")).scaled(
            260, 380,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.right_shadow.setPixmap(self.right_shadow_pixmap_light)
        self.right_shadow.lower()
        QTimer.singleShot(50, self.update_bg_position)

        # ФОНОВАЯ СЕТКА ДЛЯ CHARACTERS
        self.left_shadow = QLabel(self.root_container)
        self.left_shadow_pixmap_light = QPixmap(str(self.resource_path / 'menu' / "left_shadow.png")).scaled(
            450, 485,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.left_shadow_pixmap_dark = QPixmap(str(self.resource_path / 'menu' / "left_shadow_white.png")).scaled(
            450, 485,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.left_shadow.setPixmap(self.left_shadow_pixmap_light)
        self.left_shadow.lower()
        QTimer.singleShot(50, self.update_bg_position)




        # Читаем и применяем стиль
        with open('dark-theme.qss', 'r') as f:
            self.dark_style = f.read()
        with open('light-theme.qss', 'r') as f:
            self.light_style = f.read()
        self.setStyleSheet(self.light_style)

    def on_start_button_push(self):
        print(self.characters_panel.selected_card.character_name)

    def on_settings_button_push(self):
        pass

    def update_bg_position(self):
        # УСТАНОВКА КООРДИНАТ ДЛЯ DESCRIPTION
        global_pos = self.description_panel.mapToGlobal(QPoint(0, 0))
        local_pos = self.root_container.mapFromGlobal(global_pos)
        self.right_shadow.setGeometry(local_pos.x() - 5, local_pos.y() + 10, 260, 345)
        # УСТАНОВКА КООРДИНАТ ДЛЯ CHARACTERS
        global_pos = self.characters_panel.mapToGlobal(QPoint(0, 0))
        local_pos = self.root_container.mapFromGlobal(global_pos)
        self.left_shadow.setGeometry(local_pos.x() - 5, local_pos.y() + 5, 450, 485)

    def change_theme(self, is_change):
        if is_change:
            self.theme_color = ThemeColor.DARK
            self.setStyleSheet(self.dark_style)
            self.close_btn.setupIcon(str(self.resource_path / 'menu' / "close_but_white.svg"))
            self.minimize_btn.setupIcon(str(self.resource_path / 'menu' / 'minimize_but_white.svg'))
            self.left_shadow.setPixmap(self.left_shadow_pixmap_dark)
            self.right_shadow.setPixmap(self.right_shadow_pixmap_dark)
        else:
            self.theme_color = ThemeColor.LIGHT
            self.setStyleSheet(self.light_style)
            self.close_btn.setupIcon(str(self.resource_path / 'menu' / "close_but.svg"))
            self.minimize_btn.setupIcon(str(self.resource_path / 'menu' / 'minimize_but.svg'))
            self.left_shadow.setPixmap(self.left_shadow_pixmap_light)
            self.right_shadow.setPixmap(self.right_shadow_pixmap_light)
        self.theme_change_signal.emit(self.theme_color)
        blink = Blinker(self.root_container)
        blink.show()
        QTimer.singleShot(300, blink.deleteLater)

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
        switch_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        switch_button = SwitchButton()
        switch_layout.addWidget(switch_button)
        switch_button.change_theme.connect(self.change_theme)
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

        self.close_btn = ServiceButton(
            str(self.resource_path / 'menu' / "close_but.svg" if self.theme_color == ThemeColor.LIGHT else "close_but_white.svg"))
        self.close_btn.clicked.connect(self.close)

        self.minimize_btn = ServiceButton(
            str(self.resource_path / 'menu' / "minimize_but.svg" if self.theme_color == ThemeColor.LIGHT else "minimize_but_white.svg"))
        self.minimize_btn.clicked.connect(self.showMinimized)

        buttons_container.addWidget(self.minimize_btn)
        buttons_container.addWidget(self.close_btn)
        hlayout.addWidget(buttons_widget)

        return header

    # ОСНОВНОЙ КОНТЕНТ
    def setup_content(self):
        content = QWidget()
        content.setContentsMargins(25, 25, 25, 25)

        content_layout = QHBoxLayout(content)
        content_layout.setSpacing(15)

        self.description_panel = DescriptionWindow(self, CharactersList.getFirst().value.name, CharactersList.getFirst().value.description)
        self.characters_panel = self.setup_gif_container()

        self.description_panel.start_button_clicked.connect(self.on_start_button_push)
        self.description_panel.settings_button_clicked.connect(self.on_settings_button_push)
        content_layout.addWidget(self.characters_panel, stretch=6)
        content_layout.addWidget(self.description_panel, stretch=4)

        return content

    def setup_gif_container(self):
        characters = CharactersGallery(self,list(CharactersList))
        characters.character_signal.connect(self.update_character_info)
        return characters

    def update_character_info(self, character_a):
        self.description_panel.update_info(character_a)

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
