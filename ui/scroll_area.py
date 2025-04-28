from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea

from ui.cart import CharacterCart
from utils.enums import Characters


class CharactersGallery(QWidget):
    character_signal = pyqtSignal(Characters)

    def __init__(self, characters):
        super().__init__()
        self.cards = []
        self.selected_card = None
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)

        # Создаем скроллируемую область
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setFixedSize(450, 485)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #FFE5BD;
                border: 2px solid #000000;
                border-radius: 20px;
            }
            /* Вертикальный скроллбар */
            QScrollBar:vertical {
                background: transparent;
                width: 45px;
                margin: 10px;
               
            }
            /* Ползунок */
            QScrollBar::handle:vertical {
                background: #FFD300;
                border: 2px solid #000000;
                border-radius: 12px;
                height: 10px;
            }
            /* Убираем стрелки и дополнительные элементы */
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
                border: none;
                height: 0px;
                width: 0px;
            }
            /* Горизонтальный скроллбар (отключаем полностью) */
            QScrollBar:horizontal {
                height: 0px;
            }
        """)

        # Контейнер для карточек
        self.cards_container = QWidget()

        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Добавляем контейнер в скролл-область
        self.scroll_area.setWidget(self.cards_container)

        self.add_cards(characters)

    def add_cards(self, characters):
        row = None
        i = 0
        for character, gif_path in characters.items():
            if i % 2 == 0:
                row = QWidget()
                row.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border: none;
                }
                 """)
                layout = QHBoxLayout(row)
                layout.setSpacing(20)
                self.cards_layout.addWidget(row)

            card = CharacterCart(character, gif_path, QSize(100, 100))
            card.clicked.connect(lambda checked, c=card: self.handle_card_click(c))
            row.layout().addWidget(card)
            self.cards.append(card)
            if i == 0:
                self.selected_card = card
                card.isSelected = True
            i += 1

    def handle_card_click(self, clicked_card):
        for card in self.cards:
            card.isSelected = False
        clicked_card.isSelected = True
        self.selected_card = clicked_card
        self.character_signal.emit(clicked_card.character)
