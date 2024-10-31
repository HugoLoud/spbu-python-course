class Suit:

    """Определяет масти карт."""
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Rank:
    """Определяет ранги карт от 1 до 13 (ACE до KING)."""

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card:
    """Класс представляет одну карту с мастью и значением (рангом)."""

    def __init__(self, suit: str, rank: int):
        self.suit = suit
        self.rank = rank

    def get_card_value(self) -> int:
        """Возвращает значение карты для подсчета очков:
        Валет, дама, король дают 10, туз может дать 1 или 11, остальные карты - их номинал."""
        if self.rank in [Rank.JACK, Rank.QUEEN, Rank.KING]:
            return 10
        elif self.rank == Rank.ACE:
            return 11  # Основное значение туза (второе значение 1 учитывается при подсчете)
        else:
            return self.rank
