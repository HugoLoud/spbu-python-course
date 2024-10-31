from typing import List, Dict
from project.blackjack.source.deck import Deck
from project.blackjack.source.player import AggressiveBot, ConservativeBot, RandomBot, Dealer, Player


class Game:
    """Основной класс игры, управляет раундами, участниками и результатами."""

    def __init__(self, max_rounds: int = 10):
        self.deck: Deck = Deck()
        self.players: List[Player] = []  # Список активных игроков
        self.dealer: Dealer = Dealer()
        self.max_rounds: int = max_rounds
        self.current_round: int = 0

    def add_player(self, player: Player):
        """Добавляет игрока в игру."""
        self.players.append(player)

    def start_game(self):
        """Запускает игру на определенное количество раундов."""
        for _ in range(self.max_rounds):
            self.current_round += 1
            print(f"\n=== Раунд {self.current_round} ===")
            self.deck.shuffle_deck()
            self.play_round()

            # Проверка на оставшихся игроков
            self.players = [player for player in self.players if player.balance > 0]
            if not self.players:
                print("Все игроки потеряли свои балансы. Игра окончена.")
                break

    def play_round(self):
        """Запускает один игровой раунд."""
        bets: Dict[Player, int] = self.collect_bets()

        for player in self.players:
            player.play_turn(self.deck)
            print(
                f"{player.__class__.__name__} взял: {player.show_hand()} | Очки: {player.score}"
            )

        self.dealer.play_turn(self.deck)
        print(f"Крупье взял: {self.dealer.show_hand()} | Очки: {self.dealer.score}")

        self.resolve_round(bets)
        self.reset_round()

    def collect_bets(self) -> Dict[Player, int]:
        """Собирает ставки от каждого игрока перед началом раунда."""
        bets: Dict[Player, int] = {}
        for player in self.players:
            bets[player] = player.place_bet()
            print(
                f"{player.__class__.__name__} поставил {player.current_bet} | Баланс: {player.balance}"
            )
        return bets

    def resolve_round(self, bets: Dict[Player, int]):
        """Определяет победителей и обновляет балансы игроков по результатам раунда."""
        dealer_score = self.dealer.score
        dealer_bust = dealer_score > 21

        for player, bet in bets.items():
            if player.score > 21:
                print(f"{player.__class__.__name__} перебор! Проиграл {bet}")
            elif dealer_bust or (player.score > dealer_score):
                winnings = bet * 2
                player.win_bet(winnings)
                print(
                    f"{player.__class__.__name__} победил! Выигрыш: {winnings} | Баланс: {player.balance}"
                )
            elif player.score == dealer_score:
                player.tie_bet()
                print(
                    f"{player.__class__.__name__} ничья! Возврат ставки: {bet} | Баланс: {player.balance}"
                )
            else:
                print(f"{player.__class__.__name__} проиграл! Потерял {bet}")

    def reset_round(self):
        """Сбрасывает руки и очки игроков для следующего раунда."""
        for player in self.players:
            player.reset_hand()
        self.dealer.reset_hand()
