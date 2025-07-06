import json
import os
import sys
import time
import winreg
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, \
    QMessageBox

from bongo.bongo import Bongo
from cat.apricot import Cat
from flork.flork import Flork
from ham.ham import Ham
from ui.blink import Blinker
from ui.description_plus_buttons_window import DescriptionWindow
from ui.developer_contacts_window import ContactWindow
from ui.download_window import DownloadWindow
from ui.portal import Portal
from ui.question_for_update_window import QuestionWindow
from ui.scroll_area import CharactersGallery
from ui.service_button import SvgButton
from ui.switch_button import SwitchButton
from ui.updates_info_window import UpdateInfoWindow
from utils.update_script import UpdatesChecker, UpdatesDownloader, UpdatesInstaller
from utils.enums import ThemeColor, CharactersList


# ИЩЕМ ФЛАГ ПЕРВОГО ЗАПУСКА ДЛЯ ОТОБРАЖЕНИЯ ОКНА ИЗМЕНЕНИЙ
def check_is_first_run():
    # Путь к ключу в реестре
    reg_path = r"Software\KuivaMachine\MeowMate"
    key_name = "is_first_run"

    try:
        # Открываем ключ для чтения (HKEY_CURRENT_USER)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ) as key:
            value, reg_type = winreg.QueryValueEx(key, key_name)
            if value == b'\x01':
                print("Первый запуск")
                # Переоткрываем ключ для записи
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as w_key:
                    winreg.SetValueEx(w_key, key_name, 0, winreg.REG_BINARY, b'\x00')  # Записываем 0 (байты)
                return True
            else:
                print("Не первый запуск")
                return False
    except FileNotFoundError:
        print("Ключ реестра не найден!")
        return True


# ЧИТАЕМ НАСТРОЙКИ ИЗ ПАПКИ APPDATA И СОЗДАЕМ, ЕСЛИ ИХ НЕТ
def check_settings():
    appdata_dir = Path(os.getenv('APPDATA')) / "MeowMate/settings"
    appdata_dir.mkdir(parents=True, exist_ok=True)

    # Дефолтные настройки для каждого файла
    default_files = {
        "theme_mode.json": {"mode": "light"},
        "apricot_settings.json": {"pacman": True, "fly": True, "cat_hiding_delay": "0"},
        "bongo_settings.json": {"tap_counter": False, "bongo_type": "Классика", "count": 0},
        "flork_settings.json": {"size": 200},
        "ham_settings.json": {"size": 150, "hiding": True}
    }

    # Проверяем и создаем каждый файл
    for filename, default_content in default_files.items():
        file_path = appdata_dir / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, indent=4)


