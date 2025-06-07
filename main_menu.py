import ctypes
import json
import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton

from bongo.bongo import Bongo
from cat.apricot import Cat
from flork.flork import Flork
from ham.ham import Ham
from ui.blink import Blinker
from ui.description_plus_buttons_window import DescriptionWindow
from ui.developer_contacts_window import ContactWindow
from ui.portal import Portal
from ui.scroll_area import CharactersGallery
from ui.service_button import SvgButton
from ui.switch_button import SwitchButton
from utils.enums import ThemeColor, CharactersList


class MainMenuWindow(QMainWindow):
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent
    resource_path = app_directory / 'drawable'

    theme_color = ThemeColor.LIGHT
    theme_change_signal = pyqtSignal(ThemeColor)

    def get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return Path(base_path) / relative_path

    def __init__(self):
        super().__init__()
        self.is_contacts_showing = None
        self.drag_pos = None
        self.is_setting_showing = False
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(800, 600)
        # self.load_fonts()
        with open(self.get_resource_path('settings/theme_mode.json'), "r", encoding='utf-8') as f:
            theme = json.load(f)

        if theme['mode'] == 'dark':
            is_dark_theme = True
        else:
            is_dark_theme = False

        # ФОН ОКНА
        self.root_container = QWidget(self)

        self.root_container.setGeometry(0, 0, 800, 600)
        self.root_container.setObjectName('main_container')

        self.main_vbox = QVBoxLayout(self.root_container)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)

        # ЗАГОЛОВОК
        self.main_vbox.addWidget(self.setup_header(is_dark_theme))

        # ОСНОВНОЙ КОНТЕНТ
        self.main_vbox.addWidget(self.setup_content())

        # ФОНОВАЯ СЕТКА ДЛЯ DESCRIPTION
        self.right_shadow = QSvgWidget(self.root_container)
        self.right_shadow_pixmap_light = str(self.resource_path / 'menu' / "right_shadow.svg")
        self.right_shadow_pixmap_dark = str(self.resource_path / 'menu' / "right_shadow_white.svg")

        self.right_shadow.load(self.right_shadow_pixmap_light)
        self.right_shadow.lower()

        # ФОНОВАЯ СЕТКА ДЛЯ CHARACTERS
        self.left_shadow = QSvgWidget(self.root_container)
        self.left_shadow_pixmap_light = str(self.resource_path / 'menu' / "left_shadow.svg")
        self.left_shadow_pixmap_dark = str(self.resource_path / 'menu' / "left_shadow_white.svg")

        self.left_shadow.load(self.left_shadow_pixmap_light)
        self.left_shadow.lower()
        QTimer.singleShot(50, self.update_bg_position)

        # КНОПКА КОНТАКТОВ
        self.contacts = QPushButton('Контакты', self.root_container)
        self.contacts.setGeometry(710,560,70,30)
        self.contacts.setObjectName('contacts_btn')
        self.contacts.clicked.connect(self.show_contacts)


        # СПИСОК АКТИВНЫХ ПЕРСОНАЖЕЙ
        self.windows = []

        # Читаем и применяем стиль
        with open(self.get_resource_path('resources/dark-theme.qss'), 'r') as f:
            self.dark_style = f.read()
        with open(self.get_resource_path('resources/light-theme.qss'), 'r') as f:
            self.light_style = f.read()

        self.change_theme(is_dark_theme)

    def show_contacts(self):
        if not self.is_contacts_showing:
            self.contacts_window = ContactWindow(self)
            self.contacts_window.show()
            self.is_contacts_showing = True

    def load_fonts(self):
        font_db = QFontDatabase()
        fonts = [
            "resources/fonts/JetBrainsMono-Bold.ttf",
            "resources/fonts/JetBrainsMono-Light.ttf",
            "resources/fonts/JetBrainsMono-Regular.ttf",
            "resources/fonts/PTMono.ttf"
        ]
        for font_file in fonts:
            font_path = self.get_resource_path(font_file)
            print(font_path)
            font_db.addApplicationFont(str(font_path))


    def load_settings(self, path):
        try:
            with open(path, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл настроек не найден или поврежден")
            return None

    # КНОПКА "ЗАПУСТИТЬ"
    def on_start_button_push(self):
        selected_character = None

        match self.characters_panel.selected_card.character_name:
            case 'БОНГО-КОТ':
                settings = self.load_settings(self.get_resource_path("settings/bongo_settings.json"))
                selected_character = Bongo(settings)
            case 'ФЛОРК':
                settings = self.load_settings(self.get_resource_path("settings/flork_settings.json"))
                selected_character = Flork(settings)
            case 'АБРИКОС':
                settings = self.load_settings(self.get_resource_path("settings/apricot_settings.json"))
                selected_character = Cat(settings)
            case 'ЛЕНУСИК':
                settings = self.load_settings(self.get_resource_path("settings/ham_settings.json"))
                selected_character = Ham(settings)

        self.windows.append(selected_character)
        portal_destination = QPoint(selected_character.pos().x() + (selected_character.width() - 360) // 2,
                                    selected_character.pos().y() + (selected_character.height() - 400) // 2)
        self.portal = Portal(portal_destination)
        QTimer.singleShot(2000, selected_character.show)
        self.portal.show()

        if self.is_setting_showing:
            self.settings_window.close()

    # КНОПКА "НАСТРОИТЬ"
    def on_settings_button_push(self):
        if not self.is_setting_showing:
            self.is_setting_showing = True
            self.settings_window = None
            match self.characters_panel.selected_card.character_name:
                case 'БОНГО-КОТ':
                    settings = self.load_settings(self.get_resource_path("settings/bongo_settings.json"))
                    self.settings_window = Bongo.getSettingWindow(self.root_container, settings)
                case 'ФЛОРК':
                    settings = self.load_settings(self.get_resource_path("settings/flork_settings.json"))
                    self.settings_window = Flork.getSettingWindow(self.root_container, settings)
                case 'АБРИКОС':
                    settings = self.load_settings(self.get_resource_path("settings/apricot_settings.json"))
                    self.settings_window = Cat.getSettingWindow(self.root_container, settings)
                case 'ЛЕНУСИК':
                    settings = self.load_settings(self.get_resource_path("settings/ham_settings.json"))
                    self.settings_window = Ham.getSettingWindow(self.root_container, settings)

            self.settings_window.on_close.connect(self.update_settings)
            self.settings_window.show()

    def update_settings(self):
        self.is_setting_showing = False

    def update_bg_position(self):
        # УСТАНОВКА КООРДИНАТ ДЛЯ DESCRIPTION
        global_pos = self.description_panel.mapToGlobal(QPoint(0, 0))
        local_pos = self.root_container.mapFromGlobal(global_pos)
        self.right_shadow.setGeometry(local_pos.x() - 5, local_pos.y() + 5, 260, 345)
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
            self.left_shadow.load(self.left_shadow_pixmap_dark)
            self.right_shadow.load(self.right_shadow_pixmap_dark)
            settings = {
                "mode": 'dark',
            }
        else:
            self.theme_color = ThemeColor.LIGHT
            self.setStyleSheet(self.light_style)
            self.close_btn.setupIcon(str(self.resource_path / 'menu' / "close_but.svg"))
            self.minimize_btn.setupIcon(str(self.resource_path / 'menu' / 'minimize_but.svg'))
            self.left_shadow.load(self.left_shadow_pixmap_light)
            self.right_shadow.load(self.right_shadow_pixmap_light)
            settings = {
                "mode": 'light',
            }
        self.theme_change_signal.emit(self.theme_color)
        # БЛИК СВЕТА ПРИ СМЕНЕ ТЕМЫ
        blink = Blinker(self.root_container)
        blink.show()
        QTimer.singleShot(300, blink.deleteLater)

        with open(self.get_resource_path("settings/theme_mode.json"), "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)

    # ЗАГОЛОВОК
    def setup_header(self, is_light_theme):
        header = QWidget()
        header.setObjectName('header')
        header.setFixedHeight(55)

        hlayout = QHBoxLayout(header)
        hlayout.setContentsMargins(20, 0, 3, 0)

        # ПЕРЕКЛЮЧАТЕЛЬ ТЕМЫ
        switch_container = QWidget()
        switch_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        switch_layout = QHBoxLayout(switch_container)
        switch_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        switch_button = SwitchButton(is_light_theme)
        switch_layout.addWidget(switch_button)
        switch_button.change_theme.connect(self.change_theme)
        hlayout.addWidget(switch_container)

        # ВЫБЕРИТЕ ПЕРСОНАЖА
        title = QLabel("Выберите персонажа")
        title.setObjectName('title')
        title.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        hlayout.addWidget(title)

        # КНОПКИ СВЕРНУТЬ/ЗАКРЫТЬ
        buttons_widget = QWidget()
        buttons_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        buttons_container = QHBoxLayout(buttons_widget)
        buttons_container.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_container.setSpacing(10)

        self.close_btn = SvgButton(
            str(self.resource_path / 'menu' / "close_but.svg" if self.theme_color == ThemeColor.LIGHT else "close_but_white.svg"))
        self.close_btn.clicked.connect(self.close)

        self.minimize_btn = SvgButton(
            str(self.resource_path / 'menu' / "minimize_but.svg" if self.theme_color == ThemeColor.LIGHT else "minimize_but_white.svg"))
        self.minimize_btn.clicked.connect(self.showMinimized)

        buttons_container.addWidget(self.minimize_btn)
        buttons_container.addWidget(self.close_btn)
        hlayout.addWidget(buttons_widget)

        return header

    # ОСНОВНОЙ КОНТЕНТ
    def setup_content(self):
        content = QWidget()
        content.setContentsMargins(25, 10, 25, 10)
        content_layout = QHBoxLayout(content)
        content_layout.setSpacing(15)

        self.description_panel = DescriptionWindow(self, CharactersList.getFirst().value.name,
                                                   CharactersList.getFirst().value.description)
        self.characters_panel = self.setup_gif_container()
        self.description_panel.start_button_clicked.connect(self.on_start_button_push)
        self.description_panel.settings_button_clicked.connect(self.on_settings_button_push)
        content_layout.addWidget(self.characters_panel, alignment=Qt.AlignTop)
        content_layout.addWidget(self.description_panel, alignment=Qt.AlignTop)

        return content

    def setup_gif_container(self):
        characters = CharactersGallery(self, list(CharactersList))
        characters.character_signal.connect(self.update_character_info)
        return characters

    def update_character_info(self, character_a):
        self.description_panel.update_info(character_a)

    # Обработчики событий для перемещения окна
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 40:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_pos') and self.drag_pos is not None:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenuWindow()
    window.show()
    app.exec()
