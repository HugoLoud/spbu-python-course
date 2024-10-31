from abc import ABC, abstractmethod
import random
from deck import Deck
from card import Card, Rank


class Player(ABC):
    """Базовый класс для игроков, включающий баланс, ставку и подсчёт очков."""

    def __init__(self):
        self.hand = []
        self.score = 0
        self.balance = random.randint(10, 20) * 10  # начальный баланс от 100 до 200
        self.current_bet = 0

    def place_bet(self) -> int:
        """Определяет ставку как 10-15% от текущего баланса игрока, округленную до ближайших 10."""
        if self.balance == 0:
            self.current_bet = 0
        else:
            min_bet = max(10, (self.balance * 10) // 100)  # минимум 10% баланса
            max_bet = max(10, (self.balance * 15) // 100)  # максимум 15% баланса
            self.current_bet = random.randint(min_bet // 10, max_bet // 10) * 10
            self.current_bet = min(self.current_bet, self.balance)

        self.balance -= self.current_bet
        return self.current_bet

    def draw_card(self, deck: Deck):
        """Добавляет карту из колоды к руке игрока."""
        card = deck.draw_card()
        self.hand.append(card)
        self.calculate_score()

    def calculate_score(self) -> int:
        """Подсчет очков с учетом гибкого значения туза (1 или 11)."""
        total = 0
        aces = 0
        for card in self.hand:
            value = card.get_card_value()
            total += value
            if card.rank == Rank.ACE:
                aces += 1

        while total > 21 and aces:
            total -= 10  # Понижаем значение туза с 11 до 1
            aces -= 1

        self.score = total
        return self.score

    def reset_hand(self):
        """Сбрасывает руку и очки игрока для следующего раунда."""
        self.hand.clear()
        self.score = 0

    def show_hand(self):
        """Возвращает список карт игрока для отображения."""
        return [(card.suit, card.rank) for card in self.hand]

    def win_bet(self, winnings):
        """Добавляет выигрыш к балансу игрока."""
        self.balance += winnings

    def lose_bet(self):
        """Ничего не делает, так как ставка уже вычтена из баланса при установке."""
        pass

    def tie_bet(self):
        """Возвращает ставку игроку при ничьей."""
        self.balance += self.current_bet

    @abstractmethod
    def play_turn(self, deck: Deck):
        """Определяет действия игрока в зависимости от стратегии."""
        pass


class AggressiveBot(Player):
    """Бот с агрессивной стратегией: берет карты, пока не наберет 18 очков или больше."""

    def play_turn(self, deck: Deck):
        while self.calculate_score() < 18:
            self.draw_card(deck)


class ConservativeBot(Player):
    """Бот с консервативной стратегией: берет карты, пока не наберет 16 очков или больше."""

    def play_turn(self, deck: Deck):
        while self.calculate_score() < 16:
            self.draw_card(deck)


class RandomBot(Player):
    """Бот со случайной стратегией: иногда останавливается, иногда берет карты, если очки от 15 до 18."""

    def play_turn(self, deck: Deck):
        while self.calculate_score() < 15 or (
            self.score <= 18 and random.choice([True, False])
        ):
            self.draw_card(deck)


class Dealer(Player):
    """Крупье: берет карты, пока не наберет 17 очков или больше, затем останавливается."""

    def play_turn(self, deck: Deck):
        while self.calculate_score() < 17:
            self.draw_card(deck)
