from source.game import Game
from source.player import AggressiveBot, ConservativeBot, RandomBot

if __name__ == "__main__":
    game = Game(max_rounds=10)
    game.add_player(AggressiveBot())
    game.add_player(ConservativeBot())
    game.add_player(RandomBot())
    game.start_game()
