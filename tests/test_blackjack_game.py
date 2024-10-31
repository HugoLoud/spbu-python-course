import pytest
from project.blackjack.source.game import Game
from project.blackjack.source.deck import Deck
from project.blackjack.source.player import (
    AggressiveBot,
    ConservativeBot,
    RandomBot,
    Dealer,
)


def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 52  # Проверка, что в колоде 52 карты


def test_deck_reset():
    deck = Deck()
    _ = [deck.draw_card() for _ in range(52)]  # Извлечение всех карт
    assert len(deck.cards) == 0  # Колода пуста
    deck.reset_deck()  # Обновление колоды
    assert len(deck.cards) == 52  # Колода снова полна


def test_player_balance():
    player = AggressiveBot()
    assert 100 <= player.balance <= 200  # Начальный баланс в пределах


def test_place_bet():
    player = ConservativeBot()
    initial_balance = player.balance
    bet = player.place_bet()
    assert bet <= initial_balance  # Ставка не превышает баланс


def test_game_initialization():
    game = Game()
    game.add_player(AggressiveBot())
    game.add_player(ConservativeBot())
    game.add_player(RandomBot())
    assert len(game.players) == 3  # Три игрока в игре


def test_game_round_changes():
    game = Game(max_rounds=3)
    game.add_player(AggressiveBot())
    game.add_player(ConservativeBot())
    game.add_player(RandomBot())
    initial_round = game.current_round
    game.start_game()
    assert game.current_round > initial_round  # Текущий раунд изменился
