from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QScrollBar

from ui.cart import CharacterCart
from utils.enums import Characters


class CharactersGallery(QScrollArea):
    character_signal = pyqtSignal(Characters)

    def __init__(self, parent=None, characters=None):
        super().__init__()

        self.controller_instance = parent
        self.cards = []
        self.selected_card = None
        self.setObjectName('scroll_area')
        self.setFixedSize(450, 485)
        self.setWidgetResizable(True)

        custom_scrollbar = QScrollBar(self)
        custom_scrollbar.setObjectName('scroll_bar')
        self.setVerticalScrollBar(custom_scrollbar)

        # Контейнер для карточек
        self.cards_container = QWidget()
        self.cards_container.setObjectName('main')
        self.cards_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Добавляем контейнер в скролл-область
        self.setWidget(self.cards_container)

        self.add_cards(characters)


    def add_cards(self, characters):
        row = None

        for i, character in enumerate(characters):
            if i % 2 == 0:
                row = QWidget()
                row.setObjectName('row_of_cards')
                layout = QHBoxLayout(row)
                layout.setSpacing(20)
                self.cards_layout.addWidget(row)

            card = CharacterCart(self,character.character, character.gif_path, character.size, character.speed)
            card.clicked.connect(lambda checked, c=card: self.handle_card_click(c))
            row.layout().addWidget(card)
            self.cards.append(card)
            if i == 0:
                self.selected_card = card
                card.isSelected = True



    def handle_card_click(self, clicked_card):
        for card in self.cards:
            card.isSelected = False
        clicked_card.isSelected = True
        self.selected_card = clicked_card
        self.character_signal.emit(clicked_card.character)
