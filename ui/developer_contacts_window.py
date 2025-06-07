
import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QDesktopServices, QMovie
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget

from ui.service_button import SvgButton
from ui.settings_window import SettingsWindow


def open_link(url):
    QDesktopServices.openUrl(QUrl(url))


class ContactWindow(SettingsWindow):
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is not None:
        app_directory = Path(base_path)
    else:
        app_directory = Path(__file__).parent.parent
    resource_path = app_directory / 'drawable' / 'menu'

    def __init__(self, _parent):
        super().__init__(_parent)
        self.parent_instance = _parent
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setObjectName('contacts_window')



        # ТИТУЛЬНИК
        self.title = QLabel("Связь с\nразработчиком:", self)
        self.title.setObjectName("title")
        self.title.setGeometry(20, 20, 300, 80)

        # QR-код и утка
        self.qr_container = QWidget(self)
        self.qr_container.setGeometry(10,95,300,200 )
        self.qr_container.setObjectName('contacts_container')
        self.hbox_qr = QHBoxLayout(self.qr_container)
        self.qr_code = QSvgWidget(str(self.resource_path / "qr.svg"))
        self.qr_code.setFixedSize(165,165)
        self.duck = QLabel()
        self.duck.setFixedSize(100,80)
        self.duck.setObjectName('duck')
        self.duck_gif = QMovie(str(self.resource_path / 'duck.gif'))
        self.duck_gif.setSpeed(120)
        self.duck_gif.setScaledSize(QSize(100, 80))
        self.duck.setMovie(self.duck_gif)
        self.duck_gif.start()
        self.hbox_qr.addWidget(self.qr_code, alignment=Qt.AlignBottom)
        self.hbox_qr.addWidget(self.duck,alignment=Qt.AlignBottom)

        # ТЕЛЕГРАММ
        self.hbox_tg = QHBoxLayout()
        self.tg_icon = QSvgWidget(str(self.resource_path / "tg.svg"))
        self.tg_icon.setFixedSize(30, 30)
        self.tg_label = QLabel('<a href="https://t.me/olezha_zaostrovtsev" style=" font-size: 14px; font-weight: light; font-family: PT Mono; color: black; text-decoration: none;">Telegram: @olezha_zaostrovtsev</a>', self)
        self.tg_label.linkActivated.connect(open_link)
        self.hbox_tg.addWidget(self.tg_icon)
        self.hbox_tg.addWidget(self.tg_label,alignment=Qt.AlignLeft)
        # GITGUB
        self.hbox_github = QHBoxLayout()
        self.github_icon = QSvgWidget(str(self.resource_path / "github.svg"))
        self.github_icon.setFixedSize(30, 30)
        self.github = QLabel('<a href="https://github.com/KuivaMachine" style=" font-size: 14px; font-weight: light; font-family: PT Mono; color: black; text-decoration: none;">GitHub: KuivaMachine</a>', self)
        self.github.linkActivated.connect(open_link)
        self.hbox_github.addWidget(self.github_icon)
        self.hbox_github.addWidget(self.github,alignment=Qt.AlignLeft)
        # EMAIL
        self.hbox_email = QHBoxLayout()
        self.email_icon = QSvgWidget(str(self.resource_path / "email.svg"))
        self.email_icon.setFixedSize(30, 21)
        self.email = QLabel('<a href="mailto:olegzaostrovtsev19@yandex.ru" style=" font-size: 12px; font-weight: light; font-family: PT Mono; color: black; text-decoration: none;">Email: olegzaostrovtsev19@yandex.ru</a>', self)
        self.email.linkActivated.connect(open_link)
        self.hbox_email.addWidget(self.email_icon)
        self.hbox_email.addWidget(self.email,alignment=Qt.AlignLeft)

        self.contacts_container = QWidget(self)
        self.contacts_container.setGeometry(10,300,320,150)
        self.contacts_container.setObjectName('contacts_container')
        self.vbox_contacts = QVBoxLayout(self.contacts_container)
        self.vbox_contacts.setSpacing(10)
        self.vbox_contacts.addLayout(self.hbox_tg)
        self.vbox_contacts.addLayout(self.hbox_github)
        self.vbox_contacts.addLayout(self.hbox_email)

        # КНОПКА ЗАКРЫТЬ
        self.close_btn = SvgButton(
            str(self.resource_path / "close_but.svg"), self)
        self.close_btn.move(270, 20)
        self.close_btn.clicked.connect(self.close)
        self.setup_styles()

    def closeEvent(self, a0):
        self.parent_instance.is_contacts_showing = False

    def setup_styles(self):
        self.setStyleSheet("""
            QLabel#contacts_window {
                background: #FFD09E;
                border-radius: 15px;
                border: 2px solid black;
            }
            QLabel#duck {
                background: transparent;
                border: none;
            }
            QLabel#title {
                font-size: 26px;
                font-weight: light;
                font-family: 'PT Mono';
                color: black;
                background: transparent;
                border: none;
            }
            QWidget#contacts_container {
                font-size: 10px;
                font-weight: bold;
                font-family: 'JetBrains Mono';
                color: black;
                background: transparent;
                border: none;
            }
            QPushButton {
                background-color: #FF999E;
                color: white;
                border-radius: 10px;
                padding: 5px;
                font-family: 'JetBrains Mono';
            }

            QPushButton:hover {
                background-color: #F9A9AD;
            }
            """)