# ВОЗВРАЩАЕТ АБСОЛЮТНЫЙ ПУТЬ
def get_resource_path(relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return Path(base_path) / relative_path


# ВОЗВРАЩАЕТ НАСТРОЙКИ ИЗ APPDATA
def load_settings(path):
    appdata = os.getenv('APPDATA')
    app_dir = Path(appdata) / "MeowMate" / path
    try:
        with open(app_dir, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Файл настроек не найден или поврежден")
        return None


# ЗАГРУЖАЕТ ШРИФТЫ В ЛОКАЛЬНУЮ БАЗУ
def load_fonts():
    font_db = QFontDatabase()
    fonts = [
        "resources/fonts/JetBrainsMono-Bold.ttf",
        "resources/fonts/JetBrainsMono-Light.ttf",
        "resources/fonts/JetBrainsMono-Regular.ttf",
        "resources/fonts/PTMono.ttf"
    ]
    for font_file in fonts:
        font_path = get_resource_path(font_file)
        font_db.addApplicationFont(str(font_path))


class MainMenuWindow(QMainWindow):
    resource_path = Path(__file__).parent / 'drawable'  # ПУТЬ К ПАПКЕ С РЕСУРСАМИ
    theme_color = ThemeColor.LIGHT  # ТЕМА ПО УМОЛЧАНИЮ СВЕТЛАЯ
    theme_change_signal = pyqtSignal(ThemeColor)  # СИГНАЛ О СМЕНЕ ТЕМЫ
    new_version = '1.0.8' # НОМЕР ТЕКУЩЕЙ ВЕРСИИ
    whats_new_text = """ 
- Исправлены баги.
- Улучшена графика.
- Добавлена поддержка обновлений.
    """                     # ИНФОРМАЦИЯ ОБ ОБНОВЛЕНИИ

    def __init__(self):
        super().__init__()

        self.download_window = None
        self.BONGO_CAT_MAX_COUNT = 15  # МАКСИМАЛЬНОЕ ЧИСЛО ПЕРСОНАЖЕЙ: БОНГО-КОТ
        self.FLORK_CAT_MAX_COUNT = 15  # МАКСИМАЛЬНОЕ ЧИСЛО ПЕРСОНАЖЕЙ: ФЛОРК
        self.APRICOT_CAT_MAX_COUNT = 8  # МАКСИМАЛЬНОЕ ЧИСЛО ПЕРСОНАЖЕЙ: АБРИКОС
        self.CHAM_CAT_MAX_COUNT = 8  # МАКСИМАЛЬНОЕ ЧИСЛО ПЕРСОНАЖЕЙ: ЛЕНУСИК
        self.is_contacts_showing = False  # ПОКАЗЫВАЕТСЯ ЛИ ОКНО КОНТАКТОВ
        self.drag_pos = None  # НАЧАЛЬНАЯ ПОЗИЦИЯ ОКНА В МОМЕНТ НАЖАТИЯ ПЕРЕД ПЕРЕТАСКИВАНИЕМ
        self.is_setting_showing = False  # ПОКАЗЫВАЕТСЯ ЛИ ОКНО НАСТРОЕК
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # БЕЗ ГРАНИЦ
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # БЕЗ ФОНА
        self.setFixedSize(800, 600)

        # ЗАГРУЖАЕТ ШРИФТЫ В ЛОКАЛЬНУЮ БАЗУ
        load_fonts()

        # ЗАГРУЖАЕТ ТЕМУ
        theme = load_settings('settings/theme_mode.json')
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
        self.contacts.setGeometry(710, 560, 70, 30)
        self.contacts.setObjectName('contacts_btn')
        self.contacts.clicked.connect(self.show_contacts)

        # ВЕРСИЯ
        self.version_label = QLabel(f'v{self.new_version}', self.root_container)
        self.version_label.setGeometry(10, 568, 170, 30)
        self.version_label.setObjectName('version_label')

        # СПИСОК АКТИВНЫХ ПЕРСОНАЖЕЙ
        self.windows = []

        # ЧИТАЕТ И ПРИМЕНЯЕТ СВЕТЛЫЙ И ТЕМНЫЙ СТИЛИ ДЛЯ ВИДЖЕТОВ
        with open(get_resource_path('resources/dark-theme.qss'), 'r') as f:
            self.dark_style = f.read()
        with open(get_resource_path('resources/light-theme.qss'), 'r') as f:
            self.light_style = f.read()
        self.change_theme(is_dark_theme)

        if check_is_first_run():
            self.show_updates_info()
            self.is_first_run = True

        self.setup_update_checker(self.is_first_run)



    def setup_update_checker(self,is_first_run):
        self.update_checker_thread = UpdatesChecker(is_first_run)
        self.update_checker_thread.update_available.connect(self.show_update_dialog)
        self.update_checker_thread.start()

    def show_update_dialog(self, download_url):
        self.update_checker_thread.quit()
        self.update_checker_thread.wait()
        self.question_box = QuestionWindow(self.root_container)
        self.question_box.yes_event.connect(lambda: (
            self.question_box.close(),
            self.downloading_updates(download_url)))
        self.question_box.no_event.connect(self.question_box.close)
        self.question_box.show()

    def downloading_updates(self, download_url):
        self.download_window = DownloadWindow(self.root_container)
        self.download_window.show()

        self.download_thread = UpdatesDownloader(self, download_url)
        self.download_thread.progress_updated.connect(self.download_window.update_value)
        self.download_thread.download_finished.connect(self.start_install_updates)
        self.download_thread.start()

    def start_install_updates(self, update_file):
        self.download_window.close(),
        self.download_thread.quit(),
        self.download_thread.wait(),
        self.download_window.finish_download()

        self.updates_installer_thread = UpdatesInstaller(update_file)
        self.updates_installer_thread.install_finished.connect(self.close_application)
        self.updates_installer_thread.start()

    def close_application(self):
        if self.windows:
            for wind in self.windows:
                wind.close()
        QApplication.quit()

    # ПОКАЗЫВАЕТ ОКНО ИЗМЕНЕНИЙ В НОВОЙ ВЕРСИИ
    def show_updates_info(self):
        updates_info = UpdateInfoWindow(self.root_container, f"ОБНОВЛЕНО ДО ВЕРСИИ {self.new_version}!", f"""Что нового:
{self.whats_new_text}
""")
        updates_info.show()

    # ПОКАЗЫВАЕТ ОКНО КОНТАКТОВ
    def show_contacts(self):
        if not self.is_contacts_showing:
            self.contacts_window = ContactWindow(self)
            self.contacts_window.show()
            self.is_contacts_showing = True

    # КНОПКА "ЗАПУСТИТЬ"
    def on_start_button_push(self):
        selected_character = None

        match self.characters_panel.selected_card.character_name:
            case 'БОНГО-КОТ':
                if self.get_created_characters_count(Bongo) >= self.BONGO_CAT_MAX_COUNT: return
                settings = load_settings("settings/bongo_settings.json")
                selected_character = Bongo(settings)
            case 'ФЛОРК':
                if self.get_created_characters_count(Flork) >= self.FLORK_CAT_MAX_COUNT: return
                settings = load_settings("settings/flork_settings.json")
                selected_character = Flork(settings)
            case 'АБРИКОС':
                if self.get_created_characters_count(Cat) >= self.APRICOT_CAT_MAX_COUNT: return
                settings = load_settings("settings/apricot_settings.json")
                if not self.is_cat_exists():
                    selected_character = Cat(settings, True)
                else:
                    selected_character = Cat(settings, False)
            case 'ЛЕНУСИК':
                if self.get_created_characters_count(Ham) >= self.CHAM_CAT_MAX_COUNT: return
                settings = load_settings("settings/ham_settings.json")
                selected_character = Ham(settings)

        self.windows.append(selected_character)
        selected_character.on_close.connect(lambda: self.windows.remove(selected_character))
        portal_destination = QPoint(selected_character.pos().x() + (selected_character.width() - 360) // 2,
                                    selected_character.pos().y() + (selected_character.height() - 400) // 2)
        self.portal = Portal(portal_destination)
        QTimer.singleShot(2000, selected_character.show)
        self.portal.show()

        if self.is_setting_showing:
            self.settings_window.close()

    # ПРОВЕРЯЕТ, ЕСТЬ ЛИ ЗАПУЩЕННЫЙ ПЕРСОНАЖ "АБРИКОС"
    def is_cat_exists(self):
        return any(isinstance(x, Cat) for x in self.windows)

    # ВОЗВРАЩАЕТ ЧИСЛО ЗАПУЩЕННЫХ ПЕРСНАЖЕЙ ОДНОГО ТИПА
    def get_created_characters_count(self, character):
        return sum(1 for x in self.windows if isinstance(x, character))

    # КНОПКА "НАСТРОИТЬ"
    def on_settings_button_push(self):
        if not self.is_setting_showing:
            self.is_setting_showing = True
            self.settings_window = None
            match self.characters_panel.selected_card.character_name:
                case 'БОНГО-КОТ':
                    settings = load_settings("settings/bongo_settings.json")
                    self.settings_window = Bongo.getSettingWindow(self.root_container, settings)
                case 'ФЛОРК':
                    settings = load_settings("settings/flork_settings.json")
                    self.settings_window = Flork.getSettingWindow(self.root_container, settings)
                case 'АБРИКОС':
                    settings = load_settings("settings/apricot_settings.json")
                    self.settings_window = Cat.getSettingWindow(self.root_container, settings)
                case 'ЛЕНУСИК':
                    settings = load_settings("settings/ham_settings.json")
                    self.settings_window = Ham.getSettingWindow(self.root_container, settings)

            self.settings_window.on_close.connect(self.update_settings)
            self.settings_window.show()
        else:
            self.settings_window.save_settings()

    # СНЯТИЕ ФЛАГА НАСТРОЕК ПОСЛЕ ЗАКРЫТИЯ ОКНА
    def update_settings(self):
        self.is_setting_showing = False

    # УСТАНОВКА КООРДИНАТ
    def update_bg_position(self):
        # УСТАНОВКА КООРДИНАТ ДЛЯ DESCRIPTION
        global_pos = self.description_panel.mapToGlobal(QPoint(0, 0))
        local_pos = self.root_container.mapFromGlobal(global_pos)
        self.right_shadow.setGeometry(local_pos.x() - 5, local_pos.y() + 5, 260, 345)
        # УСТАНОВКА КООРДИНАТ ДЛЯ CHARACTERS
        global_pos = self.characters_panel.mapToGlobal(QPoint(0, 0))
        local_pos = self.root_container.mapFromGlobal(global_pos)
        self.left_shadow.setGeometry(local_pos.x() - 5, local_pos.y() + 5, 450, 485)

    # СМЕНА ТЕМЫ ПРИЛОЖЕНИЯ
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

        with open(Path(os.getenv('APPDATA')) / "MeowMate" / "settings/theme_mode.json", "w", encoding='utf-8') as f:
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

    # ИНИЦИАЛИЗАЦИЯ КОНТЕЙНЕРА С ПЕРСОНАЖАМИ
    def setup_gif_container(self):
        characters = CharactersGallery(self, list(CharactersList))
        characters.character_signal.connect(self.update_character_info)
        return characters

    # ОБНОВЛЕНИЕ ВЫБРАННОГО ПЕРСОНАЖА ПРИ КЛИКЕ
    def update_character_info(self, character_a):
        self.description_panel.update_info(character_a)

    # СРАБАТЫВАЕТ ПРИ НАЖАТИИ
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 40:
            self.drag_pos = event.globalPos()

    # СРАБАТЫВАЕТ ПРИ ПЕРЕМЕЩЕНИИ
    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_pos') and self.drag_pos is not None:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()

    # СРАБАТЫВАЕТ ПРИ ОТПУСКАНИИ
    def mouseReleaseEvent(self, a0):
        self.drag_pos = None



if __name__ == "__main__":
    app = QApplication(sys.argv)
    check_settings()
    window = MainMenuWindow()
    window.show()
    app.exec()
