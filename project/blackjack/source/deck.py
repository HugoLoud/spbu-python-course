import random
from card import Card, Suit, Rank


class Deck:
    """Класс представляет колоду карт и методы для её перетасовки и сброса."""

    def __init__(self):
        self.cards = []
        self.reset_deck()  # Инициализация колоды

    def reset_deck(self):
        """Создаёт и перетасовывает новую полную колоду карт."""
        self.cards = [
            Card(suit, rank)
            for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]
            for rank in range(Rank.ACE, Rank.KING + 1)
        ]
        self.shuffle_deck()

    def shuffle_deck(self):
        """Перетасовывает текущую колоду карт."""
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        """Извлекает карту из колоды. Сбрасывает и перетасовывает колоду, если она пуста."""
        if not self.cards:
            self.reset_deck()  # Обновляем колоду, если карты закончились
        return self.cards.pop()
